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


NOT_FOUND = {}


def on_post_template(output_content, template_name, config):
    if template_name == "404.html":
        NOT_FOUND[config.theme["language"]] = output_content
    return output_content


def write_not_found(site_dir, pages):
    for language, target in (("en", Path(site_dir)), ("es", Path(site_dir) / "es")):
        if language in pages:
            target.mkdir(parents=True, exist_ok=True)
            (target / "404.html").write_text(pages[language], encoding="utf-8")


def on_post_build(config):
    write_not_found(config["site_dir"], NOT_FOUND)
    redirect_maps = config.plugins["redirects"].config["redirect_maps"]
    write_es_redirects(config["site_dir"], redirect_maps, config["use_directory_urls"])
