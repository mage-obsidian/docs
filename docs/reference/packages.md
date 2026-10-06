---
description: "Every MageObsidian package, where it is published, which release train it belongs to and whether a store needs it."
---

# Package map

Everything MageObsidian publishes, with its registry, release train and role. The two trains are described in [Versioning & support](../project/versioning.md#two-release-trains).

## Framework

The framework train is at 4.0.1. All five packages carry the same version.

| Package | Registry | Train | Required / optional | Source |
|---|---|---|---|---|
| `mage-obsidian/module-modern-frontend` | Packagist | Framework | Required | [`module-modern-frontend`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend) |
| `mage-obsidian/module-modern-frontend-cli` | Packagist | Framework | Required (installed by `component-modern-frontend`) | [`module-modern-frontend-cli`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend-cli) |
| `mage-obsidian/module-modern-frontend-twig` | Packagist | Framework | Optional (installed by `component-modern-frontend`; [can be disabled](../guides/twig.md#disabling-twig)) | [`module-modern-frontend-twig`]({{ config.extra.gh_framework_url }}/tree/master/packages/module-modern-frontend-twig) |
| `mage-obsidian/component-modern-frontend` | Packagist | Framework | Required (the Vite build harness) | [`component-modern-frontend`]({{ config.extra.gh_framework_url }}/tree/master/packages/component-modern-frontend) |
| `mage-obsidian` | npm | Framework | Required (the JS build engine) | [`js-package-utils`]({{ config.extra.gh_js_utils_url }}) |

## Storefront

The storefront train is at 4.0.1. All nineteen packages carry the same version. `theme-base` is pulled in by `theme-default`; the modules that `theme-base` requires come with it.

| Package | Registry | Train | Required / optional | Source |
|---|---|---|---|---|
| `mage-obsidian/module-catalog` | Packagist | Storefront | Required by `theme-base` | [`module-catalog`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-catalog) |
| `mage-obsidian/module-catalog-search` | Packagist | Storefront | Required by `theme-base` | [`module-catalog-search`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-catalog-search) |
| `mage-obsidian/module-checkout` | Packagist | Storefront | Required by `theme-base` | [`module-checkout`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-checkout) |
| `mage-obsidian/module-customer` | Packagist | Storefront | Required by `theme-base` | [`module-customer`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-customer) |
| `mage-obsidian/module-downloadable` | Packagist | Storefront | Required by `theme-base` | [`module-downloadable`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-downloadable) |
| `mage-obsidian/module-gift-message` | Packagist | Storefront | Required by `theme-base` | [`module-gift-message`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-gift-message) |
| `mage-obsidian/module-instant-purchase` | Packagist | Storefront | Required by `theme-base` | [`module-instant-purchase`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-instant-purchase) |
| `mage-obsidian/module-multishipping` | Packagist | Storefront | Required by `theme-base` | [`module-multishipping`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-multishipping) |
| `mage-obsidian/module-persistent` | Packagist | Storefront | Required by `theme-base` | [`module-persistent`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-persistent) |
| `mage-obsidian/module-product-alert` | Packagist | Storefront | Required by `theme-base` | [`module-product-alert`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-product-alert) |
| `mage-obsidian/module-review` | Packagist | Storefront | Required by `theme-base` | [`module-review`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-review) |
| `mage-obsidian/module-sales` | Packagist | Storefront | Required by `theme-base` | [`module-sales`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-sales) |
| `mage-obsidian/module-search` | Packagist | Storefront | Optional (`theme-base` does not require it) | [`module-search`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-search) |
| `mage-obsidian/module-send-friend` | Packagist | Storefront | Required by `theme-base` | [`module-send-friend`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-send-friend) |
| `mage-obsidian/module-showcase` | VCS only, not on Packagist | Storefront | Optional (demo tool) | [`module-showcase`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-showcase) |
| `mage-obsidian/module-storefront` | Packagist | Storefront | Required by `theme-base` | [`module-storefront`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-storefront) |
| `mage-obsidian/module-vault` | Packagist | Storefront | Required by `theme-base` | [`module-vault`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-vault) |
| `mage-obsidian/module-wishlist` | Packagist | Storefront | Required by `theme-base` | [`module-wishlist`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/module-wishlist) |
| `mage-obsidian/theme-base` | Packagist | Storefront | Required (the base theme) | [`theme-base`]({{ config.extra.gh_storefront_monorepo_url }}/tree/master/packages/theme-base) |

## Outside the two trains

Versioned on their own.

| Package | Registry | Train | Required / optional | Source |
|---|---|---|---|---|
| `mage-obsidian/theme-default` (4.0.0) | Packagist | Own versioning | Required for the OBSIDIAN skin; optional if you write your own theme | [`theme-default`]({{ config.extra.gh_theme_default_url }}) |
| `mage-obsidian/module-inventory-stock-visualizer` (2.0.0) | Private repository, not on Packagist | Own versioning | Optional | Private repository |

`module-showcase` is the feature switchboard of the demo store. Install it from its repository, not with `composer require`. `module-inventory-stock-visualizer` adapts a panel of the MSI fork `jeanmarcos/inventory` and does not apply to Adobe Commerce.
