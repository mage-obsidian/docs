{% raw %}
# Twig Helpers & Filters

The Twig engine exposes the MageObsidian phtml bridge as Twig **functions**, and Magento's context-aware escapers as **filters**. They mirror the methods you already use in `.phtml`.

The rendering block is read from the Twig context automatically, so nested and recursive renders each address their own block — you never pass `block` to these helpers.

---

## Functions

| Function | Maps to | Returns |
|---|---|---|
| `render_vue(name, props = {})` | `renderVueComponent()` | A [Vue island](../components/modules/0105-vue-islands.md) marker (safe HTML). |
| `child_html(alias = '', use_cache = true)` | `getChildHtml()` | A child block's HTML (safe). |
| `hero_icon(name, set = 'solid', size = '24')` | `getHeroIcon()` | An inline Heroicons SVG (safe). |
| `vite_url(path)` | `getViteFileUrl()` | URL of a Vite-generated file. |
| `component_path(name)` | `resolveComponentPath()` | Resolved URL of a component by its `Vendor::Component` name. |
| `view_file_url(file_id, params = {})` | `getViewFileUrl()` | URL of a view file. |
| `json_ld(type, data = {})` | `renderJsonLd()` | A [schema.org JSON-LD](../components/modules/0130-structured-data.md) `<script>` for a custom type (safe HTML). |
| `image(src, options = {})` | `renderImage()` | A CWV-friendly [`<img>`/`<picture>`](../components/modules/0140-images.md) (safe HTML). |

The markup-emitting helpers (`render_vue`, `child_html`, `hero_icon`, `json_ld`, `image`) are flagged safe, so Twig's auto-escaping leaves their HTML intact. The URL helpers return plain strings and are auto-escaped like any value.

> **Note:** `render_vue`, `hero_icon`, `vite_url`, `component_path`, `json_ld` and `image` require the rendering block to extend `MageObsidian\ModernFrontend\Block\Template`. If a `.twig` is rendered by an unrelated block, the helper raises an actionable error naming the missing method. `child_html` and `view_file_url` work on every Magento block.

### Examples

```twig
{# Mount a Vue island (lazy-hydrated, like phtml's default) #}
{{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId(), featured: true }) }}

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
```

> `render_vue` mounts the component with the default `visible` (lazy) strategy. Eager mounting is a `.phtml` concern; if you need an above-the-fold island, render it from a `.phtml` with `$block->renderVueComponent($name, $props, true)`.

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

## Template References & Fallback

References between `.twig` templates (`{% extends %}`, `{% include %}`) use the same `Vendor_Module::path.twig` notation as the rest of the framework, resolved through Magento's theme fallback. A child theme can override a parent's `.twig` exactly like a `.phtml`:

```twig
{% extends 'Acme_Catalog::layout/base.twig' %}

{% block content %}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
{% endblock %}
```

---

## Next Steps

- [Twig Engine](index.md) — installation and how Twig coexists with phtml.
- [Vue Islands](../components/modules/0105-vue-islands.md) — what `render_vue` emits and how it hydrates.
{% endraw %}
