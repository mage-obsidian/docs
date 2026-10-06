from docs_checks.links_internal import find_protocol_relative


def test_a_link_starting_with_two_slashes_is_reported(docs_tree):
    site = docs_tree({"404.html": '<a href="//es/">home</a><a href="//">x</a>'})
    assert find_protocol_relative(site) == ["404.html: 2 protocol-relative link(s) starting with //"]


def test_root_absolute_relative_and_full_urls_pass(docs_tree):
    site = docs_tree({"es/404.html": '<a href="/es/">a</a><a href="../x/">b</a><a href="https://example.com//path">c</a>'})
    assert find_protocol_relative(site) == []


def test_single_quoted_and_src_attributes_are_covered(docs_tree):
    site = docs_tree({"x/index.html": "<img src='//cdn.example/a.png'>"})
    assert len(find_protocol_relative(site)) == 1
