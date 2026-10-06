---
description: Which Magento and Mage-OS versions each MageObsidian release was installed and tested on.
---

# Compatibility

{{ verified('matrix') }}

Every MageObsidian release is installed from Packagist on a clean store for each platform below,
and must render the storefront with its Vue islands. A ✅ means that combination passed; a ❌ means
it was tested and failed; ⏳ means it has not been run for this release yet.

## {{ compatibility.release_label }}

{{ compat_table() }}

Storefront 4.0.0 failed on PHP 8.3 and 8.4 and on Magento 2.4.7. Storefront 4.0.1 fixed it, so the
minimum storefront release is 4.0.1; Composer picks it with `^4.0`.

The packages declare a floor (`magento/framework >=103.0.7`, Magento 2.4.7) and no ceiling, so
Composer will not stop you on a newer Magento: check this table before upgrading Magento.

## Why a release does not install

    composer why-not mage-obsidian/theme-default 4.0.0

## Release trains

The framework and the storefront each release all their packages under one version; see
[Versioning & support](../project/versioning.md#two-release-trains).
