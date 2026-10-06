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


LIGHTHOUSE = {"performance": 100, "accessibility": 98, "best_practices": 100, "seo": 100, "date": "2026-10-06",
              "form_factor": "mobile", "tool": "Lighthouse", "version": "13.5.0", "runs": 3, "aggregate": "median"}


def test_lighthouse_scores_are_joined_in_category_order():
    assert docs_main.render_lighthouse_scores(LIGHTHOUSE) == "100/98/100/100"


def test_lighthouse_note_states_tool_form_factor_runs_and_date():
    note = docs_main.render_lighthouse_note(LIGHTHOUSE, "en")
    assert "Accessibility 98" in note
    assert "Lighthouse 13.5.0, mobile, median of 3 runs, 2026-10-06." in note


def test_lighthouse_note_in_spanish():
    note = docs_main.render_lighthouse_note(LIGHTHOUSE, "es")
    assert "Accesibilidad 98" in note
    assert "Lighthouse 13.5.0, móvil, mediana de 3 ejecuciones, 2026-10-06." in note


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


def test_timeline_marks_now_and_next():
    milestones = [
        {"date": "2026-06-22", "version": "2.0.0", "link": "changelog.md#june-2026", "now": False,
         "en": {"title": "The 2.0.0 cut", "text": "Islands"}, "es": {"title": "El corte 2.0.0", "text": "Islas"}},
        {"date": "2026-10-06", "version": "4.0.0", "link": "changelog.md#400", "now": True,
         "en": {"title": "4.0 stable", "text": "Stable"}, "es": {"title": "4.0 estable", "text": "Estable"}},
        {"date": None, "version": None, "link": None, "now": False,
         "en": {"title": "Wider compatibility", "text": "2.4.7"}, "es": {"title": "Más compatibilidad", "text": "2.4.7"}},
    ]
    html = docs_main.render_timeline(milestones, "es")
    assert html.count('class="mo-ms') == 3
    assert 'class="mo-ms mo-ms--now"' in html
    assert 'class="mo-ms mo-ms--next"' in html
    assert '<time datetime="2026-06-22">' in html
    assert "El corte 2.0.0" in html and "The 2.0.0 cut" not in html


def test_lanes_show_progress_only_when_measured():
    lanes = [{"key": "now", "items": [
        {"progress": 96, "measure_en": "317 covered · 3 blocked", "measure_es": "317 cubiertas · 3 bloqueadas",
         "en": {"title": "Full Luma parity", "text": "x"}, "es": {"title": "Paridad completa con Luma", "text": "x"}},
        {"progress": None, "measure_en": None, "measure_es": None,
         "en": {"title": "Reference", "text": "y"}, "es": {"title": "Referencia", "text": "y"}},
    ]}]
    html = docs_main.render_lanes(lanes, "en")
    assert html.count('role="progressbar"') == 1
    assert 'aria-valuenow="96"' in html
    assert "317 covered · 3 blocked" in html


def test_timeline_and_lanes_macros_read_their_own_data_keys():
    env = FakeEnv("en")
    env.variables["milestones"] = [
        {"date": None, "version": None, "link": None, "now": False,
         "en": {"title": "Later", "text": "t"}, "es": {"title": "Después", "text": "t"}},
    ]
    env.variables["lanes"] = [{"key": "later", "items": []}]
    docs_main.define_env(env)
    assert "timeline" not in env.variables and "roadmap_lanes" not in env.variables
    assert "mo-ms--next" in env.macros["timeline"]()
    assert "mo-lane--later" in env.macros["roadmap_lanes"]()
