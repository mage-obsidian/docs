{% raw %}
# Structured Data (JSON-LD)

**MageObsidian** auto-emits [schema.org](https://schema.org) structured data as JSON-LD so search engines can render rich results (product snippets, breadcrumbs, the sitelinks search box). It stays true to the project's server-rendered approach: the markup is part of the cached HTML — it lives inside Magento's Full Page Cache and ships no extra JavaScript.

---

## What's emitted automatically

With the feature enabled (the default), every storefront page carries the nodes relevant to it, linked to each other by `@id` so a crawler reads one graph rather than four unrelated fragments:

- **Organization** — site-wide, built entirely from configuration: `name`, `url`, `logo`, `description`, `telephone`, `email`, `vatID`, a `PostalAddress`, a `ContactPoint` and the `sameAs` URIs that let a search or answer engine tie the site to a known entity.
- **WebSite** — site-wide, including the `SearchAction` that enables Google's sitelinks search box.
- **WebPage** — one per page, carrying `datePublished` and `dateModified`: the freshness signals crawlers and answer engines look for. Its `@type` narrows to the page: `ItemPage` on a product, `CollectionPage` on a category or wishlist, `SearchResultsPage` on search, `ContactPage`, `CheckoutPage`, and plain `WebPage` everywhere else, CMS included. It links out with `isPartOf` (the WebSite), `breadcrumb`, `mainEntity` (the Product) and `publisher` (the Organization).
- **BreadcrumbList** — on catalog pages, built from Magento's native breadcrumb path (Home is prepended, the current page omits its URL).
- **Product** with a nested **Offer** — on product pages.

An empty field is **omitted** rather than emitted blank, because an empty property invalidates the node.

### The Product node

Beyond `name`, `sku`, `description`, `image`, `price`, `priceCurrency` and `availability`, the node carries:

| Property | Where it comes from |
|---|---|
| `brand` | a configurable attribute, `manufacturer` by default |
| `gtin`, `gtin8` / `gtin12` / `gtin13` / `gtin14` | a configurable attribute; the digit count picks the right property, and separators are stripped |
| `mpn` | a configurable attribute |
| `itemCondition` | configurable, `NewCondition` by default, with a "do not emit" option |
| `image` | several images from the media gallery, up to a configurable limit |
| `url`, `@id` | the product page, and the anchor the WebPage's `mainEntity` points at |
| `priceValidUntil` | see the warning below |

**Configurable, grouped and bundle products emit an `AggregateOffer`** with `lowPrice` and `highPrice` when the variants span a price range, instead of a single `Offer` carrying one final price that may not match what the shopper — and Google — see on the page. When the range collapses to a single value, it stays a plain `Offer`.

### Ratings and reviews

`aggregateRating` and `review` **are emitted on the product page** when the product has reviews. They are contributed by `MageObsidian_Review`, the only module that depends on `Magento_Review`, through a plugin on `CurrentPageSchemaProvider` (`MageObsidian\Review\Plugin\SchemaOrg\AddProductRating`, wired in that module's `etc/frontend/di.xml`).

It attaches them to the page's **single** `Product` node rather than emitting a second one from a template — two partial descriptions of the same product would leave a search engine choosing between them. A product with no reviews gets neither property.

The JSON-LD is rendered just before `</body>` (valid anywhere in the document for Google), alongside the other MageObsidian runtime markers.

## Configuration

Everything lives under **Stores → Configuration → MageObsidian → SEO**, scoped per store view, and every field depends on the master switch.

| Setting | Path | Default |
|---|---|---|
| Emit Structured Data (JSON-LD) | `mage_obsidian/seo/structured_data_enabled` | `1` |
| Emit WebPage Node | `mage_obsidian/seo/webpage_enabled` | `1` |
| Organization Logo | `mage_obsidian/seo/organization_logo` | empty (falls back to the header logo) |
| Organization Description | `mage_obsidian/seo/organization_description` | empty (falls back to `design/head/default_description`) |
| Organization sameAs URIs | `mage_obsidian/seo/organization_same_as` | empty |
| Contact Point Type | `mage_obsidian/seo/organization_contact_type` | `customer support` |
| Emit Postal Address | `mage_obsidian/seo/organization_address_enabled` | `1` |
| Brand Attribute Code | `mage_obsidian/seo/product_brand_attribute` | `manufacturer` |
| GTIN Attribute Code | `mage_obsidian/seo/product_gtin_attribute` | empty |
| MPN Attribute Code | `mage_obsidian/seo/product_mpn_attribute` | empty |
| Item Condition | `mage_obsidian/seo/product_condition` | `NewCondition` |
| Product Images In Schema | `mage_obsidian/seo/product_image_limit` | `3` |
| priceValidUntil Horizon (days) | `mage_obsidian/seo/price_valid_until_days` | `0` |

```bash
# Disable everything (e.g. when another SEO extension already outputs JSON-LD)
bin/magento config:set mage_obsidian/seo/structured_data_enabled 0
```

The defaults are all safe: without configuring anything a store gains `@id`, `inLanguage`, `publisher`, the WebPage node with its dates, `itemCondition`, `brand` (if it uses `manufacturer`) and multiple images. `sameAs`, the GTIN and MPN attributes and `price_valid_until_days` stay off until the merchant sets them, because **there is no correct default** for any of them.

A separate **Organization Logo** exists because the header logo is often an SVG or a horizontal lockup, while Google wants a raster of at least 112×112 for the knowledge panel. Leave it empty to reuse the header logo.

### `priceValidUntil`: a claim, not a computed fact

The horizon ships at **`0`, meaning the property is not emitted**, and that is deliberate.

An active special price always supplies `priceValidUntil` from its own end date — and only when that date is in the future, because a past date tells Google the price has expired. That is reading a fact, not inventing one.

The horizon field only applies when there is no special price, and **any value above 0 asserts to Google that your price is guaranteed for that many days**. That assertion is the merchant's, not something the framework can compute. Google treats an invented validity date as misleading markup, which is a policy risk — whereas omitting the property costs only a **non-blocking warning** in the Rich Results Test, since Google lists it as recommended, not required.

A policy risk is never worth trading for a warning. Set it above 0 only if your commercial policy actually guarantees prices for that window.

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

- **Pure builders** (`Organization`, `WebSite`, `WebPage`, `BreadcrumbList`, `Product`) turn plain data into schema.org arrays, omitting empty fields so the output is never invalid.
- A **renderer** serializes a node into a `<script type="application/ld+json">` tag with escaping that prevents an embedded `</script>` from breaking out.
- A **provider** collects the current page's data from Magento (product, breadcrumbs, store, logo, dates) and feeds the builders; a runtime block emits the result. Other modules extend the graph by plugging into that provider rather than emitting nodes of their own — which is how the rating reaches the Product node.

Structured data is an enhancement, never page-critical: if generation fails, the error is logged and the page renders without it.

## Next Steps

- [SEO & Head Metadata](0135-seo-head.md) — canonical, Open Graph, robots and the manifest.
- [Twig Helpers](../../twig/helpers.md) — the `json_ld` function and the rest of the bridge.
- [Internationalization](0107-i18n.md) — another runtime layer wired the same way.
{% endraw %}
