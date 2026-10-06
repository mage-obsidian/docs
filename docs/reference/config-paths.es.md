---
description: "Las rutas de core_config_data que lee el frontend de MageObsidian, con etiquetas del admin, valores por defecto y alcance."
---
# Rutas de configuración

Estas son las rutas de `core_config_data` que lee el frontend de MageObsidian. Se editan en **Stores → Configuration → MageObsidian → Frontend**, o con `bin/magento config:set <ruta> <valor>`. El valor por defecto sale del `etc/config.xml` del módulo; `—` significa que la ruta no trae un valor por defecto. Las etiquetas del admin se muestran tal como aparecen en la interfaz.

## Hot Module Replacement

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/hmr/enabled` | Enable HMR | `0` | Vista de tienda |

## Vite Dev Server

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/dev_server/host` | Server Host | `localhost` | Global |
| `mage_obsidian/dev_server/port` | Server Port | `5173` | Global |
| `mage_obsidian/dev_server/secure` | Secure HMR (wss) | `0` | Global |
| `mage_obsidian/dev_server/hmr_path` | HMR Path | `/__vite_ping` | Global |
| `mage_obsidian/dev_server/public_host` | Public Host | `localhost` | Global |
| `mage_obsidian/dev_server/allowed_hosts` | Allowed Hosts | `localhost` | Global |

## SEO

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/seo/structured_data_enabled` | Emit Structured Data (JSON-LD) | `1` | Vista de tienda |
| `mage_obsidian/seo/webpage_enabled` | Emit WebPage Node | `1` | Vista de tienda |
| `mage_obsidian/seo/organization_logo` | Organization Logo | — | Vista de tienda |
| `mage_obsidian/seo/organization_description` | Organization Description | — | Vista de tienda |
| `mage_obsidian/seo/organization_same_as` | Organization sameAs URIs | — | Vista de tienda |
| `mage_obsidian/seo/organization_contact_type` | Contact Point Type | `customer support` | Vista de tienda |
| `mage_obsidian/seo/organization_address_enabled` | Emit Postal Address | `1` | Vista de tienda |
| `mage_obsidian/seo/product_brand_attribute` | Brand Attribute Code | `manufacturer` | Vista de tienda |
| `mage_obsidian/seo/product_gtin_attribute` | GTIN Attribute Code | — | Vista de tienda |
| `mage_obsidian/seo/product_mpn_attribute` | MPN Attribute Code | — | Vista de tienda |
| `mage_obsidian/seo/product_condition` | Item Condition | `NewCondition` | Vista de tienda |
| `mage_obsidian/seo/product_image_limit` | Product Images In Schema | `3` | Vista de tienda |
| `mage_obsidian/seo/price_valid_until_days` | priceValidUntil Horizon (days) | `0` | Vista de tienda |
| `mage_obsidian/seo/canonical_enabled` | Emit a Canonical URL | `1` | Vista de tienda |
| `mage_obsidian/seo/canonical_query_params` | Query Parameters Kept in the Canonical | `p,q` | Vista de tienda |
| `mage_obsidian/seo/social_meta_enabled` | Emit Open Graph and Twitter Card Metadata | `1` | Vista de tienda |
| `mage_obsidian/seo/social_image` | Fallback Share Image | — | Vista de tienda |
| `mage_obsidian/seo/twitter_site` | Twitter Account | — | Vista de tienda |
| `mage_obsidian/seo/meta_description_fallback` | Derive the Meta Description from the Page | `1` | Vista de tienda |
| `mage_obsidian/seo/robots_directives` | Extra Robots Directives | `max-image-preview:large,max-snippet:-1,max-video-preview:-1` | Vista de tienda |
| `mage_obsidian/seo/manifest_enabled` | Serve a Web App Manifest | `1` | Vista de tienda |
| `mage_obsidian/seo/manifest_display` | Manifest Display Mode | `standalone` | Vista de tienda |
| `mage_obsidian/seo/manifest_theme_color` | Manifest Theme Colour | `#ffffff` | Vista de tienda |
| `mage_obsidian/seo/manifest_background_color` | Manifest Background Colour | `#ffffff` | Vista de tienda |

## Checkout

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/checkout/layout_mode` | Checkout Layout | `stepped` | Vista de tienda |
| `mage_obsidian/checkout/cacheable_shell` | Cacheable Checkout Shell | `0` | Vista de tienda |

## HTML Head Includes

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/head/includes_defer_scripts` | Defer Scripts In Head Includes | `0` | Vista de tienda |
| `mage_obsidian/head/includes_defer_styles` | Defer Stylesheets In Head Includes | `0` | Vista de tienda |

## Storefront

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/storefront/optimistic_ui` | Optimistic UI | `1` | Vista de tienda |
| `mage_obsidian/storefront/island_preload` | Preload Eager Island Chunks | `0` | Vista de tienda |

## Product Listing

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/listing/fragments_enabled` | Serve Filters and Pagination as Fragments | `1` | Vista de tienda |

## Appearance

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/appearance/enabled` | Enable the Appearance Selector | `0` | Vista de tienda |

## Speculative Loading

| Ruta | Etiqueta en el admin | Valor por defecto | Alcance |
|---|---|---|---|
| `mage_obsidian/speculation/enabled` | Enable Speculative Loading | `1` | Vista de tienda |
| `mage_obsidian/speculation/mode` | Mode | `prefetch` | Vista de tienda |
| `mage_obsidian/speculation/eagerness` | Eagerness | `moderate` | Vista de tienda |
| `mage_obsidian/speculation/exclude_paths` | Exclude URL Patterns | `customer`<br>`checkout`<br>`wishlist`<br>`logout`<br>`auth`<br>`search`<br>`download`<br>`redirect`<br>`rewrite`<br>`stores`<br>`productalert`<br>*Un token por línea.* | Vista de tienda |
| `mage_obsidian/speculation/exclude_extensions` | Exclude File Extensions | `pdf,zip` | Vista de tienda |
| `mage_obsidian/speculation/exclude_selectors` | Exclude Selectors | `.no-prefetch`<br>*Un token por línea.* | Vista de tienda |
| `mage_obsidian/navigation/retain` | Hold the Previous Page Until the Next Is Ready | `1` | Vista de tienda |

