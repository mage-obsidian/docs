from docs_checks.phrases import find_banned, find_mirror_links


def test_a_banned_phrase_in_the_build_is_reported(docs_tree):
    site = docs_tree({"why/comparison/index.html": "<td>Maturity</td><td>Pre-1.0</td>"})
    assert find_banned(site, ["Pre-1.0"], {}) == ["why/comparison/index.html: Pre-1.0"]


def test_banned_phrase_allowed_only_in_listed_path(docs_tree):
    site = docs_tree({
        "project/changelog/index.html": "packages were independently versioned until 4.0",
        "index.html": "independently versioned",
    })
    allowed = {"independently versioned": ["project/changelog/index.html"]}
    assert find_banned(site, ["independently versioned"], allowed) == ["index.html: independently versioned"]


def test_matching_ignores_case_and_html_tags(docs_tree):
    site = docs_tree({"x/index.html": "<p>Ready <b>to</b> try</p>"})
    assert find_banned(site, ["ready to try"], {}) == ["x/index.html: ready to try"]


def test_mirror_urls_are_allowed_only_in_the_package_map(docs_tree):
    site = docs_tree({
        "reference/packages/index.html": '<a href="https://github.com/mage-obsidian/module-catalog">x</a>',
        "guides/index.html": '<a href="https://github.com/mage-obsidian/module-catalog/blob/master/README.md">x</a>'
                             '<a href="https://github.com/mage-obsidian/framework">y</a>'
                             '<a href="https://github.com/mage-obsidian/theme-default">z</a>',
    })
    assert find_mirror_links(site, ["module-catalog"], ["reference/packages/index.html"]) == [
        "guides/index.html: github.com/mage-obsidian/module-catalog"]
