# Adobe Commerce

**{{ config.extra.components_name }}** installs and runs on **Adobe Commerce 2.4.9** with the
same packages as Magento Open Source. This page covers what differs: the Composer keys, the
packages that do not apply, and the problems you may meet on the way.

## What "compatible" means here

The published packages were installed on Adobe Commerce 2.4.9 (PHP 8.5, `default` mode) and
the storefront was walked end to end in a browser: home, search, category, product page, cart,
a guest checkout through to a placed order, sign-up, the customer account, sign-out and
sign-in. No console, network or server log errors appeared, and the order was recorded with
the right totals.

What that does **not** cover:

- **Commerce-only storefront features** — gift cards, store credit, reward points, gift
  registry, order by SKU, invitations and the rest — have no MageObsidian storefront yet. Run
  `bin/magento mage-obsidian:frontend:doctor` to see which of them your store has enabled.
- **Adobe Commerce Cloud.** Its build runs without a database, which the frontend contract
  generation does not support yet.
- **Payment gateways.** Only Check / Money order was exercised.

## Requirements

- **Adobe Commerce 2.4.7 or later.** The core package requires Magento 2.4.7.
- **PHP 8.3 or later.** Every MageObsidian Magento module declares `"php": ">=8.3"`.
- **Node.js 22.13 or later** and **pnpm 11**, the version the Vite harness pins.
- **Keys for `repo.magento.com` with Commerce entitlement**, in the project's `auth.json`.
  MageObsidian itself comes from Packagist and needs no keys.

## Installation

```bash
composer require mage-obsidian/component-modern-frontend mage-obsidian/theme-default
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
pnpm --prefix vite install --frozen-lockfile
```

Assign the theme under **Content → Design → Configuration** (**MageObsidian — Default
(Obsidian)**), then build and publish the assets:

```bash
bin/magento setup:static-content:deploy -f en_US
bin/magento cache:flush
```

`setup:static-content:deploy` runs the Vite build for every MageObsidian theme and checks that
its output was published. A theme with no build is reported; set
`MAGE_OBSIDIAN_STRICT_DEPLOY=1` to turn that report into a failed deploy.

In production mode, run `bin/magento setup:di:compile` before the static content deploy, as
for any Magento store.

## Development

HMR is **off by default**, so a fresh install serves the built assets. To work with the Vite
dev server, follow [Development](development.md):

```bash
bin/magento mage-obsidian:frontend:dev --up
```

## Packages that do not apply

The standard install above pulls only what the theme needs. Two packages in the MageObsidian
organisation are not part of it and should stay out of an Adobe Commerce store:

- **`mage-obsidian/module-inventory-stock-visualizer`** adapts a panel from the MSI fork
  `jeanmarcos/inventory`. Adobe Commerce does not ship the module it depends on, so Composer
  refuses it. That is expected.
- **`mage-obsidian/module-showcase`** is the feature switchboard of the demo store.

## Troubleshooting

**Every asset returns 404 under `…/vite_generated/…` and no island mounts.** HMR is on without a
dev server running. Releases before core 2.20.0 shipped HMR enabled. Turn it off:

```bash
bin/magento mage-obsidian:frontend:hmr --disable
```

**`There are no commands defined in the "mage-obsidian" namespace`.** Look in
`var/log/exception.log` for `Failed to load core Magento commands`. Magento drops every
module command when one of them cannot be built, which happens when `generated/code` holds an
interceptor for an older constructor. Rebuild the generated code with
`bin/magento setup:di:compile`, or delete `generated/code` and run `bin/magento cache:clean config`.

**`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` after upgrading `component-modern-frontend`.**
Versions before 2.6.0 placed the pnpm store elsewhere, and pnpm refuses to rebuild
`vite/node_modules` without a terminal. Delete `vite/node_modules` once and install again.

**`ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION`.** pnpm refuses a package published less than a
day ago. Wait, or exempt that one version for the install:

```bash
pnpm_config_minimum_release_age_exclude='["mage-obsidian@3.1.0"]' pnpm --prefix vite install --frozen-lockfile
```

**A guest is sent to sign in instead of reaching checkout.** The cart holds a downloadable
product and `catalog/downloadable/disable_guest_checkout` is on, which is Magento's default.
This is native behaviour; set that option to **No** to let guests buy downloadable products.
