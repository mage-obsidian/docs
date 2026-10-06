---
description: "Cada paquete de MageObsidian, dónde se publica, a qué tren de versiones pertenece y si una tienda lo necesita."
---

# Mapa de paquetes

Todo lo que publica MageObsidian, con su registro, su tren de versiones y su función. Los dos trenes se describen en [Versionado y soporte](../project/versioning.md#two-release-trains).

## Framework

El tren del framework está en 4.0.0. Los cinco paquetes llevan la misma versión.

| Paquete | Registro | Tren | Obligatorio / opcional | Fuente |
|---|---|---|---|---|
| `mage-obsidian/module-modern-frontend` | Packagist | Framework | Obligatorio | [`module-modern-frontend`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend) |
| `mage-obsidian/module-modern-frontend-cli` | Packagist | Framework | Obligatorio (lo instala `component-modern-frontend`) | [`module-modern-frontend-cli`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend-cli) |
| `mage-obsidian/module-modern-frontend-twig` | Packagist | Framework | Opcional (lo instala `component-modern-frontend`; [se puede deshabilitar](../guides/twig.md#deshabilitar-twig)) | [`module-modern-frontend-twig`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend-twig) |
| `mage-obsidian/component-modern-frontend` | Packagist | Framework | Obligatorio (el arnés de build de Vite) | [`component-modern-frontend`]({{ config.extra.gh_framework_url }}/tree/master/packages/component-modern-frontend) |
| `mage-obsidian` | npm | Framework | Obligatorio (el motor de build JS) | [`js-package-utils`]({{ config.extra.gh_js_utils_url }}) |

## Storefront

El tren del storefront está en 4.0.1. Los diecinueve paquetes llevan la misma versión. `theme-default` incorpora `theme-base`; los módulos que `theme-base` requiere llegan con él.

| Paquete | Registro | Tren | Obligatorio / opcional | Fuente |
|---|---|---|---|---|
| `mage-obsidian/module-catalog` | Packagist | Storefront | Lo requiere `theme-base` | [`module-catalog`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-catalog) |
| `mage-obsidian/module-catalog-search` | Packagist | Storefront | Lo requiere `theme-base` | [`module-catalog-search`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-catalog-search) |
| `mage-obsidian/module-checkout` | Packagist | Storefront | Lo requiere `theme-base` | [`module-checkout`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-checkout) |
| `mage-obsidian/module-customer` | Packagist | Storefront | Lo requiere `theme-base` | [`module-customer`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-customer) |
| `mage-obsidian/module-downloadable` | Packagist | Storefront | Lo requiere `theme-base` | [`module-downloadable`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-downloadable) |
| `mage-obsidian/module-gift-message` | Packagist | Storefront | Lo requiere `theme-base` | [`module-gift-message`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-gift-message) |
| `mage-obsidian/module-instant-purchase` | Packagist | Storefront | Lo requiere `theme-base` | [`module-instant-purchase`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-instant-purchase) |
| `mage-obsidian/module-multishipping` | Packagist | Storefront | Lo requiere `theme-base` | [`module-multishipping`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-multishipping) |
| `mage-obsidian/module-persistent` | Packagist | Storefront | Lo requiere `theme-base` | [`module-persistent`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-persistent) |
| `mage-obsidian/module-product-alert` | Packagist | Storefront | Lo requiere `theme-base` | [`module-product-alert`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-product-alert) |
| `mage-obsidian/module-review` | Packagist | Storefront | Lo requiere `theme-base` | [`module-review`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-review) |
| `mage-obsidian/module-sales` | Packagist | Storefront | Lo requiere `theme-base` | [`module-sales`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-sales) |
| `mage-obsidian/module-search` | Packagist | Storefront | Opcional (`theme-base` no lo requiere) | [`module-search`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-search) |
| `mage-obsidian/module-send-friend` | Packagist | Storefront | Lo requiere `theme-base` | [`module-send-friend`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-send-friend) |
| `mage-obsidian/module-showcase` | Solo VCS, no está en Packagist | Storefront | Opcional (herramienta de la demo) | [`module-showcase`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-showcase) |
| `mage-obsidian/module-storefront` | Packagist | Storefront | Lo requiere `theme-base` | [`module-storefront`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-storefront) |
| `mage-obsidian/module-vault` | Packagist | Storefront | Lo requiere `theme-base` | [`module-vault`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-vault) |
| `mage-obsidian/module-wishlist` | Packagist | Storefront | Lo requiere `theme-base` | [`module-wishlist`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-wishlist) |
| `mage-obsidian/theme-base` | Packagist | Storefront | Obligatorio (el tema base) | [`theme-base`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/theme-base) |

## Fuera de los dos trenes

Se versionan por su cuenta.

| Paquete | Registro | Tren | Obligatorio / opcional | Fuente |
|---|---|---|---|---|
| `mage-obsidian/theme-default` (4.0.0) | Packagist | Versionado propio | Obligatorio para el skin OBSIDIAN; opcional si escribes tu propio tema | [`theme-default`]({{ config.extra.gh_theme_default_url }}) |
| `mage-obsidian/module-inventory-stock-visualizer` (2.0.0) | Repositorio privado, no está en Packagist | Versionado propio | Opcional | Repositorio privado |

`module-showcase` es el panel de funcionalidades de la tienda de demo. Instálalo desde su repositorio, no con `composer require`. `module-inventory-stock-visualizer` adapta un panel del fork de MSI `jeanmarcos/inventory` y no aplica a Adobe Commerce.
