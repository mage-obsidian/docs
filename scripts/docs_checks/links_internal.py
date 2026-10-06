import re
from pathlib import Path

PROTOCOL_RELATIVE = re.compile(r"""(?:href|src|action)\s*=\s*["']//""", re.IGNORECASE)


def find_protocol_relative(site_dir):
    site_dir = Path(site_dir)
    findings = []
    for page in sorted(site_dir.rglob("*.html")):
        text = page.read_text(encoding="utf-8", errors="ignore")
        count = len(PROTOCOL_RELATIVE.findall(text))
        if count:
            findings.append(f"{page.relative_to(site_dir).as_posix()}: {count} protocol-relative link(s) starting with //")
    return findings


def run(args):
    return find_protocol_relative(args[0] if args else "site")
