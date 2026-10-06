import re

FENCE = re.compile(r"^\s*(```|~~~)")
INLINE = re.compile(r"`[^`]*`")


def prose_lines(text):
    lines = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append((number, INLINE.sub(" ", line)))
    return lines
