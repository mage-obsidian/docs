from docs_checks.redirects import old_paths, unresolved

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://example.test/</loc></url>
<url><loc>https://example.test/components/modules/0105-vue-islands/</loc></url>
<url><loc>https://example.test/es/components/modules/0105-vue-islands/</loc></url>
</urlset>"""

REDIRECT = '<html><head><meta http-equiv="refresh" content="0; url={target}"></head></html>'


def test_old_paths_are_relative_to_the_site_url():
    assert old_paths(SITEMAP, "https://example.test/") == [
        "",
        "components/modules/0105-vue-islands/",
        "es/components/modules/0105-vue-islands/",
    ]


def test_a_path_with_its_own_page_resolves(docs_tree):
    site = docs_tree({"index.html": "<h1>home</h1>"})
    assert unresolved(site, [""]) == []


def test_es_prefixed_old_url_resolves_through_redirect(docs_tree):
    site = docs_tree({
        "es/components/modules/0105-vue-islands/index.html": REDIRECT.format(target="../../../guides/vue/islands/"),
        "es/guides/vue/islands/index.html": "<h1>Islas</h1>",
    })
    assert unresolved(site, ["es/components/modules/0105-vue-islands/"]) == []


def test_a_redirect_to_a_missing_page_is_reported(docs_tree):
    site = docs_tree({
        "components/overview/index.html": REDIRECT.format(target="../../why/"),
    })
    assert unresolved(site, ["components/overview/"]) == ["components/overview/ -> why/ (missing)"]


def test_a_path_with_nothing_is_reported(docs_tree):
    site = docs_tree({"index.html": "x"})
    assert unresolved(site, ["roadmap/"]) == ["roadmap/ (missing)"]


def test_a_redirect_loop_is_reported(docs_tree):
    site = docs_tree({
        "a/index.html": REDIRECT.format(target="../b/"),
        "b/index.html": REDIRECT.format(target="../a/"),
    })
    assert unresolved(site, ["a/"]) == ["a/ (redirect chain longer than 3)"]


def test_the_hook_mirrors_redirects_under_es(tmp_path):
    import importlib.util
    from pathlib import Path

    hook_path = Path(__file__).resolve().parents[2] / "hooks" / "i18n_redirects.py"
    spec = importlib.util.spec_from_file_location("i18n_redirects", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.write_es_redirects(tmp_path, {"showcase.md": "why/showcase.md"})

    page = (tmp_path / "es/showcase/index.html").read_text()
    assert "url=../why/showcase/" in page


def _load_hook():
    import importlib.util
    from pathlib import Path

    hook_path = Path(__file__).resolve().parents[2] / "hooks" / "i18n_redirects.py"
    spec = importlib.util.spec_from_file_location("i18n_redirects", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_hook_redirects_index_pages_on_both_sides(tmp_path):
    module = _load_hook()
    for page in ("es/why/index.html", "es/guides/twig/index.html"):
        target = tmp_path / page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("<h1>page</h1>")

    module.write_es_redirects(
        tmp_path,
        {
            "introduction/index.md": "why/index.md",
            "components/overview.md": "why/index.md",
            "twig/index.md": "guides/twig.md",
        },
    )

    assert (tmp_path / "es/introduction/index.html").is_file()
    assert not (tmp_path / "es/introduction/index/index.html").exists()
    assert unresolved(tmp_path, ["es/introduction/", "es/components/overview/", "es/twig/"]) == []


def test_the_hook_keeps_fragments_and_external_targets(tmp_path):
    module = _load_hook()

    module.write_es_redirects(
        tmp_path,
        {"a.md": "b.md#part", "c.md": "https://example.test/x"},
    )

    assert "url=../b/#part" in (tmp_path / "es/a/index.html").read_text()
    assert "url=https://example.test/x" in (tmp_path / "es/c/index.html").read_text()
