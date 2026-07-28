{% raw %}
# Twig Helpers & Filters

The Twig engine exposes the MageObsidian phtml bridge as Twig **functions**, and Magento's context-aware escapers as **filters**. They mirror the methods you already use in `.phtml`.

The rendering block is read from the Twig context automatically, so nested and recursive renders each address their own block — you never pass `block` to these helpers.

---

## Functions

| Function | Maps to | Returns |
|---|---|---|
| `render_vue(name, props = {}, eager = false, server_html = '', hydrate = false)` | `renderVueComponent()` | A [Vue island](../components/modules/0105-vue-islands.md) marker (safe HTML). |
| `__(text, ...args)` | Magento's `__()` | Translated text with `%1`/`%2` argument substitution (auto-escaped). |
| `child_html(alias = '', use_cache = true)` | `getChildHtml()` | A child block's HTML (safe). |
| `hero_icon(name, set = 'solid', size = '24', class = '')` | `getHeroIcon()` | A Heroicons `<svg>` (safe). |
| `vite_url(path)` | `getViteFileUrl()` | URL of a Vite-generated file. |
| `component_path(name)` | `resolveComponentPath()` | Resolved URL of a component by its `Vendor::Component` name. |
| `view_file_url(file_id, params = {})` | `getViewFileUrl()` | URL of a view file. |
| `json_ld(type, data = {})` | `renderJsonLd()` | A [schema.org JSON-LD](../components/modules/0130-structured-data.md) `<script>` for a custom type (safe HTML). |
| `image(src, options = {})` | `renderImage()` | A CWV-friendly [`<img>`/`<picture>`](../components/modules/0140-images.md) (safe HTML). |

The markup-emitting helpers (`render_vue`, `child_html`, `hero_icon`, `json_ld`, `image`) are flagged safe, so Twig's auto-escaping leaves their HTML intact. The URL helpers return plain strings and are auto-escaped like any value.

Twig supports named arguments, which is worth using once a call reaches the tail of `render_vue`'s signature:

```twig
{{ render_vue('Acme_Catalog::BuyBox', props, true, server_html, hydrate = true) }}
```

> **Note:** `render_vue`, `hero_icon`, `vite_url`, `component_path`, `json_ld` and `image` require the rendering block to extend `MageObsidian\ModernFrontend\Block\Template`. If a `.twig` is rendered by an unrelated block, the helper raises an actionable error naming the missing method. `child_html` and `view_file_url` work on every Magento block; `__` is block-independent.

### Formatting helpers

A second extension (`FormatExtension`) adds framework-level formatting backed by Magento services (not by the rendering block, so these work in any `.twig`). All output is plain text and is auto-escaped — none are flagged safe. Each tolerates `null`/empty input.

| Helper | Backed by | Use |
|---|---|---|
| `value\|number` | `LocaleFormatter` | Group a number per the store locale (`1234567` → `1,234,567`). |
| `date\|date_format(format = 'medium', part = 'date')` | `TimezoneInterface` | Locale/timezone date. `format`: `short\|medium\|long\|full`; `part`: `date\|time\|datetime`. |
| `html\|strip_tags(allowed = null)` | `Filter\StripTags` | Strip markup to plain text. |
| `config(path, scope = 'store')` | `ScopeConfigInterface` | A store-config value. |
| `url(route, params = {})` | `UrlInterface` | A framework URL for a route. |
| `media_url(path)` | store media base | A URL under the store's media base. |

Commerce formatting lives in the **storefront** module's `PriceExtension` (registered on the engine via DI — see [Extending the engine](#extending-the-twig-engine)): `amount\|price(include_container = true)` and `amount\|currency(code = null)`, both `is_safe html` because `PriceCurrency::format()` returns a `<span class="price">`.

### Examples

