import re
import time
from pathlib import Path

import requests

HREF = re.compile(r'href="(https://(?:github\.com/mage-obsidian|packagist\.org|www\.npmjs\.com)[^"#]*)"')


def external_links(site_dir):
    found = set()
    for page in Path(site_dir).rglob("*.html"):
        found.update(HREF.findall(page.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)


def broken(urls, fetch, attempts=3, pause=1.0):
    problems = []
    for url in urls:
        status = None
        for _ in range(attempts):
            status = fetch(url)
            if status < 500 and status != 429:
                break
            time.sleep(pause)
        if status >= 400:
            problems.append(f"{url} ({status})")
    return problems


def run(args):
    session = requests.Session()
    fetch = lambda url: session.head(url, allow_redirects=True, timeout=15).status_code
    return broken(external_links(Path(args[0] if args else "site")), fetch)
