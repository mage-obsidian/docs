{% raw %}
# SEO y metadata del head

**MageObsidian** completa la metadata del head que Magento deja vacía: una URL canónica en cada página, propiedades de Open Graph y Twitter Card, una meta description derivada de la propia página, las directivas modernas de robots y un Web App Manifest. Todo se renderiza en el servidor dentro del HTML cacheado —sin JavaScript adicional, sin nada calculado en el navegador.

La metadata vive en `MageObsidian_Storefront` y se escribe a través del propio `Page\Config` de Magento, así que el escapeo y el render los hace el core. Cada pieza es un interruptor: una tienda que ya usa una extensión de SEO apaga la mitad que se duplica.

---

## Nota de actualización: el head ahora incluye el asset collection de la página

Hasta esta versión el template raíz del tema imprimía solo `headContent` y `headAdditional`. Nunca imprimía **`headAssets`**, que es lo único que renderiza el page asset collection de Magento.

Todo lo que pasa por `Page\Config::addPageAsset()` / `addRemotePageAsset()` se generaba, se guardaba… y se descartaba en silencio. Eso incluía:

- la **canónica** que el core emite en páginas de catálogo (con `catalog/seo/*_canonical_tag` activado),
- los **`<link rel="icon">` / `<link rel="shortcut icon">`** nativos,
- el **`<link rel="alternate">`** del RSS,
- y lo que el merchant hubiera configurado en **Design → HTML Head → Scripts and Style Sheets**.

`root.phtml` ahora lo imprime. Es un arreglo, pero **cambia lo que emite en su head una tienda existente**, así que conviene planificar la actualización sabiéndolo: medido en el demo de este proyecto, agrega cuatro etiquetas y entre 448 y 530 bytes por página. Ni RequireJS, ni jQuery, ni CSS de Luma: esos pipelines ya están excluidos de los temas Obsidian, así que el collection simplemente no los contiene.

