from pathlib import Path

from mkdocs.structure.files import File
from mkdocs_redirects.plugin import get_html_path, get_relative_html_path, write_html


def _target(old, new, use_directory_urls):
    if new.lower().startswith(("http://", "https://")):
        return new
    path, hash_mark, fragment = new.partition("#")
    url = File(path, "", "", use_directory_urls).url
    return get_relative_html_path(old, url + hash_mark + fragment, use_directory_urls)


def write_es_redirects(site_dir, redirect_maps, use_directory_urls=True):
    es_dir = Path(site_dir) / "es"
    for old, new in redirect_maps.items():
        write_html(
            str(es_dir),
            get_html_path(old, use_directory_urls),
            _target(old, new, use_directory_urls),
        )


def on_post_build(config):
    redirect_maps = config.plugins["redirects"].config["redirect_maps"]
    write_es_redirects(config["site_dir"], redirect_maps, config["use_directory_urls"])