```twig
{# Mount a Vue island (lazy-hydrated by default) #}
{{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId(), featured: true }) }}

{# Eager-mount an above-the-fold island (header, mini-cart trigger) #}
{{ render_vue('Acme_Theme::MiniCart', { count: block.getItemCount() }, true) }}

{# Translate text — %1/%2 are substituted, output is escaped #}
<span>{{ __('Items %1 to %2 of %3', first, last, total) }}</span>

{# Render a child block declared in layout #}
{{ child_html('product.reviews') }}

{# Inline an icon #}
{{ hero_icon('shopping-cart', 'outline', '20') }}

{# Resolve URLs #}
<link rel="stylesheet" href="{{ view_file_url('Acme_Catalog::css/extra.css') }}">
<script type="module" src="{{ vite_url('Acme_Catalog::js/widget') }}"></script>

{# Emit a custom schema.org type (@context/@type added for you) #}
{{ json_ld('FAQPage', { mainEntity: [{ '@type': 'Question', name: 'Q?', acceptedAnswer: { '@type': 'Answer', text: 'A.' } }] }) }}

{# CWV-friendly image; width/height auto-detected for Vendor::path assets #}
{{ image('Acme_Catalog::images/hero.jpg', { alt: 'Hero', fetchpriority: 'high' }) }}

{# Formatting #}
<span>{{ product.getFinalPrice()|price }}</span>
<span>{{ block.getTotalCount()|number }}</span>
<time>{{ order.getCreatedAt()|date_format('long') }}</time>
<a href="{{ url('customer/account') }}">{{ config('general/store_information/name') }}</a>
```

> `render_vue` mounts the component with the default `visible` (lazy) strategy. For an above-the-fold island (header, mini-cart trigger), pass `true` as the third argument to mount it `eager`ly — mirroring `$block->renderVueComponent($name, $props, true)` in `.phtml`.

---

## Filters

HTML escaping is already Twig's default, so there is no `escape_html` filter — just output a value. The remaining context-aware escapers mirror Magento's `$escaper->escape*` for the cases where HTML escaping is the wrong context:

| Filter | Maps to | Use for |
|---|---|---|
| `escape_url` | `escapeUrl()` | A value placed in an `href`/`src`. |
| `escape_html_attr` | `escapeHtmlAttr()` | A value placed in an HTML attribute. |
| `escape_js` | `escapeJs()` | A value injected into a JS context. |
| `escape_css` | `escapeCss()` | A value injected into a CSS context. |

### Examples

```twig
<a href="{{ block.getLink() | escape_url }}">Details</a>

<div data-label="{{ label | escape_html_attr }}"></div>

<script>
    const term = "{{ query | escape_js }}";
</script>

<style>
    .promo { color: {{ brandColor | escape_css }}; }
</style>
```

---

## Naming a template: namespaces

A template reference can be written as `Vendor_Module::path.twig`, or with a namespace: `@catalog/path.twig`. Both resolve through Magento's theme fallback, so a child theme overrides any of them exactly like a `.phtml`.

Namespaces are derived from the enabled module list rather than declared, so there is nothing to register:

| Module | Always | Also, while no other module claims it |
|---|---|---|
| `Magento_Catalog` | `@magento-catalog` | `@catalog` |
| `MageObsidian_Storefront` | `@mage-obsidian-storefront` | `@storefront` |

The vendor-qualified form never collides and never changes, so it is the one a template can rely on unconditionally. The short form is the convenience.

When two vendors ship the same module name, the tie goes to whichever of them actually contains templates — `MageObsidian_Catalog` extends `Magento_Catalog` with code and JS but ships no `view/*/templates`, so `@catalog` is the core module's. A tie neither or both can break is left unregistered rather than decided silently; declare it in `di.xml` to settle it:

```xml
<type name="MageObsidian\ModernFrontendTwig\Model\Template\TemplateNamespaces">
    <arguments>
        <argument name="namespaces" xsi:type="array">
            <item name="catalog" xsi:type="string">MageObsidian_Catalog</item>
        </argument>
    </arguments>
</type>
```

`bin/magento mage-obsidian:twig:namespaces` prints the resolved table and flags the short names lost to a collision. An unknown namespace fails at load time with the closest matches suggested.

---

## Composition: includes, embeds & macros

Prefer composing templates over copy-pasting markup.

**`{% extends %}` + `{% block %}`** — a base layout with overridable regions:

```twig
{% extends 'Acme_Catalog::layout/base.twig' %}
{% block content %}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
{% endblock %}
```

