import posixpath
import re
from pathlib import Path

REFRESH = re.compile(r'http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', re.IGNORECASE)
MAX_HOPS = 3


def old_paths(sitemap_xml, site_url):
    base = site_url if site_url.endswith("/") else site_url + "/"
    return [loc[len(base):] for loc in re.findall(r"<loc>(.*?)</loc>", sitemap_xml) if loc.startswith(base)]


def _page(site_dir, path):
    candidate = site_dir / path / "index.html" if path.endswith("/") or path == "" else site_dir / path
    return candidate if candidate.is_file() else None


def _follow(site_dir, path):
    current = path
    for _ in range(MAX_HOPS + 1):
        page = _page(site_dir, current)
        if page is None:
            return current, "missing"
        match = REFRESH.search(page.read_text(encoding="utf-8", errors="ignore"))
        if not match:
            return current, None
        target = match.group(1).split("#", 1)[0]
        joined = posixpath.normpath(posixpath.join(current or ".", target))
        current = "" if joined == "." else joined.lstrip("/") + ("/" if target.endswith("/") else "")
    return path, "chain"


def unresolved(site_dir, paths):
    problems = []
    for path in paths:
        final, error = _follow(Path(site_dir), path)
        if error == "chain":
            problems.append(f"{path} (redirect chain longer than {MAX_HOPS})")
        elif error == "missing" and final == path:
            problems.append(f"{path} (missing)")
        elif error == "missing":
            problems.append(f"{path} -> {final} (missing)")
    return problems


def run(args):
    sitemap, site_dir = args
    xml = Path(sitemap).read_text(encoding="utf-8")
    return unresolved(Path(site_dir), old_paths(xml, "https://mage-obsidian.jeanmarcos.dev/"))
