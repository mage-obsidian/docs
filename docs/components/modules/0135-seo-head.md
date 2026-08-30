{% raw %}
# SEO & Head Metadata

**MageObsidian** fills in the head metadata Magento leaves empty: a canonical URL on every page, Open Graph and Twitter Card properties, a meta description derived from the page itself, the modern robots directives, and a Web App Manifest. Everything is server-rendered into the cached HTML — no extra JavaScript, nothing computed in the browser.

The metadata lives in `MageObsidian_Storefront` and is written through Magento's own `Page\Config`, so core does the escaping and the rendering. Every piece is a toggle: a store already running an SEO extension turns off the half that duplicates it.

---

## Upgrade note: the head now carries the page asset collection

Until this version the theme's root template printed only `headContent` and `headAdditional`. It never printed **`headAssets`**, which is the only thing that renders Magento's page asset collection.

Everything that goes through `Page\Config::addPageAsset()` / `addRemotePageAsset()` was generated, stored — and silently dropped. That included:

- the **canonical** the core emits on catalog pages (with `catalog/seo/*_canonical_tag` on),
- the native **`<link rel="icon">` / `<link rel="shortcut icon">`**,
- the RSS **`<link rel="alternate">`**,
- and whatever the merchant configured in **Design → HTML Head → Scripts and Style Sheets**.

`root.phtml` now prints it. This is a fix, but **it changes what an existing store emits in its head**, so plan the upgrade with that in mind: measured on this project's demo, it adds four tags and between 448 and 530 bytes per page. No RequireJS, no jQuery, no Luma CSS — those pipelines are excluded from Obsidian themes elsewhere, so the collection simply does not contain them.

