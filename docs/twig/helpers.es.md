{% raw %}
# Helpers y Filtros de Twig

El motor Twig expone el puente phtml de MageObsidian como **funciones** Twig, y los escapers conscientes del contexto de Magento como **filtros**. Reflejan los métodos que ya usas en `.phtml`.

El bloque que renderiza se lee automáticamente del contexto de Twig, así que los renders anidados y recursivos cada uno apunta a su propio bloque —nunca le pasas `block` a estos helpers.

---

## Funciones

| Función | Mapea a | Devuelve |
|---|---|---|
| `render_vue(name, props = {}, eager = false)` | `renderVueComponent()` | Un marcador de [isla Vue](../components/modules/0105-vue-islands.md) (HTML seguro). |
| `__(text, ...args)` | El `__()` de Magento | Texto traducido con sustitución de argumentos `%1`/`%2` (auto-escapado). |
| `child_html(alias = '', use_cache = true)` | `getChildHtml()` | El HTML de un bloque hijo (seguro). |
| `hero_icon(name, set = 'solid', size = '24')` | `getHeroIcon()` | Un SVG de Heroicons en línea (seguro). |
| `vite_url(path)` | `getViteFileUrl()` | URL de un archivo generado por Vite. |
| `component_path(name)` | `resolveComponentPath()` | URL resuelta de un componente por su nombre `Vendor::Component`. |
| `view_file_url(file_id, params = {})` | `getViewFileUrl()` | URL de un archivo de vista. |
| `json_ld(type, data = {})` | `renderJsonLd()` | Un `<script>` [JSON-LD de schema.org](../components/modules/0130-structured-data.md) para un tipo personalizado (HTML seguro). |
| `image(src, options = {})` | `renderImage()` | Un [`<img>`/`<picture>`](../components/modules/0140-images.md) amigable con CWV (HTML seguro). |

Los helpers que emiten markup (`render_vue`, `child_html`, `hero_icon`, `json_ld`, `image`) están marcados como seguros, así que el auto-escaping de Twig deja su HTML intacto. Los helpers de URL devuelven cadenas planas y se auto-escapan como cualquier valor.

> **Nota:** `render_vue`, `hero_icon`, `vite_url`, `component_path`, `json_ld` e `image` requieren que el bloque que renderiza extienda `MageObsidian\ModernFrontend\Block\Template`. Si un `.twig` lo renderiza un bloque no relacionado, el helper lanza un error accionable que nombra el método ausente. `child_html` y `view_file_url` funcionan en cualquier bloque de Magento; `__` es independiente del bloque.

### Helpers de formato

Una segunda extensión (`FormatExtension`) añade formato a nivel de framework, respaldado por servicios de Magento (no por el bloque, así que funcionan en cualquier `.twig`). Toda la salida es texto plano y se auto-escapa —ninguno está marcado como seguro. Cada uno tolera entrada `null`/vacía.

| Helper | Respaldado por | Uso |
|---|---|---|
| `value\|number` | `LocaleFormatter` | Agrupa un número según el locale de la tienda (`1234567` → `1,234,567`). |
| `date\|date_format(format = 'medium', part = 'date')` | `TimezoneInterface` | Fecha por locale/zona horaria. `format`: `short\|medium\|long\|full`; `part`: `date\|time\|datetime`. |
| `html\|strip_tags(allowed = null)` | `Filter\StripTags` | Quita el markup dejando texto plano. |
| `config(path, scope = 'store')` | `ScopeConfigInterface` | Un valor de configuración de tienda. |
| `url(route, params = {})` | `UrlInterface` | Una URL de framework para una ruta. |
| `media_url(path)` | base media de la tienda | Una URL bajo la base media de la tienda. |

