{% raw %}
# Structured Data (JSON-LD)

**MageObsidian** auto-emits [schema.org](https://schema.org) structured data as JSON-LD so search engines can render rich results (product snippets, breadcrumbs, the sitelinks search box). It stays true to the project's server-rendered approach: the markup is part of the cached HTML — it lives inside Magento's Full Page Cache and ships no extra JavaScript.

---

## What's emitted automatically

With the feature enabled (the default), every storefront page carries the nodes relevant to it:

- **Organization** and **WebSite** — site-wide. `WebSite` includes the `SearchAction` that enables Google's sitelinks search box.
- **BreadcrumbList** — on catalog pages, built from Magento's native breadcrumb path (Home is prepended, the current page omits its URL).
- **Product** with a nested **Offer** — on product pages: name, SKU, image, brand, price, currency and availability.

`aggregateRating` / `review` are intentionally left out for now, to avoid emitting rating data the storefront cannot back.

The JSON-LD is rendered just before `</body>` (valid anywhere in the document for Google), alongside the other MageObsidian runtime markers.

## Enabling and disabling

It is **on by default**. Toggle it under **Stores → Configuration → MageObsidian → SEO → Emit Structured Data (JSON-LD)**, or via the config path `mage_obsidian/seo/structured_data_enabled`:

```bash
# Disable (e.g. when another SEO extension already outputs JSON-LD, to avoid duplicates)
bin/magento config:set mage_obsidian/seo/structured_data_enabled 0
```

The flag is scoped per store view, so you can enable it only where you want it.

## Custom types in templates

For types MageObsidian doesn't emit on its own (`FAQPage`, `Article`, `Event`, …) there's a template helper. It wraps your data in a node — `@context` and `@type` are added for you, so you pass only the body.

In **Twig**, use the `json_ld` function ([see Twig helpers](../../twig/helpers.md)):

```twig
{{ json_ld('FAQPage', {
    mainEntity: [
        {
            '@type': 'Question',
            name: 'Do you ship worldwide?',
            acceptedAnswer: { '@type': 'Answer', text: 'Yes, we ship to most countries.' }
        }
    ]
}) }}
```

In **phtml**, reach the `SchemaOrg` ViewModel through a layout argument:

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
            'name' => 'Do you ship worldwide?',
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => 'Yes, we ship to most countries.'],
        ],
    ],
]) ?>
```

## How it works

- **Pure builders** (`Organization`, `WebSite`, `BreadcrumbList`, `Product`) turn plain data into schema.org arrays, omitting empty fields so the output is never invalid.
- A **renderer** serializes a node into a `<script type="application/ld+json">` tag with escaping that prevents an embedded `</script>` from breaking out.
- A **provider** collects the current page's data from Magento (product, breadcrumbs, store, logo) and feeds the builders; a runtime block emits the result.

Structured data is an enhancement, never page-critical: if generation fails, the error is logged and the page renders without it.

## Next Steps

- [Twig Helpers](../../twig/helpers.md) — the `json_ld` function and the rest of the bridge.
- [Internationalization](0107-i18n.md) — another runtime layer wired the same way.
{% endraw %}
