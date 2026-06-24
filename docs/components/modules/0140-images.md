{% raw %}
# Responsive Images

**MageObsidian** ships an `image` helper that renders a Core-Web-Vitals-friendly `<img>` (or `<picture>`). It sets `width`/`height` to reserve layout space — eliminating **CLS** — and exposes `loading`/`fetchpriority` so you can defer below-the-fold images and prioritize the **LCP** image.

It works with any image URL, or a `Vendor_Module::path` asset id — for assets it resolves the URL and, when you omit the dimensions, **auto-detects** them from the source file so the markup is always CLS-safe without hand-measuring.

> **Scope:** this is the render layer. Catalog image *resizing* stays with Magento (driven by `view.xml`); the helper wraps the resulting URL with the right attributes. It does not re-encode catalog images.

---

## Usage

In **Twig**, use the `image` function ([see Twig helpers](../../twig/helpers.md)):

```twig
{# Asset id: URL resolved, width/height auto-detected from the source file #}
{{ image('Acme_Catalog::images/banner.jpg', { alt: 'Spring sale' }) }}

{# The LCP/hero image: prioritize it (auto-eager) #}
{{ image('Acme_Catalog::images/hero.jpg', { alt: 'Hero', fetchpriority: 'high' }) }}

{# A ready URL (e.g. a catalog image): pass the known dimensions #}
{{ image(product_image_url, { alt: product.name, width: 600, height: 600 }) }}
```

In **phtml**, reach the `Image` ViewModel through a layout argument:

```xml
<block class="MageObsidian\ModernFrontend\Block\Template" name="..." template="...">
    <arguments>
        <argument name="image" xsi:type="object">MageObsidian\ModernFrontend\ViewModel\Image</argument>
    </arguments>
</block>
```

```php
<?= $block->getData('image')->render('Acme_Catalog::images/banner.jpg', ['alt' => 'Spring sale']) ?>
```

## Options

| Option | Default | Purpose |
|---|---|---|
| `alt` | `''` | Alternative text (always emitted for valid HTML). |
| `width` / `height` | auto for assets | Reserve layout space — the CLS fix. |
| `loading` | `lazy` (`eager` when `fetchpriority: 'high'`) | Defer off-screen images. |
| `decoding` | `async` | Off-thread image decode. |
| `fetchpriority` | — | `high` for the LCP image; auto-switches `loading` to `eager`. |
| `class`, `sizes`, `srcset` | — | Standard `<img>` attributes. |
| `sources` | — | A list of `<source>`s — switches output to `<picture>`. |
| `attributes` | — | Any extra attributes (`id`, `data-*`, …). |

## `<picture>` with modern formats

Pass `sources` to emit a `<picture>` with AVIF/WebP fallbacks:

```twig
{{ image('Acme_Catalog::images/a.jpg', {
    alt: 'Product',
    sources: [
        { srcset: vite_url('Acme_Catalog::images/a.avif'), type: 'image/avif' },
        { srcset: vite_url('Acme_Catalog::images/a.webp'), type: 'image/webp' }
    ]
}) }}
```

> Generating AVIF/WebP at build time is not part of this helper yet — provide the alternate sources yourself (or via your own pipeline). The helper assembles the `<picture>`; it never invents formats.

## Why this helps Core Web Vitals

- **CLS:** `width`/`height` (or the auto-detected intrinsic size) let the browser reserve the box before the image loads — no layout shift.
- **LCP:** mark the hero image `fetchpriority: 'high'`; the helper keeps it `eager` so it is never lazy-loaded.
- **Everything else stays cheap:** images default to `loading="lazy"` and `decoding="async"`.

The default theme on the [live demo](https://mage-obsidian-demo.jeanmarcos.dev/) scores a perfect 100 across the board:

[![Lighthouse report: 100 across Performance, Accessibility, Best Practices and SEO](/assets/lighthouse-100.png)](https://mage-obsidian-demo.jeanmarcos.dev/){ .lighthouse-shot target=_blank rel=noopener }

## Next Steps

- [Twig Helpers](../../twig/helpers.md) — the `image` function and the rest of the bridge.
- [Structured Data](0130-structured-data.md) — another SEO-focused runtime layer.
{% endraw %}
