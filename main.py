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


LANE_LABELS = {
    "en": {"now": "Now", "next": "Next", "later": "Later", "upcoming": "Next"},
    "es": {"now": "Ahora", "next": "Siguiente", "later": "Después", "upcoming": "Siguiente"},
}


def render_timeline(milestones, lang):
    parts = ['<ol class="mo-timeline">']
    for m in milestones:
        state = "now" if m["now"] else ("next" if m["date"] is None else "done")
        css = "mo-ms" if state == "done" else f"mo-ms mo-ms--{state}"
        when = (f'<time datetime="{m["date"]}">{m["date"]}</time>' if m["date"]
                else LANE_LABELS[lang]["upcoming"])
        version = f' <span class="mo-ver">{m["version"]}</span>' if m["version"] else ""
        title = m[lang]["title"]
        heading = f'<a href="{m["link"]}">{title}</a>' if m["link"] else title
        parts.append(f'<li class="{css}"><span class="mo-date">{when}</span>'
                     f'<strong>{heading}</strong>{version}<p>{m[lang]["text"]}</p></li>')
    parts.append("</ol>")
    return "".join(parts)


def render_lanes(lanes, lang):
    parts = ['<div class="mo-lanes">']
    for lane in lanes:
        parts.append(f'<section class="mo-lane mo-lane--{lane["key"]}"><h3>{LANE_LABELS[lang][lane["key"]]}</h3>')
        for item in lane["items"]:
            parts.append(f'<div class="mo-item"><strong>{item[lang]["title"]}</strong><p>{item[lang]["text"]}</p>')
            if item["progress"] is not None:
                measure = item[f"measure_{lang}"]
                parts.append(f'<div class="mo-bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" '
                             f'aria-valuenow="{item["progress"]}" aria-label="{measure}">'
                             f'<i style="width:{item["progress"]}%"></i></div><small>{measure}</small>')
            parts.append("</div>")
        parts.append("</section>")
    parts.append("</div>")
    return "".join(parts)


def define_env(env):
    def lang():
        return env.conf["theme"]["language"] if env.conf["theme"]["language"] in LABELS else "en"

    @env.macro
    def verified(key):
        return render_verified(env.variables["verifications"][key], lang())

    @env.macro
    def compat_table():
        return render_compat_table(env.variables["compatibility"]["cells"], lang())

    @env.macro
    def timeline():
        return render_timeline(env.variables["milestones"], lang())

    @env.macro
    def roadmap_lanes():
        return render_lanes(env.variables["lanes"], lang())
