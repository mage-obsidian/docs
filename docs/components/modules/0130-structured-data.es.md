{% raw %}
# Datos estructurados (JSON-LD)

**MageObsidian** emite automáticamente datos estructurados de [schema.org](https://schema.org) como JSON-LD para que los buscadores muestren rich results (snippets de producto, migas de pan, la caja de búsqueda de sitelinks). Se mantiene fiel al enfoque renderizado en servidor del proyecto: el markup forma parte del HTML cacheado —vive dentro del Full Page Cache de Magento— y no envía JavaScript adicional.

---

## Qué se emite automáticamente

Con la función habilitada (el valor por defecto), cada página del storefront lleva los nodos que le corresponden, enlazados entre sí por `@id` para que un crawler lea un solo grafo y no cuatro fragmentos sueltos:

- **Organization** — a nivel de sitio, construido íntegramente desde la configuración: `name`, `url`, `logo`, `description`, `telephone`, `email`, `vatID`, una `PostalAddress`, un `ContactPoint` y los URIs de `sameAs`, que son los que permiten a un buscador o a un motor de respuestas asociar el sitio con una entidad conocida.
- **WebSite** — a nivel de sitio, incluido el `SearchAction` que habilita la caja de búsqueda de sitelinks de Google.
- **WebPage** — uno por página, con `datePublished` y `dateModified`: las señales de frescura que buscan los crawlers y los motores de respuestas. Su `@type` se ajusta a la página: `ItemPage` en un producto, `CollectionPage` en una categoría o una lista de deseos, `SearchResultsPage` en la búsqueda, `ContactPage`, `CheckoutPage`, y `WebPage` a secas en el resto, CMS incluido. Enlaza hacia afuera con `isPartOf` (el WebSite), `breadcrumb`, `mainEntity` (el Product) y `publisher` (la Organization).
- **BreadcrumbList** — en páginas de catálogo, construida desde la ruta de migas nativa de Magento (se antepone Inicio, y la página actual omite su URL).
- **Product** con un **Offer** anidado — en páginas de producto.

Un campo vacío **se omite** en lugar de emitirse en blanco, porque una propiedad vacía invalida el nodo.

### El nodo Product

Además de `name`, `sku`, `description`, `image`, `price`, `priceCurrency` y `availability`, el nodo lleva:

| Propiedad | De dónde sale |
|---|---|
| `brand` | un atributo configurable; `manufacturer` por defecto |
| `gtin`, `gtin8` / `gtin12` / `gtin13` / `gtin14` | un atributo configurable; la cantidad de dígitos elige la propiedad correcta, y los separadores se limpian |
| `mpn` | un atributo configurable |
| `itemCondition` | configurable, `NewCondition` por defecto, con una opción para no emitirlo |
| `image` | varias imágenes de la galería, hasta un límite configurable |
| `url`, `@id` | la página del producto, y el ancla a la que apunta el `mainEntity` del WebPage |
| `priceValidUntil` | ver la advertencia más abajo |

**Los productos configurables, agrupados y bundle emiten un `AggregateOffer`** con `lowPrice` y `highPrice` cuando las variantes abarcan un rango de precios, en lugar de un `Offer` único con un precio final que puede no coincidir con lo que ven el comprador —y Google— en la página. Cuando el rango colapsa en un solo valor, sigue siendo un `Offer` plano.

### Valoraciones y reseñas

`aggregateRating` y `review` **sí se emiten en la ficha de producto** cuando el producto tiene reseñas. Los aporta `MageObsidian_Review`, el único módulo que depende de `Magento_Review`, mediante un plugin sobre `CurrentPageSchemaProvider` (`MageObsidian\Review\Plugin\SchemaOrg\AddProductRating`, declarado en el `etc/frontend/di.xml` de ese módulo).

Los adjunta al **único** nodo `Product` de la página en vez de emitir un segundo nodo desde una plantilla: dos descripciones parciales del mismo producto obligarían a un buscador a elegir entre ellas. Un producto sin reseñas no recibe ninguna de las dos propiedades.

El JSON-LD se renderiza justo antes de `</body>` (válido en cualquier parte del documento para Google), junto a los demás marcadores de runtime de MageObsidian.

## Configuración

Todo vive en **Stores → Configuration → MageObsidian → SEO**, con alcance por vista de tienda, y cada campo depende del interruptor principal.

| Ajuste | Ruta | Valor por defecto |
|---|---|---|
| Emit Structured Data (JSON-LD) | `mage_obsidian/seo/structured_data_enabled` | `1` |
| Emit WebPage Node | `mage_obsidian/seo/webpage_enabled` | `1` |
| Organization Logo | `mage_obsidian/seo/organization_logo` | vacío (cae al logo del header) |
| Organization Description | `mage_obsidian/seo/organization_description` | vacío (cae a `design/head/default_description`) |
| Organization sameAs URIs | `mage_obsidian/seo/organization_same_as` | vacío |
| Contact Point Type | `mage_obsidian/seo/organization_contact_type` | `customer support` |
| Emit Postal Address | `mage_obsidian/seo/organization_address_enabled` | `1` |
| Brand Attribute Code | `mage_obsidian/seo/product_brand_attribute` | `manufacturer` |
| GTIN Attribute Code | `mage_obsidian/seo/product_gtin_attribute` | vacío |
| MPN Attribute Code | `mage_obsidian/seo/product_mpn_attribute` | vacío |
| Item Condition | `mage_obsidian/seo/product_condition` | `NewCondition` |
| Product Images In Schema | `mage_obsidian/seo/product_image_limit` | `3` |
| priceValidUntil Horizon (days) | `mage_obsidian/seo/price_valid_until_days` | `0` |

```bash
# Deshabilitar todo (p. ej. cuando otra extensión SEO ya emite JSON-LD)
bin/magento config:set mage_obsidian/seo/structured_data_enabled 0
```

Todos los valores por defecto son seguros: sin configurar nada, una tienda gana `@id`, `inLanguage`, `publisher`, el nodo WebPage con sus fechas, `itemCondition`, `brand` (si usa `manufacturer`) e imágenes múltiples. `sameAs`, los atributos de GTIN y MPN y `price_valid_until_days` quedan apagados hasta que el merchant los configure, porque **no existe un valor por defecto correcto** para ninguno.

Hay un campo **Organization Logo** aparte porque el logo del header suele ser un SVG o un lockup horizontal, mientras que Google pide un raster de al menos 112×112 para el panel de conocimiento. Déjalo vacío para reutilizar el logo del header.

### `priceValidUntil`: una afirmación, no un dato calculado

El horizonte viene en **`0`, es decir que la propiedad no se emite**, y es a propósito.

Un precio especial activo siempre aporta `priceValidUntil` desde su propia fecha de fin —y solo cuando esa fecha es futura, porque una fecha pasada le dice a Google que el precio expiró. Eso es leer un dato, no inventarlo.

El campo del horizonte solo aplica cuando no hay precio especial, y **cualquier valor mayor que 0 le afirma a Google que tu precio está garantizado durante esa cantidad de días**. Esa afirmación es del merchant, no algo que el framework pueda calcular. Google trata una fecha de vigencia inventada como marcado engañoso, lo que es un riesgo de política —mientras que omitir la propiedad cuesta apenas un **warning no bloqueante** en el Rich Results Test, ya que Google la lista como recomendada, no como obligatoria.

Un riesgo de política nunca compensa evitar un warning. Ponlo por encima de 0 solo si tu política comercial realmente garantiza los precios durante esa ventana.

## Tipos personalizados en las plantillas

Para los tipos que MageObsidian no emite por sí mismo (`FAQPage`, `Article`, `Event`, …) hay un helper de plantilla. Envuelve tus datos en un nodo —`@context` y `@type` se añaden por ti, así que solo pasas el cuerpo.

En **Twig**, usa la función `json_ld` ([ver helpers de Twig](../../twig/helpers.md)):

```twig
{{ json_ld('FAQPage', {
    mainEntity: [
        {
            '@type': 'Question',
            name: '¿Hacen envíos internacionales?',
            acceptedAnswer: { '@type': 'Answer', text: 'Sí, enviamos a la mayoría de los países.' }
        }
    ]
}) }}
```

En **phtml**, alcanza el ViewModel `SchemaOrg` mediante un argumento de layout:

```xml
<block class="MageObsidian\ModernFrontend\Block\Template" name="faq.schema" template="...">
    <arguments>
        <argument name="schema_org" xsi:type="object">MageObsidian\ModernFrontend\ViewModel\SchemaOrg</argument>
    </arguments>
</block>
```

```php
<?= $block->getData('schema_org')->renderJsonLd('FAQPage', [
    'mainEntity' => [
        [
            '@type' => 'Question',
            'name' => '¿Hacen envíos internacionales?',
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => 'Sí, enviamos a la mayoría de los países.'],
        ],
    ],
]) ?>
```

## Cómo funciona

- Los **builders puros** (`Organization`, `WebSite`, `WebPage`, `BreadcrumbList`, `Product`) convierten datos planos en arrays de schema.org, omitiendo los campos vacíos para que la salida nunca sea inválida.
- Un **renderer** serializa un nodo en una etiqueta `<script type="application/ld+json">` con un escaping que impide que un `</script>` incrustado rompa la etiqueta.
- Un **provider** recoge los datos de la página actual desde Magento (producto, migas, tienda, logo, fechas) y alimenta los builders; un block de runtime emite el resultado. Otros módulos extienden el grafo enganchándose a ese provider en vez de emitir nodos propios: así es como la valoración llega al nodo Product.

Los datos estructurados son una mejora, nunca algo crítico para la página: si la generación falla, el error se registra y la página se renderiza sin ellos.

## Próximos pasos

- [SEO y metadata del head](0135-seo-head.md) — canónica, Open Graph, robots y el manifest.
- [Helpers de Twig](../../twig/helpers.md) — la función `json_ld` y el resto del puente.
- [Internacionalización](0107-i18n.md) — otra capa de runtime cableada del mismo modo.
{% endraw %}
