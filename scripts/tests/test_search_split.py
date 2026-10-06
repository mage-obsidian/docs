import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("search_split", Path(__file__).resolve().parents[2] / "hooks/search_split.py")
search_split = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search_split)


def test_split_index_separates_languages():
    index = {"config": {"lang": ["en", "es"]}, "docs": [
        {"location": "", "title": "Home", "text": "a"},
        {"location": "why/", "title": "Why", "text": "b"},
        {"location": "es/", "title": "Inicio", "text": "c"},
        {"location": "es/why/", "title": "Por qué", "text": "d"},
    ]}
    parts = search_split.split_index(index, ["es"])
    assert [d["location"] for d in parts[""]["docs"]] == ["", "why/"]
    assert [d["location"] for d in parts["es"]["docs"]] == ["", "why/"]
    assert parts["es"]["config"] == {"lang": ["en", "es"]}
