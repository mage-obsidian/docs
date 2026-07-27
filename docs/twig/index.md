{% raw %}
# Twig Engine

**MageObsidian** ships with a [Twig](https://twig.symfony.com/) template engine that runs **alongside** Magento's native `.phtml`. It comes **included by default** with the components install — you do not opt in. It is delivered as its own module, so you can turn it off without affecting anything else.

> **Included by default, never mandatory, fully backward-compatible.** Twig ships with the install but nothing forces you — or third-party modules/themes — to use it: `.phtml` keeps working untouched, and adopting Twig is never a migration. `.twig` and `.phtml` coexist in the same theme, the theme fallback works identically for both. You can write `.twig` one template at a time, only `.phtml`, or [disable the engine entirely](#disabling-twig).

---

## Why Twig

Twig is positioned honestly as a **developer-experience** improvement for the server-side template shell — not a frontend performance feature. The page that reaches the browser is identical whether the shell was a `.phtml` or a `.twig`; both compile to PHP and run on the server.

What Twig gives you over raw `.phtml`:

- **HTML auto-escaping by default** — the main security gain. Output is escaped unless you explicitly mark it safe.
- **Clean template inheritance** (`{% extends %}`, `{% block %}`, `{% include %}`) with the familiar Twig syntax.
- **A restricted surface** — templates express presentation, not arbitrary PHP.
- **First-class IDE support** for the Twig language.

Frontend performance still comes from the [Vue islands](../components/modules/0105-vue-islands.md) architecture, which a `.twig` template drives exactly like a `.phtml` (via the `render_vue` helper).

---

## How It Coexists With phtml

Magento dispatches a template to an engine **by its file extension** (`Magento\Framework\View\Element\Template::fetchView`). The native engine is registered for `phtml`; this module registers one more entry for `twig`:

- A block whose `template="…​.twig"` is rendered by Twig.
- A block whose `template="…​.phtml"` keeps using the native PHP engine.
- The `engines` map is an array argument that **merges across modules**, so this only *adds* `twig` — it never replaces `phtml`.

Theme fallback is unchanged: Magento resolves a template by path, agnostic to its extension, so a child theme overrides a parent's `.twig` exactly the way it overrides a `.phtml`.

---

## Installation

Nothing to install. The `mage-obsidian/module-modern-frontend-twig` module is a dependency of `mage-obsidian/component-modern-frontend`, so `composer require mage-obsidian/component-modern-frontend` (the standard [installation](../getting-started/installation.md)) already pulls it in. It brings `twig/twig ^3.12` along.

## Disabling Twig

Twig is a normal Magento module, so disabling it is a one-liner — `.phtml` keeps working exactly as before:

```bash
bin/magento module:disable MageObsidian_ModernFrontendTwig
bin/magento setup:upgrade
```

After this, the `.twig` extension is no longer registered as an engine. Re-enable it any time with `bin/magento module:enable MageObsidian_ModernFrontendTwig`. There is no feature flag — the module's enabled state *is* the switch.

---

## A First Template

A `.twig` template renders within the context of its Magento block. Unlike `.phtml`, there is no implicit `$this`; the block is exposed as the `block` variable:

```twig
{# view/frontend/templates/example.twig #}
<section class="example">
    <h1>{{ block.getTitle() }}</h1>

    {# Mount a Vue island, exactly like phtml's renderVueComponent #}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
</section>
```

Wire it from layout with any block — for the MageObsidian helpers (`render_vue`, `hero_icon`, …) use a block extending `MageObsidian\ModernFrontend\Block\Template`:

```xml
<referenceContainer name="content">
    <block class="MageObsidian\ModernFrontend\Block\Template"
           name="acme.example"
           template="Acme_Catalog::example.twig"/>
</referenceContainer>
```

---

## Caching

Twig compiles each template to a PHP class the first time it is rendered. Those classes are a real Magento cache type, **Twig Templates** (`twig_templates`), so they show up in `bin/magento cache:status` and in the admin's Cache Management grid alongside every other type:

```bash
bin/magento cache:clean twig_templates   # rebuild the compiled templates
bin/magento cache:flush                  # includes them, like every other type
bin/magento cache:disable twig_templates # compile on every request
```

Disabling the type is the supported way to debug a template that seems stuck — nothing is written to disk and every request recompiles. Expect a noticeably slower response while it is off.

You should never have to clear this cache after a deploy. The compiled classes live in a directory keyed by the installed package set, so a `composer install` or `composer update` starts from a clean namespace and the previous build's files are pruned. Templates edited in place are picked up from their modification time. Both mechanisms are needed: Composer preserves the packaged modification times, so a package installed today can carry files dated weeks ago — older than the cache built from its previous version.

In **developer mode** `{{ dump() }}` is available and an undefined variable raises an error (`strict_variables`) instead of rendering as an empty string. HTML auto-escaping is always on, in every mode.

---

## Next Steps

- [Helpers & Filters](helpers.md) — the full reference of MageObsidian Twig functions and escaping filters.
- [Vue Islands](../components/modules/0105-vue-islands.md) — how `render_vue` mounts components.
{% endraw %}
