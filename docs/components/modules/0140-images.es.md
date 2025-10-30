{% raw %}
# Imágenes responsivas

**MageObsidian** incluye un helper `image` que renderiza un `<img>` (o `<picture>`) amigable con los Core Web Vitals. Fija `width`/`height` para reservar el espacio de layout —eliminando el **CLS**— y expone `loading`/`fetchpriority` para diferir las imágenes bajo el pliegue y priorizar la imagen **LCP**.

Funciona con cualquier URL de imagen, o con un id de asset `Vendor_Module::path` —para los assets resuelve la URL y, cuando omites las dimensiones, las **auto-detecta** desde el archivo fuente, así el markup siempre evita CLS sin medir a mano.

> **Alcance:** esta es la capa de render. El *redimensionado* de imágenes de catálogo sigue siendo de Magento (gobernado por `view.xml`); el helper envuelve la URL resultante con los atributos correctos. No re-codifica las imágenes de catálogo.

---

## Uso

En **Twig**, usa la función `image` ([ver helpers de Twig](../../twig/helpers.md)):

```twig
{# Id de asset: URL resuelta, width/height auto-detectados del archivo fuente #}
{{ image('Acme_Catalog::images/banner.jpg', { alt: 'Oferta de primavera' }) }}

{# La imagen LCP/hero: priorízala (eager automático) #}
{{ image('Acme_Catalog::images/hero.jpg', { alt: 'Hero', fetchpriority: 'high' }) }}

{# Una URL lista (p. ej. una imagen de catálogo): pasa las dimensiones conocidas #}
{{ image(product_image_url, { alt: product.name, width: 600, height: 600 }) }}
```

En **phtml**, alcanza el ViewModel `Image` mediante un argumento de layout:

```xml
<block class="MageObsidian\ModernFrontend\Block\Template" name="..." template="...">
    <arguments>
        <argument name="image" xsi:type="object">MageObsidian\ModernFrontend\ViewModel\Image</argument>
    </arguments>
</block>
```

```php
<?= $block->getData('image')->render('Acme_Catalog::images/banner.jpg', ['alt' => 'Oferta de primavera']) ?>
```

## Opciones

| Opción | Default | Propósito |
|---|---|---|
| `alt` | `''` | Texto alternativo (siempre se emite, para HTML válido). |
| `width` / `height` | auto en assets | Reservan el espacio de layout — el arreglo de CLS. |
| `loading` | `lazy` (`eager` si `fetchpriority: 'high'`) | Difiere imágenes fuera de pantalla. |
| `decoding` | `async` | Decodificación de imagen fuera del hilo principal. |
| `fetchpriority` | — | `high` para la imagen LCP; cambia `loading` a `eager` automáticamente. |
| `class`, `sizes`, `srcset` | — | Atributos `<img>` estándar. |
| `sources` | — | Una lista de `<source>` — cambia la salida a `<picture>`. |
| `attributes` | — | Cualquier atributo extra (`id`, `data-*`, …). |

## `<picture>` con formatos modernos

Pasa `sources` para emitir un `<picture>` con fallbacks AVIF/WebP:

```twig
{{ image('Acme_Catalog::images/a.jpg', {
    alt: 'Producto',
    sources: [
        { srcset: vite_url('Acme_Catalog::images/a.avif'), type: 'image/avif' },
        { srcset: vite_url('Acme_Catalog::images/a.webp'), type: 'image/webp' }
    ]
}) }}
```

> Generar AVIF/WebP en tiempo de build aún no forma parte de este helper —proporciona tú los sources alternos (o vía tu propio pipeline). El helper ensambla el `<picture>`; nunca inventa formatos.

## Por qué ayuda a los Core Web Vitals

- **CLS:** `width`/`height` (o el tamaño intrínseco auto-detectado) dejan que el navegador reserve la caja antes de cargar la imagen — sin saltos de layout.
- **LCP:** marca la imagen hero con `fetchpriority: 'high'`; el helper la mantiene `eager` para que nunca se cargue de forma perezosa.
- **El resto sigue siendo barato:** las imágenes usan `loading="lazy"` y `decoding="async"` por defecto.

## Próximos pasos

- [Helpers de Twig](../../twig/helpers.md) — la función `image` y el resto del puente.
- [Datos estructurados](0130-structured-data.md) — otra capa de runtime enfocada en SEO.
{% endraw %}
