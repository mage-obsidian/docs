import importlib.util
from pathlib import Path

HOOK = Path(__file__).resolve().parents[2] / "hooks" / "i18n_redirects.py"
spec = importlib.util.spec_from_file_location("i18n_redirects", HOOK)
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


def test_each_language_owns_its_own_not_found_page(tmp_path):
    hook.write_not_found(tmp_path, {"en": "<html lang='en'>", "es": "<html lang='es'>"})
    assert (tmp_path / "404.html").read_text(encoding="utf-8") == "<html lang='en'>"
    assert (tmp_path / "es" / "404.html").read_text(encoding="utf-8") == "<html lang='es'>"


def test_a_language_that_was_not_rendered_is_skipped(tmp_path):
    hook.write_not_found(tmp_path, {"en": "<html lang='en'>"})
    assert not (tmp_path / "es").exists()
