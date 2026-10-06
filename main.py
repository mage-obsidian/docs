LABELS = {
    "en": {"verified": "Verified on", "pass": "✅ Passed", "fail": "❌ Failed", "pending": "⏳ Not run yet",
           "platform": "Platform", "result": "Result", "date": "Date"},
    "es": {"verified": "Verificado en", "pass": "✅ Pasa", "fail": "❌ Falla", "pending": "⏳ Sin ejecutar",
           "platform": "Plataforma", "result": "Resultado", "date": "Fecha"},
}

DISTROS = {"community": "Magento Open Source", "mageos": "Mage-OS"}


def render_verified(entry, lang):
    label = LABELS[lang]["verified"]
    platforms = " · ".join(entry["platforms"])
    return (f'<span class="mo-verified">{label} {platforms} '
            f'<time datetime="{entry["date"]}">{entry["date"]}</time></span>')


def render_compat_table(cells, lang):
    labels = LABELS[lang]
    rows = [f"| {labels['platform']} | {labels['result']} | {labels['date']} |", "|---|---|---|"]
    ordered = sorted(cells, key=lambda c: (c["distro"], c["version"]))
    for cell in ordered:
        date = cell["date"] or "—"
        rows.append(f"| {DISTROS[cell['distro']]} {cell['version']} | {labels[cell['result']]} | {date} |")
    return "\n".join(rows)


def define_env(env):
    def lang():
        return env.conf["theme"]["language"] if env.conf["theme"]["language"] in LABELS else "en"

    @env.macro
    def verified(key):
        return render_verified(env.variables["verified"][key], lang())

    @env.macro
    def compat_table():
        return render_compat_table(env.variables["compatibility"]["cells"], lang())
