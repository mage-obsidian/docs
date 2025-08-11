{% raw %}
# Datos estructurados (JSON-LD)

**MageObsidian** emite automáticamente datos estructurados de [schema.org](https://schema.org) como JSON-LD para que los buscadores muestren rich results (snippets de producto, migas de pan, la caja de búsqueda de sitelinks). Se mantiene fiel al enfoque renderizado en servidor del proyecto: el markup forma parte del HTML cacheado —vive dentro del Full Page Cache de Magento— y no envía JavaScript adicional.

---

## Qué se emite automáticamente

Con la función habilitada (el valor por defecto), cada página del storefront lleva los nodos que le corresponden:

- **Organization** y **WebSite** — a nivel de sitio. `WebSite` incluye el `SearchAction` que habilita la caja de búsqueda de sitelinks de Google.
- **BreadcrumbList** — en páginas de catálogo, construida desde la ruta de migas nativa de Magento (se antepone Inicio, y la página actual omite su URL).
- **Product** con un **Offer** anidado — en páginas de producto: nombre, SKU, imagen, marca, precio, moneda y disponibilidad.

`aggregateRating` / `review` se dejan fuera por ahora, para no emitir datos de valoración que el storefront no pueda respaldar.

El JSON-LD se renderiza justo antes de `</body>` (válido en cualquier parte del documento para Google), junto a los demás marcadores de runtime de MageObsidian.

## Habilitar y deshabilitar

Está **activado por defecto**. Se conmuta en **Stores → Configuration → MageObsidian → SEO → Emit Structured Data (JSON-LD)**, o mediante la ruta de config `mage_obsidian/seo/structured_data_enabled`:

```bash
# Deshabilitar (p. ej. cuando otra extensión SEO ya emite JSON-LD, para evitar duplicados)
bin/magento config:set mage_obsidian/seo/structured_data_enabled 0
```

El flag tiene alcance por vista de tienda, así que puedes habilitarlo solo donde lo quieras.

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

- Los **builders puros** (`Organization`, `WebSite`, `BreadcrumbList`, `Product`) convierten datos planos en arrays de schema.org, omitiendo los campos vacíos para que la salida nunca sea inválida.
- Un **renderer** serializa un nodo en una etiqueta `<script type="application/ld+json">` con un escaping que impide que un `</script>` incrustado rompa la etiqueta.
- Un **provider** recoge los datos de la página actual desde Magento (producto, migas, tienda, logo) y alimenta los builders; un block de runtime emite el resultado.

Los datos estructurados son una mejora, nunca algo crítico para la página: si la generación falla, el error se registra y la página se renderiza sin ellos.

## Próximos pasos

- [Helpers de Twig](../../twig/helpers.md) — la función `json_ld` y el resto del puente.
- [Internacionalización](0107-i18n.md) — otra capa de runtime cableada del mismo modo.
{% endraw %}
