---
description: "MageObsidian 4.0 is the first stable release: a stable contract for all of 4.x, two release trains, and a tested compatibility table."
---

# What's new in 4.0

## 4.0 is stable

MageObsidian 4.0 is the first stable release. From here on, the surface listed in the [Reference](../reference/index.md) does not change incompatibly until 5.0. What that covers, and how long each line is supported, is in [Versioning & support](../project/versioning.md).

## Same packages, same code

No package was renamed. The Packagist and npm names are the ones you already use.

4.0.0 shipped the last 2.x and 3.x code plus SPDX license headers. Those headers caused a regression, fixed the same day in storefront 4.0.1: templates failed on PHP 8.3 and 8.4, and a template variable was missing on Magento 2.4.7.

## Two release trains

The framework and the storefront are versioned separately. Each train versions all of its packages together.

- **Framework:** `module-modern-frontend`, `module-modern-frontend-cli`, `module-modern-frontend-twig`, `component-modern-frontend` and the npm package `mage-obsidian`.
- **Storefront:** the storefront modules and `theme-base`.

The storefront declares the framework line it needs, so a storefront release never installs against a framework it was not built for. See [Two release trains](../project/versioning.md#two-release-trains).

## Where the code lives

The framework lives in the [`mage-obsidian/framework`]({{ config.extra.gh_framework_url }}) monorepo and the storefront in [`mage-obsidian/storefront`]({{ config.extra.gh_storefront_monorepo_url }}). The per-package repositories are read-only mirrors: open issues and pull requests in the monorepos. `theme-default` stays in [its own repository]({{ config.extra.gh_theme_default_url }}).

## Compatibility

Every combination of Magento Open Source and Mage-OS 2.4.7, 2.4.8 and 2.4.9 passed on 2026-10-06, with framework 4.0.0 and storefront 4.0.1. Magento and Mage-OS 2.4.7 is the floor and there is no ceiling: newer releases are expected to work and are added to the table once tested. See the [compatibility table](../getting-started/compatibility.md).

## Upgrading from 3.x

The upgrade changes your version constraints and nothing else. Follow [Upgrading from 3.x to 4.0](../upgrade/3-to-4.md).

## What is not verified yet

Some areas have not been tested to the same depth as the rest. They are listed, with their status, in [Known scope](../project/known-scope.md).
