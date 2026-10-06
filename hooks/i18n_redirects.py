import posixpath
from pathlib import Path

PAGE = """<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Redirecting...</title>
    <link rel="canonical" href="{target}">
    <script>var anchor=window.location.hash.substr(1);location.href="{target}"+(anchor?"#"+anchor:"")</script>
    <meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
You're being redirected to a <a href="{target}">new destination</a>.
</body>
</html>
"""


def _directory(markdown_path):
    return markdown_path[: -len(".md")]


def write_es_redirects(site_dir, redirect_maps):
    for old, new in redirect_maps.items():
        old_directory = _directory(old)
        target = posixpath.relpath(_directory(new), old_directory) + "/"
        page = Path(site_dir) / "es" / old_directory / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(PAGE.format(target=target), encoding="utf-8")


def on_post_build(config):
    redirect_maps = config.plugins["redirects"].config["redirect_maps"]
    write_es_redirects(config["site_dir"], redirect_maps)
