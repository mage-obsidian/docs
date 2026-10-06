import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("docs_main", Path(__file__).resolve().parents[2] / "main.py")
docs_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docs_main)


def test_verified_chip_lists_platforms_and_date():
    html = docs_main.render_verified({"platforms": ["Magento Open Source 2.4.9", "Mage-OS 2.4.9"], "date": "2026-10-06", "source": "zento-matrix"}, "en")
    assert 'class="mo-verified"' in html
    assert "Verified on Magento Open Source 2.4.9 · Mage-OS 2.4.9" in html
    assert 'datetime="2026-10-06"' in html


def test_verified_chip_in_spanish():
    html = docs_main.render_verified({"platforms": ["Mage-OS 2.4.9"], "date": "2026-10-06", "source": "zento-matrix"}, "es")
    assert "Verificado en Mage-OS 2.4.9" in html


def test_compat_table_marks_each_cell():
    cells = [
        {"distro": "mageos", "version": "2.4.9", "result": "pass", "date": "2026-10-06"},
        {"distro": "community", "version": "2.4.7", "result": "fail", "date": "2026-10-07"},
        {"distro": "community", "version": "2.4.8", "result": "pending", "date": ""},
    ]
    table = docs_main.render_compat_table(cells, "en")
    assert "| Magento Open Source 2.4.7 | ❌ Failed | 2026-10-07 |" in table
    assert "| Magento Open Source 2.4.8 | ⏳ Not run yet | — |" in table
    assert "| Mage-OS 2.4.9 | ✅ Passed | 2026-10-06 |" in table


class FakeEnv:
    def __init__(self, language):
        self.conf = {"theme": {"language": language}}
        self.variables = {
            "verifications": {"matrix": {"platforms": ["Mage-OS 2.4.9"], "date": "2026-10-06", "source": "zento-matrix"}},
            "compatibility": {"cells": []},
        }
        self.macros = {}

    def macro(self, function):
        self.macros[function.__name__] = function
        return function


def test_verified_macro_is_registered_apart_from_the_verifications_data():
    env = FakeEnv("es")
    docs_main.define_env(env)
    assert "verified" in env.macros
    assert "verified" not in env.variables
    assert "Verificado en Mage-OS 2.4.9" in env.macros["verified"]("matrix")
