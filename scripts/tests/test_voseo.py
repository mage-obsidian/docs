from docs_checks.voseo import find_voseo


def test_voseo_ignores_code_but_flags_prose(docs_tree):
    docs = docs_tree({"g.es.md": "Ejecutá el comando.\n\n```bash\necho vos\n```\n\nUsa `acá` como valor.\nMirá el resultado acá.\n"})
    assert find_voseo(docs) == ["g.es.md:1: ejecutá", "g.es.md:8: mirá", "g.es.md:8: acá"]


def test_english_pages_are_not_scanned(docs_tree):
    docs = docs_tree({"g.md": "vos podés"})
    assert find_voseo(docs) == []


def test_neutral_spanish_passes(docs_tree):
    docs = docs_tree({"g.es.md": "Ejecuta el comando aquí y revisa el resultado.\n"})
    assert find_voseo(docs) == []


def test_widened_voseo_forms_are_flagged_in_prose(docs_tree):
    docs = docs_tree({"g.es.md": "Activá la opción y guardá el cambio.\n"})
    assert find_voseo(docs) == ["g.es.md:1: activá", "g.es.md:1: guardá"]
