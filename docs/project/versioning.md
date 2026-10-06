---
description: "How MageObsidian versions its two release trains, what the 4.x contract covers, the deprecation policy and which versions are supported."
---

# Versioning & support

## Semantic versioning

Every package follows [semantic versioning](https://semver.org): `MAJOR.MINOR.PATCH`.

- **MAJOR** may break the contract. It is the only release that removes anything.
- **MINOR** adds features and deprecations without breaking the contract.
- **PATCH** fixes bugs and changes nothing else.

## Two release trains { #two-release-trains }

MageObsidian ships two independent release trains. Each one versions all of its packages together, so every package in a train always carries the same version.

| Train | Packages | Repository |
|---|---|---|
| Framework | `module-modern-frontend`, `module-modern-frontend-cli`, `module-modern-frontend-twig`, `component-modern-frontend`, npm `mage-obsidian` | [`mage-obsidian/framework`]({{ config.extra.gh_framework_url }}) |
| Storefront | the storefront modules and `theme-base` | [`mage-obsidian/storefront`]({{ config.extra.gh_storefront_monorepo_url }}) |

The storefront depends on the framework and declares the framework line it needs, so the two trains are related by that requirement and not by a shared version number. Storefront 4.0.1 requires framework 4.x; a storefront patch release does not force a framework release, and the other way around.

`theme-default` is versioned on its own and lives in [its repository]({{ config.extra.gh_theme_default_url }}).

## What the 4.x contract covers

The contract is the surface listed in the [Reference](../reference/index.md):

- CLI commands and their options.
- Configuration paths.
- Environment variables.
- Keys of `theme.config.js` and `module.config.ts`.
- The compatibility XML and the contract schema version.
- Twig functions and filters.
- Package names.
- `Vendor_Module::path` specifiers.
- The JS interceptor API.

Anything that is not in the Reference is not part of the contract and may change in any release.

## Deprecation policy { #deprecation-policy }

Nothing in the contract is removed in a minor or a patch. A deprecation is marked in a minor release, announced in the [Upgrade notes](../upgrade/index.md) and removed in the next major.

## Supported versions

| Line | Support |
|---|---|
| Latest 4.x minor | Receives fixes. |
| 3.x | Frozen. Only emergency hotfixes, published from a `3.x` branch of the affected repository. |

4.x requires PHP 8.3+, Node 22+, pnpm 11+ and Magento Open Source or Mage-OS 2.4.7+, as shown in the [compatibility table](../getting-started/compatibility.md).

Questions and reports go to the Discussions of the [framework]({{ config.extra.gh_discussions_framework }}) and [storefront]({{ config.extra.gh_discussions_storefront }}) monorepos.

## Constraints in your composer.json

Use `^4.0` for every MageObsidian package:

```json
{
    "require": {
        "mage-obsidian/module-modern-frontend": "^4.0"
    }
}
```

No ceiling is needed. `^4.0` accepts every 4.x release and stops at 5.0, and the contract guarantees that nothing in 4.x breaks you. The Magento and Mage-OS versions are a floor too, so a newer Magento does not require a new constraint.
