{% raw %}
# Helpers y Filtros de Twig

El motor Twig expone el puente phtml de MageObsidian como **funciones** Twig, y los escapers conscientes del contexto de Magento como **filtros**. Reflejan los métodos que ya usas en `.phtml`.

El bloque que renderiza se lee automáticamente del contexto de Twig, así que los renders anidados y recursivos cada uno apunta a su propio bloque —nunca le pasas `block` a estos helpers.

---

## Funciones

| Función | Mapea a | Devuelve |
|---|---|---|
| `render_vue(name, props = {})` | `renderVueComponent()` | Un marcador de [isla Vue](../components/modules/0105-vue-islands.md) (HTML seguro). |
| `child_html(alias = '', use_cache = true)` | `getChildHtml()` | El HTML de un bloque hijo (seguro). |
| `hero_icon(name, set = 'solid', size = '24')` | `getHeroIcon()` | Un SVG de Heroicons en línea (seguro). |
| `vite_url(path)` | `getViteFileUrl()` | URL de un archivo generado por Vite. |
| `component_path(name)` | `resolveComponentPath()` | URL resuelta de un componente por su nombre `Vendor::Component`. |
| `view_file_url(file_id, params = {})` | `getViewFileUrl()` | URL de un archivo de vista. |
| `json_ld(type, data = {})` | `renderJsonLd()` | Un `<script>` [JSON-LD de schema.org](../components/modules/0130-structured-data.md) para un tipo personalizado (HTML seguro). |

Los helpers que emiten markup (`render_vue`, `child_html`, `hero_icon`, `json_ld`) están marcados como seguros, así que el auto-escaping de Twig deja su HTML intacto. Los helpers de URL devuelven cadenas planas y se auto-escapan como cualquier valor.

> **Nota:** `render_vue`, `hero_icon`, `vite_url`, `component_path` y `json_ld` requieren que el bloque que renderiza extienda `MageObsidian\ModernFrontend\Block\Template`. Si un `.twig` lo renderiza un bloque no relacionado, el helper lanza un error accionable que nombra el método ausente. `child_html` y `view_file_url` funcionan en cualquier bloque de Magento.

### Ejemplos

```twig
{# Monta una isla Vue (hidratación perezosa, como el default de phtml) #}
{{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId(), featured: true }) }}

{# Renderiza un bloque hijo declarado en layout #}
{{ child_html('product.reviews') }}

{# Inserta un icono en línea #}
{{ hero_icon('shopping-cart', 'outline', '20') }}

{# Resuelve URLs #}
<link rel="stylesheet" href="{{ view_file_url('Acme_Catalog::css/extra.css') }}">
<script type="module" src="{{ vite_url('Acme_Catalog::js/widget') }}"></script>

{# Emite un tipo schema.org personalizado (@context/@type se añaden por ti) #}
{{ json_ld('FAQPage', { mainEntity: [{ '@type': 'Question', name: '¿P?', acceptedAnswer: { '@type': 'Answer', text: 'R.' } }] }) }}
```

> `render_vue` monta el componente con la estrategia `visible` (perezosa) por defecto. El montaje eager es un asunto de `.phtml`; si necesitas una isla por encima del pliegue, renderízala desde un `.phtml` con `$block->renderVueComponent($name, $props, true)`.

---

## Filtros

El escape de HTML ya es el default de Twig, así que no hay un filtro `escape_html` —basta con imprimir un valor. Los demás escapers conscientes del contexto reflejan el `$escaper->escape*` de Magento para los casos donde el escape de HTML es el contexto equivocado:

| Filtro | Mapea a | Úsalo para |
|---|---|---|
| `escape_url` | `escapeUrl()` | Un valor en un `href`/`src`. |
| `escape_html_attr` | `escapeHtmlAttr()` | Un valor en un atributo HTML. |
| `escape_js` | `escapeJs()` | Un valor inyectado en un contexto JS. |
| `escape_css` | `escapeCss()` | Un valor inyectado en un contexto CSS. |

### Ejemplos

```twig
<a href="{{ block.getLink() | escape_url }}">Detalles</a>

<div data-label="{{ label | escape_html_attr }}"></div>

<script>
    const term = "{{ query | escape_js }}";
</script>

<style>
    .promo { color: {{ brandColor | escape_css }}; }
</style>
```

---

## Referencias de Plantillas y Fallback

Las referencias entre plantillas `.twig` (`{% extends %}`, `{% include %}`) usan la misma notación `Vendor_Module::path.twig` que el resto del framework, resuelta mediante el fallback de temas de Magento. Un tema hijo puede sobrescribir el `.twig` de un padre exactamente como un `.phtml`:

```twig
{% extends 'Acme_Catalog::layout/base.twig' %}

{% block content %}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
{% endblock %}
```

---

## Próximos Pasos

- [Motor Twig](index.md) — instalación y cómo Twig coexiste con phtml.
- [Islas Vue](../components/modules/0105-vue-islands.md) — qué emite `render_vue` y cómo se hidrata.
{% endraw %}