Lo único que conviene revisar antes de desplegar es el último punto de esa lista: si `design/head/includes` tiene algo cargado, **ahora se está sirviendo y antes no**. Lee la sección [Head includes](#head-includes-nativo-de-magento-y-render-blocking) antes de dar por hecho que eso sale gratis.

---

## URL canónica

Magento solo emite una canónica en páginas de catálogo, y solo con los flags de SEO de catálogo activados. Las páginas CMS, la home y los resultados de búsqueda no reciben ninguna. MageObsidian la emite **en toda página que no tenga una ya**.

Una canónica puesta por el core o por otra extensión **nunca se sobrescribe**. El módulo revisa primero el page asset collection; si ya hay una canónica reclamada, no escribe nada.

### Parámetros de query: una lista de permitidos

Todo lo que no está en la lista se descarta, parámetros de tracking incluidos. El valor por defecto es `p,q`:

- **`p`** se conserva porque un listado paginado tiene que apuntarse a sí mismo. Si la página 2 canonicaliza hacia la 1, los productos a los que solo se llega desde la página 2 salen del índice.
- **`q`** se conserva porque sin él todos los resultados de búsqueda canonicalizan hacia la misma URL vacía.

Se usa una lista de permitidos y no una de bloqueados porque una lista de bloqueados envejece: hoy es `utm_*`, `gclid` y `fbclid`; mañana es otra cosa.

También se descarta el parámetro de paginación cuando vale `1`, y cualquier parámetro permitido con valor vacío, así que `?p=1` nunca genera una segunda URL para la primera página.

```
/gear/bags.html?p=2&color=Blue&utm_source=nl   →   /gear/bags.html?p=2
/catalogsearch/result/?q=bag&p=1               →   /catalogsearch/result?q=bag
```

### Sufijo de URL y la barra final

El path se normaliza sin su barra final, porque Magento responde `200` tanto en `/about-us` como en `/about-us/`: dejar las dos significaría dos URLs indexables para una misma página.

La excepción es una tienda cuyo `catalog/seo/category_url_suffix` o `catalog/seo/product_url_suffix` **sea** `/`. Ahí la barra es parte de la dirección, así que el path se deja tal cual.

### Configuración

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Emit a Canonical URL | `mage_obsidian/seo/canonical_enabled` | `1` |
| Query Parameters Kept in the Canonical | `mage_obsidian/seo/canonical_query_params` | `p,q` |

**Stores → Configuration → MageObsidian → SEO**.

```bash
# Hacer que la paginación y los resultados de búsqueda colapsen en una sola URL
bin/magento config:set mage_obsidian/seo/canonical_query_params ""
```

---

## Open Graph y Twitter Card

Con la metadata social activada, el head lleva lo siguiente, derivado del título, la descripción y las imágenes de la propia página:

| Propiedad | Origen |
|---|---|
| `og:type` | `product` en una ficha de producto, `website` en el resto |
| `og:site_name` | nombre de la tienda |
| `og:locale` | `general/locale/code` |
| `og:title` | el título de la página |
| `og:description` | la meta description de la página |
| `og:url` | la canónica resuelta —incluida una puesta por el core |
| `og:image` | la imagen de la entidad, luego la imagen social de respaldo, luego el logo de la tienda |
| `twitter:card` | `summary_large_image` |
| `twitter:site` | la cuenta configurada; se omite si está vacía |
| `twitter:title` / `twitter:description` / `twitter:image` | igual que arriba |

`og:url` usa deliberadamente la canónica **resuelta** y no la propia del módulo: si el core canonicaliza una ficha de producto hacia una URL, la URL que se comparte tiene que ser esa misma.

### Complementa, no duplica

En una ficha de producto, `MageObsidian_Catalog` ya emite su propio bloque de Open Graph (`opengraph.general`, desde el view model `ProductOpenGraph`): `og:type`, `og:title`, `og:url`, `og:image`, `og:description` y el par `product:price:*`.

En lugar de fijar esa lista en el código, el módulo **le pregunta al bloque qué emite**. Un mapa en di.xml asocia el nombre de un bloque con el argumento de layout que contiene su view model, y al objeto se le consulta mediante `getProperties()`; lo que ese bloque reclame se le deja a él:

```xml
<type name="MageObsidian\Storefront\Model\Seo\ClaimedSocialProperties">
    <arguments>
        <argument name="claimants" xsi:type="array">
            <item name="opengraph.general" xsi:type="string">open_graph</item>
        </argument>
    </arguments>
</type>
```

Si mañana ese bloque suma una propiedad, la detección se ajusta sola. Una tienda con una extensión de SEO de terceros agrega una línea aquí y sus propiedades tampoco se duplican.

### Configuración

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Emit Open Graph and Twitter Card Metadata | `mage_obsidian/seo/social_meta_enabled` | `1` |
| Fallback Share Image | `mage_obsidian/seo/social_image` | vacío (cae al logo de la tienda) |
| Twitter Account | `mage_obsidian/seo/twitter_site` | vacío (`twitter:site` se omite) |

La imagen social de respaldo debería ser de 1200×630 o mayor.

---

## Meta description

Magento repite la descripción por defecto de la tienda en cada página que no tiene una propia. Con el fallback activado, el módulo la reemplaza por algo referido a la página real:

1. gana la meta description propia de la entidad;
2. si no la hay, se resume su contenido: se quita el HTML (`<script>` y `<style>` con su contenido, y también las directivas `{{...}}` de Page Builder), se colapsan los espacios y se corta en un borde de palabra alrededor de los 160 caracteres;
3. si la página ya trae algo específico —otra extensión, un handle de layout—, no se toca.

El módulo solo interviene cuando la página está **repitiendo el valor por defecto de la tienda**, y la comparación se hace sobre el texto normalizado, así que el escapeo HTML que aplica `setMetadata()` no la invalida.

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Derive the Meta Description from the Page | `mage_obsidian/seo/meta_description_fallback` | `1` |

---

## Meta robots

Magento escribe `INDEX,FOLLOW` y ahí se detiene. El módulo agrega las tres directivas que controlan cuánto puede mostrar un buscador de la página:

```html
<meta name="robots" content="INDEX,FOLLOW,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
```

Dos reglas lo mantienen seguro:

- **Una página `NOINDEX` no se toca nunca.** La extensión se detiene apenas ve la directiva, así que una página que debe quedar fuera del índice permanece exactamente como la escribió Magento.
- **Solo escribe cuando realmente agrega algo.** Una directiva ya presente no se repite, y cuando no hay nada que sumar el valor queda intacto.

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Extra Robots Directives | `mage_obsidian/seo/robots_directives` | `max-image-preview:large,max-snippet:-1,max-video-preview:-1` |

Vacía el campo para dejar el meta robots exactamente como lo escribió Magento.

---

## Web App Manifest

El manifest se deriva de la configuración de la tienda —nombre, base URL, logo, favicon, colores—, así que lo sirve un controller en vez de ser un archivo estático, y varía por vista de tienda.

**Endpoint:** `/mage-obsidian-storefront/manifest/`, enlazado desde el head con `<link rel="manifest">`.

```bash
curl -i https://store.example/mage-obsidian-storefront/manifest/
```

```
HTTP/1.1 200 OK
Content-Type: application/manifest+json
Cache-Control: max-age=86400, public

{"name":"Main Website Store","short_name":"Main Website","start_url":"https://store.example/",
 "scope":"https://store.example/","display":"standalone","theme_color":"#ffffff","background_color":"#ffffff"}
```

Detalles que conviene conocer:

- El media type es `application/manifest+json`, no `application/json`.
- Es cacheable por un día para el navegador, la CDN y Varnish. El full page cache de Magento no lo alcanza —solo cubre resultados `Result\Page`—, así que acá el mecanismo son las cabeceras HTTP.
- `icons` aparece en cuanto haya un logo o un favicon configurado; sin ninguno de los dos, la propiedad se omite en lugar de emitirse vacía.
- Apagado, el endpoint responde **404**, no un manifest vacío, y ese `404` no se anuncia como cacheable por un día.

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Serve a Web App Manifest | `mage_obsidian/seo/manifest_enabled` | `1` |
| Manifest Display Mode | `mage_obsidian/seo/manifest_display` | `standalone` |
| Manifest Theme Colour | `mage_obsidian/seo/manifest_theme_color` | `#ffffff` |
| Manifest Background Colour | `mage_obsidian/seo/manifest_background_color` | `#ffffff` |

---

## Head includes: nativo de Magento, y render-blocking

**Design → HTML Head → Scripts and Style Sheets** (`design/head/includes`) es una capacidad **nativa de Magento**. Lo que se pegue ahí se inserta tal cual en el `<head>`, en todas las páginas de la vista de tienda.

### Todo lo que va en ese campo es render-blocking

Esta es la parte que se subestima:

- un `<script src>` sin `async` ni `defer` **frena el parseo del HTML** hasta que se descarga, se parsea y se ejecuta;
- un `<link rel="stylesheet">` **bloquea el primer render** hasta que la hoja llega.

En un stack que mide FCP y LCP en milisegundos, un solo tag de terceros en ese campo puede costar más que todo el resto de la página. Es el único lugar del admin donde un merchant puede deshacer el presupuesto entero de frontend con un pegado.

### El framework no lo reescribe

Ese campo es contenido del merchant sobre un contrato nativo de Magento, y quien lo pega es responsable de lo que hace. MageObsidian no lo toca. **Los dos flags de abajo vienen apagados**, así que recién instalado el comportamiento es exactamente el de Magento.

Existen dos flags opt-in para quien haya mirado su propio contenido y haya decidido:

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Defer Scripts In Head Includes | `mage_obsidian/head/includes_defer_scripts` | `0` |
| Defer Stylesheets In Head Includes | `mage_obsidian/head/includes_defer_styles` | `0` |

**Stores → Configuration → MageObsidian → Frontend → HTML Head Includes**.

### Diferir scripts, y cuándo no conviene

Con el flag activado, un `<script src>` externo recibe `defer`. Las etiquetas con `async`, `defer` o `type="module"` ya no son bloqueantes y se dejan intactas; **un script inline no se toca nunca**, porque no hay forma segura de diferirlo y puede ser justamente lo que tiene que correr primero.

**No enciendas esto si el campo contiene un tag que necesita correr bloqueando.** Los dos casos habituales viven en ese mismo campo:

- **Scripts anti-flicker de A/B testing.** Diferidos, provocan exactamente el parpadeo del contenido original que existen para evitar.
- **Gestores de consentimiento.** Diferidos, el banner llega después de la página —y después de los tags que debía condicionar.

#### La regla posicional

Un script externo se difiere **solo si no hay ningún `<script>` inline después de él en el mismo campo**. El snippet canónico de analytics es un par:

```html
<script src="https://cdn.example/lib.js"></script>
<script>lib.init()</script>
```

Un script diferido corre *después* de que se parsea el documento, así que correría después de esa llamada inline: `lib` todavía no existiría y la página se rompería. La regla es posicional, no global:

```html
<script src="a.js"></script>      <!-- no se difiere: hay un inline después -->
<script>a.init()</script>
<script src="b.js"></script>      <!-- se difiere: no hay ningún inline después -->
```

**Esa comprobación solo ve este campo.** Si un script inline de una plantilla, de otro módulo o de un widget de Page Builder depende de un script pegado aquí, el framework no tiene forma de saberlo. Ese es el límite de la heurística, y es la razón por la que el flag viene apagado.

### Diferir hojas de estilo, y cuándo no conviene

Con el flag activado, un `<link rel="stylesheet">` pasa a ser un preload que se promueve a hoja de estilo en cuanto llega, con un respaldo en `<noscript>`:

```html
<link rel="preload" as="style" href="…" data-obsidian-include-sheet/>
<noscript><link rel="stylesheet" href="…"/></noscript>
```

El cambio lo hace un único `<script>` con nonce emitido una sola vez al final, nunca un atributo `onload` inline: bajo una CSP aplicada el atributo se descarta y la hoja quedaría como un preload que no se aplica jamás. Escucha el evento `load` y usa `DOMContentLoaded` como respaldo, ambos con `{ once: true }`.

**La página pinta antes de que esa CSS se aplique.** Si la hoja da estilo a algo sobre el fold, el comprador ve un destello de contenido sin estilo y la maqueta salta cuando la hoja aterriza, lo que penaliza el Cumulative Layout Shift. Enciéndelo solo cuando sepas que la hoja da estilo a contenido bajo el fold o es puramente cosmética. Es la misma razón por la que el tema difiere su propia hoja únicamente en las páginas que inlinearon critical CSS —ver [Rendimiento](0160-performance.md).

Dos detalles mantienen honesta la conversión:

- **`media="print"` se saltea.** Nunca bloqueó el render de pantalla, así que convertirla no ganaría nada y sí costaría algo: tras el swap pasaría a aplicarse a la pantalla.
- **`media`, `integrity`, `crossorigin`, `referrerpolicy`, `id` y `title` se preservan** tanto en el preload como en el `<noscript>`. `integrity` y `crossorigin` son válidos en `rel=preload as=style` y el navegador verifica el hash ahí, así que **Subresource Integrity sigue funcionando de punta a punta**.

### La válvula de escape

Cualquier etiqueta que lleve **`data-obsidian-blocking`** queda exactamente como se escribió, digan lo que digan los flags:

```html
<script src="https://cdn.example/anti-flicker.js" data-obsidian-blocking></script>
```

Todo lo demás del campo —`<meta>`, `<link rel="preconnect">`, comentarios HTML, texto suelto, scripts inline— sale byte por byte igual a como entró. El contenido nunca se parsea para volver a serializarlo: solo se reescribe en el lugar la lista de atributos de una etiqueta de apertura que coincida.

### El consejo que de verdad aplica

Antes de encender cualquiera de los dos flags, lo correcto casi siempre es **sacar ese script de head includes y cargarlo bien desde el tema**, donde se puede ordenar, empaquetar, diferir a propósito y medir. Estos flags son control de daños para contenido que no controlas o no puedes mover, no un sustituto de cargar un script correctamente.

---

## Próximos pasos

- [Datos estructurados (JSON-LD)](0130-structured-data.md) — la mitad de schema.org de esta misma historia.
- [Rendimiento](0160-performance.md) — critical CSS, los flags nativos de build y Varnish.
{% endraw %}