El formato de comercio vive en el `PriceExtension` del módulo **storefront** (registrado en el motor vía DI — ver [Extender el motor](#extender-el-motor-twig)): `amount\|price(include_container = true)` y `amount\|currency(code = null)`, ambos `is_safe html` porque `PriceCurrency::format()` devuelve un `<span class="price">`.

### Ejemplos

```twig
{# Monta una isla Vue (hidratación perezosa por defecto) #}
{{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId(), featured: true }) }}

{# Monta eager una isla por encima del pliegue (header, trigger del mini-cart) #}
{{ render_vue('Acme_Theme::MiniCart', { count: block.getItemCount() }, true) }}

{# Traduce texto — %1/%2 se sustituyen, la salida se escapa #}
<span>{{ __('Items %1 to %2 of %3', first, last, total) }}</span>

{# Renderiza un bloque hijo declarado en layout #}
{{ child_html('product.reviews') }}

{# Inserta un icono en línea #}
{{ hero_icon('shopping-cart', 'outline', '20') }}

{# Resuelve URLs #}
<link rel="stylesheet" href="{{ view_file_url('Acme_Catalog::css/extra.css') }}">
<script type="module" src="{{ vite_url('Acme_Catalog::js/widget') }}"></script>

{# Emite un tipo schema.org personalizado (@context/@type se añaden por ti) #}
{{ json_ld('FAQPage', { mainEntity: [{ '@type': 'Question', name: '¿P?', acceptedAnswer: { '@type': 'Answer', text: 'R.' } }] }) }}

{# Formato #}
<span>{{ product.getFinalPrice()|price }}</span>
<span>{{ block.getTotalCount()|number }}</span>
<time>{{ order.getCreatedAt()|date_format('long') }}</time>
<a href="{{ url('customer/account') }}">{{ config('general/store_information/name') }}</a>
```

> `render_vue` monta el componente con la estrategia `visible` (perezosa) por defecto. Para una isla por encima del pliegue (header, trigger del mini-cart), pasa `true` como tercer argumento para montarla `eager` —reflejando `$block->renderVueComponent($name, $props, true)` en `.phtml`.

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

## Composición: includes, embeds y macros

Todas las referencias usan la notación `Vendor_Module::path.twig`, resuelta por el fallback de temas de Magento —así que un tema hijo sobrescribe cualquier partial/macro igual que un `.phtml`. Prefiere componer plantillas antes que copiar markup.

**`{% extends %}` + `{% block %}`** — una base con regiones sobrescribibles:

```twig
{% extends 'Acme_Catalog::layout/base.twig' %}
{% block content %}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
{% endblock %}
```

**`{% include %}` con `with`/`only`** — un partial parametrizado (`only` aísla el scope del partial):

```twig
{% include 'Acme_Catalog::partials/badge.twig' with { label: 'New', tone: 'accent' } only %}
```

**`{% embed %}` — el equivalente de slots en Twig.** Incluye una carcasa y rellena sus bloques en el sitio de llamada. Ideal para cards/secciones cuyo armazón es compartido pero el contenido varía:

```twig
{# Acme_Catalog::components/card.twig #}
<article class="card">
    {% block media %}{% endblock %}
    <div class="card__body">{% block body %}{% endblock %}</div>
</article>

{# sitio de llamada — rellena los slots #}
{% embed 'Acme_Catalog::components/card.twig' %}
    {% block media %}{{ image(product.getImage()) }}{% endblock %}
    {% block body %}<h3>{{ product.getName() }}</h3>{% endblock %}
{% endembed %}
```

**`{% macro %}` — fragmentos reutilizables sin pasar por layout.** Importa una vez, llama muchas:

```twig
{% from 'Magento_Theme::macros/ui.twig' import nav_list %}
<nav>{{ nav_list(block.getNavigation().getItems(), 'nav-link') }}</nav>
```

---

## ViewModels en Twig

Mantén la lógica de datos fuera de la plantilla: ponla en un ViewModel (`ArgumentInterface`), regístralo como `<argument>` del bloque en el layout, y léelo desde Twig con el getter mágico del bloque.

```xml
<referenceBlock name="header-content" template="Acme_Theme::html/header.twig">
    <arguments>
        <argument name="navigation" xsi:type="object">Acme\Theme\ViewModel\Navigation</argument>
    </arguments>
</referenceBlock>
```

```twig
{# el argumento `navigation` → block.getNavigation() #}
{% for item in block.getNavigation().getItems() %}
    <a href="{{ item.url|escape_url }}">{{ item.label }}</a>
{% endfor %}
```

El mismo ViewModel puede registrarse en varios bloques (header, footer, …) para compartir una sola fuente de verdad —sin datos duplicados en las plantillas.

---

## Extender el motor Twig

El entorno Twig compartido lo construye `EnvironmentFactory`, cuyo argumento array `extensions` **se mergea entre módulos por clave de item** —como el `engines` de `TemplateEngineFactory`. Cualquier módulo añade sus filtros/funciones registrando un `Twig\Extension\ExtensionInterface` en ese array, sin tocar el motor:

```xml
<!-- Acme_Catalog/etc/di.xml — scope GLOBAL, no etc/frontend (ver nota) -->
<type name="MageObsidian\ModernFrontendTwig\Model\Template\EnvironmentFactory">
    <arguments>
        <argument name="extensions" xsi:type="array">
            <item name="acme_catalog" xsi:type="object">Acme\Catalog\Twig\CatalogExtension</item>
        </argument>
    </arguments>
</type>
```

Así es exactamente como el `PriceExtension` del storefront añade `price`/`currency`.

> **Decláralo en scope global, no en `etc/frontend/di.xml`.** Los argumentos array se mergean acumulativamente *dentro* de un scope, pero un scope de área **reemplaza** un array global en vez de mergear —lo que descartaría las extensiones del propio motor en el frontend. La extensión solo se instancia al construir el entorno (frontend), así que una declaración global es inerte en otros lados. Los nombres de filtro/función son un namespace compartido; prefija los de terceros para evitar colisiones (gana el último).

---

## Próximos Pasos

- [Motor Twig](index.md) — instalación y cómo Twig coexiste con phtml.
- [Islas Vue](../components/modules/0105-vue-islands.md) — qué emite `render_vue` y cómo se hidrata.
{% endraw %}
