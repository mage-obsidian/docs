from docs_checks.parity import missing_counterparts


def test_pages_with_both_languages_pass(docs_tree):
    docs = docs_tree({"a.md": "x", "a.es.md": "x", "sub/b.md": "x", "sub/b.es.md": "x"})
    assert missing_counterparts(docs) == []


def test_a_missing_translation_and_an_orphan_translation_are_reported(docs_tree):
    docs = docs_tree({"a.md": "x", "b.es.md": "x", "data/roadmap.yml": "x"})
    assert missing_counterparts(docs) == ["a.es.md (missing)", "b.md (missing)"]
