import json
from pathlib import Path

from mkdocs.plugins import event_priority


def split_index(index, languages):
    prefixes = tuple(f"{lang}/" for lang in languages)
    parts = {"": {"config": index["config"], "docs": [d for d in index["docs"] if not d["location"].startswith(prefixes)]}}
    for lang in languages:
        prefix = f"{lang}/"
        docs = [dict(d, location=d["location"][len(prefix):]) for d in index["docs"] if d["location"].startswith(prefix)]
        parts[lang] = {"config": index["config"], "docs": docs}
    return parts


@event_priority(-100)
def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    source = site / "search" / "search_index.json"
    if not source.exists():
        return
    index = json.loads(source.read_text(encoding="utf-8"))
    for lang, part in split_index(index, ["es"]).items():
        target = site / lang / "search" / "search_index.json" if lang else source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(part, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
