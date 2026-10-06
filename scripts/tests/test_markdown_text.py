from docs_checks.markdown_text import prose_lines


def test_a_tilde_line_inside_a_backtick_fence_does_not_close_it():
    text = "```\n~~~\nvos podés\n```\nprosa\n"
    assert prose_lines(text) == [(5, "prosa")]


def test_a_shorter_backtick_run_does_not_close_a_longer_fence():
    text = "````\n```\nvos\n````\nprosa\n"
    assert prose_lines(text) == [(5, "prosa")]
