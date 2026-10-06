import re
from pathlib import Path

from docs_checks.markdown_text import prose_lines

WORDS = [
    "vos", "podés", "querés", "tenés", "hacé", "fijate", "mirá", "dale", "acá", "che",
    "usá", "instalá", "ejecutá", "corré", "agregá", "creá", "probá", "revisá", "configurá",
    "elegí", "escribí", "seguí", "abrí", "definí", "vosotros", "tío", "órale", "güey", "chido",
    "activá", "sos", "sabés", "necesitás", "tené", "poné", "decí", "andá", "guardá", "cambiá",
    "borrá", "copiá", "pegá", "verificá", "reiniciá", "ingresá", "completá", "asegurate", "acordate",
]

PATTERN = re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in WORDS) + r")(?![\w-])", re.IGNORECASE)


def find_voseo(docs_dir):
    docs_dir = Path(docs_dir)
    findings = []
    for page in sorted(docs_dir.rglob("*.es.md")):
        relative = page.relative_to(docs_dir).as_posix()
        for number, line in prose_lines(page.read_text(encoding="utf-8")):
            for match in PATTERN.finditer(line):
                findings.append(f"{relative}:{number}: {match.group(1).lower()}")
    return findings


def run(args):
    return find_voseo(Path(args[0] if args else "docs"))