The one thing worth checking before you deploy is the last item on that list: if `design/head/includes` has something in it, **it is being served now and it was not before**. Read the [Head includes](#head-includes-native-magento-and-render-blocking) section below before you assume that is free.

---

## Canonical URL

Magento only emits a canonical on catalog pages, and only with the catalog SEO flags on. CMS pages, the home page and search results never get one. MageObsidian emits it **on every page that does not already have one**.

A canonical set by the core or by another extension is **never overwritten**. The module inspects the page asset collection first; if a canonical is already claimed, it writes nothing.

### Query parameters: an allowlist

Everything not on the list is dropped, tracking parameters included. The default is `p,q`:

- **`p`** stays because a paginated listing has to point at itself. If page 2 canonicalises onto page 1, the products only reachable from page 2 leave the index.
- **`q`** stays because without it every search result canonicalises onto the same empty URL.

An allowlist is used rather than a blocklist because a blocklist ages: today it is `utm_*`, `gclid` and `fbclid`, tomorrow it is something else.

A pagination parameter of `1` and any listed parameter with an empty value are dropped as well, so `?p=1` never produces a second URL for the first page.

```
/gear/bags.html?p=2&color=Blue&utm_source=nl   →   /gear/bags.html?p=2
/catalogsearch/result/?q=bag&p=1               →   /catalogsearch/result?q=bag
```

### URL suffix and the trailing slash

The path is normalised without its trailing slash, because Magento answers `200` for both `/about-us` and `/about-us/` — leaving both would mean two indexable URLs for one page.

The exception is a store whose `catalog/seo/category_url_suffix` or `catalog/seo/product_url_suffix` **is** `/`. There the slash is part of the address, so the path is left exactly as it is.

### Configuration

| Setting | Path | Default |
|---|---|---|
| Emit a Canonical URL | `mage_obsidian/seo/canonical_enabled` | `1` |
| Query Parameters Kept in the Canonical | `mage_obsidian/seo/canonical_query_params` | `p,q` |

**Stores → Configuration → MageObsidian → SEO**.

```bash
# Let pagination and search results collapse onto a single URL
bin/magento config:set mage_obsidian/seo/canonical_query_params ""
```

---

## Open Graph and Twitter Card

With social metadata on, the head carries, derived from the page's own title, description and imagery:

| Property | Source |
|---|---|
| `og:type` | `product` on a product page, `website` everywhere else |
| `og:site_name` | store name |
| `og:locale` | `general/locale/code` |
| `og:title` | the page title |
| `og:description` | the page's meta description |
| `og:url` | the resolved canonical — including one set by the core |
| `og:image` | the entity's image, then the fallback share image, then the store logo |
| `twitter:card` | `summary_large_image` |
| `twitter:site` | the configured account, omitted when empty |
| `twitter:title` / `twitter:description` / `twitter:image` | as above |

`og:url` deliberately uses the **resolved** canonical rather than the module's own: if the core canonicalises a product page to a URL, the shared URL has to be that same one.

### It complements, it does not duplicate

On a product page `MageObsidian_Catalog` already emits its own Open Graph block (`opengraph.general`, from the `ProductOpenGraph` view model): `og:type`, `og:title`, `og:url`, `og:image`, `og:description` and the `product:price:*` pair.

Rather than hardcoding that list, the module **asks the block what it emits**. A di.xml map pairs a block name with the layout argument holding its view model, and the object is queried through `getProperties()`; whatever it claims is left to it:

```xml
<type name="MageObsidian\Storefront\Model\Seo\ClaimedSocialProperties">
    <arguments>
        <argument name="claimants" xsi:type="array">
            <item name="opengraph.general" xsi:type="string">open_graph</item>
        </argument>
    </arguments>
</type>
```

If that block grows a property tomorrow, the detection follows on its own. A store running a third-party SEO extension adds one line here and its properties stop being duplicated too.

### Configuration

| Setting | Path | Default |
|---|---|---|
| Emit Open Graph and Twitter Card Metadata | `mage_obsidian/seo/social_meta_enabled` | `1` |
| Fallback Share Image | `mage_obsidian/seo/social_image` | empty (falls back to the store logo) |
| Twitter Account | `mage_obsidian/seo/twitter_site` | empty (`twitter:site` omitted) |

The fallback share image should be 1200×630 or larger.

---

## Meta description

Magento repeats the store default description on every page that has none of its own. When the fallback is on, the module replaces it with something about the actual page:

1. the entity's own meta description wins;
2. otherwise the entity's content is summarised — HTML stripped (`<script>` and `<style>` with their contents, Page Builder `{{...}}` directives too), whitespace collapsed, cut at a word boundary around 160 characters;
3. if the page already carries something specific — another extension, a layout handle — it is left alone.

The module only steps in when the page is **repeating the store default**, and the comparison runs on normalised text, so the HTML escaping `setMetadata()` applies does not defeat it.

| Setting | Path | Default |
|---|---|---|
| Derive the Meta Description from the Page | `mage_obsidian/seo/meta_description_fallback` | `1` |

---

## Meta robots

Magento writes `INDEX,FOLLOW` and stops there. The module appends the three directives that control how much of the page a search engine may show:

```html
<meta name="robots" content="INDEX,FOLLOW,max-image-preview:large,max-snippet:-1,max-video-preview:-1"/>
```

Two rules keep it safe:

- **A page that is `NOINDEX` is never touched.** The extension bails out on sight of the directive, so a page kept out of the index stays exactly as Magento wrote it.
- **It only writes when it actually adds something.** A directive already present is not repeated, and when there is nothing to add the value is left untouched.

| Setting | Path | Default |
|---|---|---|
| Extra Robots Directives | `mage_obsidian/seo/robots_directives` | `max-image-preview:large,max-snippet:-1,max-video-preview:-1` |

Clear the field to leave the meta robots exactly as Magento wrote it.

---

## Web App Manifest

The manifest is derived from store configuration — name, base URL, logo, favicon, colours — so it is served by a controller rather than shipped as a static file, and it varies per store view.

**Endpoint:** `/mage-obsidian-storefront/manifest/`, linked from the head with `<link rel="manifest">`.

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

Notes worth knowing:

- The media type is `application/manifest+json`, not `application/json`.
- It is cacheable for a day by the browser, the CDN and Varnish. Magento's full page cache does not reach it — that only covers `Result\Page` — so the HTTP headers are the mechanism here.
- `icons` appears once a logo or favicon is configured; without either, the property is omitted rather than emitted empty.
- Turned off, the endpoint answers **404**, not an empty manifest, and the `404` does not advertise itself as cacheable for a day.

| Setting | Path | Default |
|---|---|---|
| Serve a Web App Manifest | `mage_obsidian/seo/manifest_enabled` | `1` |
| Manifest Display Mode | `mage_obsidian/seo/manifest_display` | `standalone` |
| Manifest Theme Colour | `mage_obsidian/seo/manifest_theme_color` | `#ffffff` |
| Manifest Background Colour | `mage_obsidian/seo/manifest_background_color` | `#ffffff` |

---

## Head includes: native Magento, and render-blocking

**Design → HTML Head → Scripts and Style Sheets** (`design/head/includes`) is a **native Magento** capability. Whatever is pasted there is inserted into the `<head>` verbatim, on every page of the store view.

### Everything in that field is render-blocking

This is the part that gets underestimated:

- a `<script src>` with neither `async` nor `defer` **stops the HTML parser** until it has been fetched, parsed and executed;
- a `<link rel="stylesheet">` **blocks the first paint** until the sheet arrives.

On a stack that measures FCP and LCP in milliseconds, a single third-party tag in that field can cost more than the entire rest of the page. It is the one place in the admin where a merchant can undo the whole front-end budget with a paste.

### The framework does not rewrite it

That field is merchant content on a native Magento contract, and whoever pastes into it owns what it does. MageObsidian leaves it alone. **Both flags below ship off**, so out of the box the behaviour is exactly Magento's.

Two opt-in flags exist for merchants who have looked at their own content and decided:

| Setting | Path | Default |
|---|---|---|
| Defer Scripts In Head Includes | `mage_obsidian/head/includes_defer_scripts` | `0` |
| Defer Stylesheets In Head Includes | `mage_obsidian/head/includes_defer_styles` | `0` |

**Stores → Configuration → MageObsidian → Frontend → HTML Head Includes**.

### Deferring scripts — and when not to

With the flag on, an external `<script src>` gets `defer`. `async`, `defer` and `type="module"` tags are already non-blocking and are left alone; **an inline script is never touched**, because there is no safe way to defer one and it may be exactly what has to run first.

**Do not turn this on if the field holds a tag that has to run blocking.** The two common cases both live in this exact field:

- **A/B testing anti-flicker snippets.** Deferred, they cause the very flash of the original content they exist to prevent.
- **Consent managers.** Deferred, the banner arrives after the page — and after the tags it was supposed to gate.

#### The positional rule

An external script is deferred **only if no inline `<script>` follows it in the same field**. The canonical analytics snippet is a pair:

```html
<script src="https://cdn.example/lib.js"></script>
<script>lib.init()</script>
```

A deferred script runs *after* the document is parsed, so it would run after that inline call — `lib` would not exist yet and the page would break. The rule is positional, not global:

```html
<script src="a.js"></script>      <!-- not deferred: an inline follows -->
<script>a.init()</script>
<script src="b.js"></script>      <!-- deferred: nothing inline after it -->
```

**That check only sees this one field.** If an inline script in a template, in another module, or in a Page Builder widget depends on a script pasted here, the framework has no way to know. That is the limit of the heuristic, and it is the reason the flag is off by default.

### Deferring stylesheets — and when not to

With the flag on, a `<link rel="stylesheet">` becomes a preload that is promoted to a stylesheet once it arrives, with a `<noscript>` fallback:

```html
<link rel="preload" as="style" href="…" data-obsidian-include-sheet/>
<noscript><link rel="stylesheet" href="…"/></noscript>
```

The swap runs from a single nonced `<script>` emitted once at the end, never from an inline `onload` attribute — under an enforced CSP the attribute is dropped and the sheet would stay a preload that never applies. It listens for `load` and falls back to `DOMContentLoaded`, both `{ once: true }`.

**The page paints before that CSS applies.** If the sheet styles anything above the fold, the shopper sees a flash of unstyled content and the layout jumps when it lands, which counts against Cumulative Layout Shift. Only turn it on when you know the sheet styles content below the fold or is purely cosmetic. It is the same reason the theme only defers its own stylesheet on pages that inlined critical CSS — see [Performance](0160-performance.md).

Two details keep the conversion honest:

- **`media="print"` is skipped.** It never blocked the screen render, so converting it would gain nothing and cost something: after the swap it would apply to the screen.
- **`media`, `integrity`, `crossorigin`, `referrerpolicy`, `id` and `title` are carried over** to both the preload and the `<noscript>`. `integrity` and `crossorigin` are valid on `rel=preload as=style` and the browser verifies the hash there, so **Subresource Integrity keeps working end to end**.

### The escape hatch

Any tag carrying **`data-obsidian-blocking`** is left exactly as written, whatever the flags say:

```html
<script src="https://cdn.example/anti-flicker.js" data-obsidian-blocking></script>
```

Everything else in the field — `<meta>`, `<link rel="preconnect">`, HTML comments, loose text, inline scripts — comes out byte for byte as it went in. The blob is never parsed and re-serialised; only the attribute list of a matching open tag is rewritten in place.

### The advice that actually applies

Before turning either flag on, the right move is almost always to **take the script out of head includes and load it properly from the theme**, where it can be ordered, bundled, deferred deliberately and measured. These flags are damage control for content you do not own or cannot move — not a substitute for loading a script correctly.

---

## Next Steps

- [Structured Data (JSON-LD)](0130-structured-data.md) — the schema.org half of the same story.
- [Performance](0160-performance.md) — critical CSS, the native build flags and Varnish.
{% endraw %}
