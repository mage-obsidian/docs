from docs_checks.links import broken, external_links


def test_only_project_registries_are_collected(docs_tree):
    site = docs_tree({"a/index.html": '<a href="https://github.com/mage-obsidian/framework">x</a><a href="https://example.com">y</a>'})
    assert external_links(site) == ["https://github.com/mage-obsidian/framework"]


def test_a_transient_error_is_retried_and_a_404_reported():
    calls = {"https://a": [503, 200], "https://b": [404]}
    fetch = lambda url: calls[url].pop(0)
    assert broken(["https://a", "https://b"], fetch, pause=0) == ["https://b (404)"]
