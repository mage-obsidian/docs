import html
import re
from pathlib import Path

BANNED = [
    "Pre-1.0",
    "not yet available",
    "independently versioned",
    "once parity is reached",
    "ready to try",
    "one version train",
    "module-modern-frontend/discussions",
    "aún no está disponible",
    "versionados de forma independiente",
    "cuando se alcance la paridad",
    "listo para probar",
]

ALLOWED = {
    "independently versioned": ["changelog/index.html", "project/changelog/index.html"],
    "versionados de forma independiente": ["es/changelog/index.html", "es/project/changelog/index.html"],
}

TAGS = re.compile(r"<[^>]+>")
SPACE = re.compile(r"\s+")


def _text(markup):
    return SPACE.sub(" ", html.unescape(TAGS.sub(" ", markup))).lower()


def find_banned(site_dir, banned, allowed):
    site_dir = Path(site_dir)
    findings = []
    for page in sorted(site_dir.rglob("*.html")):
        relative = page.relative_to(site_dir).as_posix()
        text = _text(page.read_text(encoding="utf-8", errors="ignore"))
        for phrase in banned:
            if SPACE.sub(" ", phrase.lower()) in text and relative not in allowed.get(phrase, []):
                findings.append(f"{relative}: {phrase}")
    return findings


MIRRORS = [
    "module-modern-frontend", "module-modern-frontend-cli", "module-modern-frontend-twig",
    "component-modern-frontend", "js-package-utils", "theme-base",
    "module-catalog", "module-catalog-search", "module-checkout", "module-customer", "module-downloadable",
    "module-gift-message", "module-instant-purchase", "module-multishipping", "module-persistent",
    "module-product-alert", "module-review", "module-sales", "module-search", "module-send-friend",
    "module-showcase", "module-storefront", "module-vault", "module-wishlist",
]

MIRROR_ALLOWED = ["reference/packages/index.html", "es/reference/packages/index.html"]


def find_mirror_links(site_dir, mirrors, allowed):
    site_dir = Path(site_dir)
    pattern = re.compile(r"github\.com/mage-obsidian/(" + "|".join(re.escape(m) for m in mirrors) + r")(?![\w-])")
    findings = []
    for page in sorted(site_dir.rglob("*.html")):
        relative = page.relative_to(site_dir).as_posix()
        if relative in allowed:
            continue
        for name in sorted(set(pattern.findall(page.read_text(encoding="utf-8", errors="ignore")))):
            findings.append(f"{relative}: github.com/mage-obsidian/{name}")
    return findings


def run(args):
    site = Path(args[0] if args else "site")
    return find_banned(site, BANNED, ALLOWED) + find_mirror_links(site, MIRRORS, MIRROR_ALLOWED)
