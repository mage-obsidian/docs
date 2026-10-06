import re

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE = re.compile(r"`[^`]*`")


def _closes(opening, delimiter):
    return delimiter[0] == opening[0] and len(delimiter) >= len(opening)


def prose_lines(text):
    lines = []
    opening = None
    for number, line in enumerate(text.splitlines(), start=1):
        fence = FENCE.match(line)
        if fence and opening is None:
            opening = fence.group(1)
            continue
        if fence and _closes(opening, fence.group(1)):
            opening = None
            continue
        if opening is None:
            lines.append((number, INLINE.sub(" ", line)))
    return lines
