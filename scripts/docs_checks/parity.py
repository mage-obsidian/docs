from pathlib import Path


def missing_counterparts(docs_dir):
    docs_dir = Path(docs_dir)
    english = {p.relative_to(docs_dir).as_posix() for p in docs_dir.rglob("*.md") if not p.name.endswith(".es.md")}
    spanish = {p.relative_to(docs_dir).as_posix() for p in docs_dir.rglob("*.es.md")}
    problems = [f"{e[:-3]}.es.md (missing)" for e in english if f"{e[:-3]}.es.md" not in spanish]
    problems += [f"{s[:-6]}.md (missing)" for s in spanish if f"{s[:-6]}.md" not in english]
    return sorted(problems)


def run(args):
    return missing_counterparts(Path(args[0] if args else "docs"))