**`@parent` — extend the template you are overriding.** A theme override cannot `{% extends %}` its own name: the fallback resolves it right back to the override and Twig recurses. `@parent` is the copy one level up the chain — the parent theme's, or the module's if there is none:

```twig
{# app/design/frontend/Acme/child/Magento_Theme/templates/html/header.twig #}
{% extends '@parent' %}

{% block nav %}
    {{ parent() }}
    <a href="/outlet">Outlet</a>
{% endblock %}
```

Each copy resolves its own level, so a three-theme chain works: the child extends the parent's, the parent extends the base's, the base extends the module's. In a module template it is an error — nothing is above it.

**`{% include %}` with `with`/`only`** — a parameterized partial (the `only` keeps the partial's scope isolated):

```twig
{% include '@catalog/partials/badge.twig' with { label: 'New', tone: 'accent' } only %}
```

!!! warning "`only` drops `block` too"
    `render_vue`, `hero_icon`, `image` and `json_ld` all read the rendering block from the context. A partial included with `only` does not inherit it, so pass it through — `with { block: block, … } only` — or the helper raises an error saying exactly this.

**`{% embed %}` — the Twig equivalent of slots.** Include a shell and fill its blocks at the call site. Ideal for cards/sections whose chrome is shared but whose contents vary:

```twig
{# Acme_Catalog::components/card.twig #}
<article class="card">
    {% block media %}{% endblock %}
    <div class="card__body">{% block body %}{% endblock %}</div>
</article>

{# call site — fills the slots #}
{% embed 'Acme_Catalog::components/card.twig' %}
    {% block media %}{{ image(product.getImage()) }}{% endblock %}
    {% block body %}<h3>{{ product.getName() }}</h3>{% endblock %}
{% endembed %}
```

**`{% macro %}` — reusable fragments without a layout round-trip.** Import once, call many times:

```twig
{% from 'Magento_Theme::macros/ui.twig' import nav_list %}
<nav>{{ nav_list(block.getNavigation().getItems(), 'nav-link') }}</nav>
```

---

## ViewModels in Twig

Keep data logic out of templates: put it in a ViewModel (`ArgumentInterface`), register it as a block `<argument>` in layout, and read it from Twig via the block's magic getter.

```xml
<referenceBlock name="header-content" template="Acme_Theme::html/header.twig">
    <arguments>
        <argument name="navigation" xsi:type="object">Acme\Theme\ViewModel\Navigation</argument>
    </arguments>
</referenceBlock>
```

```twig
{# the argument name `navigation` → block.getNavigation() #}
{% for item in block.getNavigation().getItems() %}
    <a href="{{ item.url|escape_url }}">{{ item.label }}</a>
{% endfor %}
```

The same ViewModel can be registered on several blocks (header, footer, …) so they share one source of truth — no duplicated data in templates.

---

## Extending the Twig engine

The shared Twig environment is built by `EnvironmentFactory`, whose `extensions` array argument **merges across modules by item key** — like `TemplateEngineFactory`'s `engines`. Any module adds its own filters/functions by registering a `Twig\Extension\ExtensionInterface` on that array, without editing the engine:

```xml
<!-- Acme_Catalog/etc/di.xml — GLOBAL scope, not etc/frontend (see note) -->
<type name="MageObsidian\ModernFrontendTwig\Model\Template\EnvironmentFactory">
    <arguments>
        <argument name="extensions" xsi:type="array">
            <item name="acme_catalog" xsi:type="object">Acme\Catalog\Twig\CatalogExtension</item>
        </argument>
    </arguments>
</type>
```

This is exactly how the storefront's `PriceExtension` adds `price`/`currency`.

> **Declare it at global scope, not `etc/frontend/di.xml`.** Array arguments merge cumulatively *within* a scope, but an area scope **replaces** a global array instead of merging — which would drop the engine's own extensions in the frontend. The extension is only instantiated when the (frontend) environment is built, so a global declaration is inert elsewhere. Filter/function names are a shared namespace; prefix third-party names to avoid collisions (last one wins).

---

## Next Steps

- [Twig Engine](index.md) — installation and how Twig coexists with phtml.
- [Vue Islands](../components/modules/0105-vue-islands.md) — what `render_vue` emits and how it hydrates.
{% endraw %}
