---
description: "The core_config_data paths the MageObsidian frontend reads, with admin labels, defaults and scope."
---
# Configuration paths

These are the `core_config_data` paths the MageObsidian frontend reads. Edit them under **Stores → Configuration → MageObsidian → Frontend**, or with `bin/magento config:set <path> <value>`. The default comes from the module's `etc/config.xml`; `—` means the path ships without a default. Admin labels are shown as they appear in the interface.

## Hot Module Replacement

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/hmr/enabled` | Enable HMR | `0` | Store View |

## Vite Dev Server

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/dev_server/host` | Server Host | `localhost` | Global |
| `mage_obsidian/dev_server/port` | Server Port | `5173` | Global |
| `mage_obsidian/dev_server/secure` | Secure HMR (wss) | `0` | Global |
| `mage_obsidian/dev_server/hmr_path` | HMR Path | `/__vite_ping` | Global |
| `mage_obsidian/dev_server/public_host` | Public Host | `localhost` | Global |
| `mage_obsidian/dev_server/allowed_hosts` | Allowed Hosts | `localhost` | Global |

## SEO

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/seo/structured_data_enabled` | Emit Structured Data (JSON-LD) | `1` | Store View |
| `mage_obsidian/seo/webpage_enabled` | Emit WebPage Node | `1` | Store View |
| `mage_obsidian/seo/organization_logo` | Organization Logo | — | Store View |
| `mage_obsidian/seo/organization_description` | Organization Description | — | Store View |
| `mage_obsidian/seo/organization_same_as` | Organization sameAs URIs | — | Store View |
| `mage_obsidian/seo/organization_contact_type` | Contact Point Type | `customer support` | Store View |
| `mage_obsidian/seo/organization_address_enabled` | Emit Postal Address | `1` | Store View |
| `mage_obsidian/seo/product_brand_attribute` | Brand Attribute Code | `manufacturer` | Store View |
| `mage_obsidian/seo/product_gtin_attribute` | GTIN Attribute Code | — | Store View |
| `mage_obsidian/seo/product_mpn_attribute` | MPN Attribute Code | — | Store View |
| `mage_obsidian/seo/product_condition` | Item Condition | `NewCondition` | Store View |
| `mage_obsidian/seo/product_image_limit` | Product Images In Schema | `3` | Store View |
| `mage_obsidian/seo/price_valid_until_days` | priceValidUntil Horizon (days) | `0` | Store View |
| `mage_obsidian/seo/canonical_enabled` | Emit a Canonical URL | `1` | Store View |
| `mage_obsidian/seo/canonical_query_params` | Query Parameters Kept in the Canonical | `p,q` | Store View |
| `mage_obsidian/seo/social_meta_enabled` | Emit Open Graph and Twitter Card Metadata | `1` | Store View |
| `mage_obsidian/seo/social_image` | Fallback Share Image | — | Store View |
| `mage_obsidian/seo/twitter_site` | Twitter Account | — | Store View |
| `mage_obsidian/seo/meta_description_fallback` | Derive the Meta Description from the Page | `1` | Store View |
| `mage_obsidian/seo/robots_directives` | Extra Robots Directives | `max-image-preview:large,max-snippet:-1,max-video-preview:-1` | Store View |
| `mage_obsidian/seo/manifest_enabled` | Serve a Web App Manifest | `1` | Store View |
| `mage_obsidian/seo/manifest_display` | Manifest Display Mode | `standalone` | Store View |
| `mage_obsidian/seo/manifest_theme_color` | Manifest Theme Colour | `#ffffff` | Store View |
| `mage_obsidian/seo/manifest_background_color` | Manifest Background Colour | `#ffffff` | Store View |

## Checkout

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/checkout/layout_mode` | Checkout Layout | `stepped` | Store View |
| `mage_obsidian/checkout/cacheable_shell` | Cacheable Checkout Shell | `0` | Store View |

## HTML Head Includes

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/head/includes_defer_scripts` | Defer Scripts In Head Includes | `0` | Store View |
| `mage_obsidian/head/includes_defer_styles` | Defer Stylesheets In Head Includes | `0` | Store View |

## Storefront

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/storefront/optimistic_ui` | Optimistic UI | `1` | Store View |
| `mage_obsidian/storefront/island_preload` | Preload Eager Island Chunks | `0` | Store View |

## Product Listing

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/listing/fragments_enabled` | Serve Filters and Pagination as Fragments | `1` | Store View |

## Appearance

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/appearance/enabled` | Enable the Appearance Selector | `0` | Store View |

## Speculative Loading

| Path | Admin label | Default | Scope |
|---|---|---|---|
| `mage_obsidian/speculation/enabled` | Enable Speculative Loading | `1` | Store View |
| `mage_obsidian/speculation/mode` | Mode | `prefetch` | Store View |
| `mage_obsidian/speculation/eagerness` | Eagerness | `moderate` | Store View |
| `mage_obsidian/speculation/exclude_paths` | Exclude URL Patterns | `customer`<br>`checkout`<br>`wishlist`<br>`logout`<br>`auth`<br>`search`<br>`download`<br>`redirect`<br>`rewrite`<br>`stores`<br>`productalert`<br>*One token per line.* | Store View |
| `mage_obsidian/speculation/exclude_extensions` | Exclude File Extensions | `pdf,zip` | Store View |
| `mage_obsidian/speculation/exclude_selectors` | Exclude Selectors | `.no-prefetch`<br>*One token per line.* | Store View |
| `mage_obsidian/navigation/retain` | Hold the Previous Page Until the Next Is Ready | `1` | Store View |

