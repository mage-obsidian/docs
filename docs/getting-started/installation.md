# Installation

{{ verified('install') }}

Steps 1 to 6 are the recipe the release matrix runs on every platform listed in [Compatibility](compatibility.md): the published packages, installed from Packagist on a clean store and built, followed by a storefront smoke check. Step 7 is the production step and is not part of the matrix run. With `^4.0`, Composer installs the storefront modules 4.0.1 and the framework and `theme-default` 4.0.0. Check the [requirements](requirements.md) first. On Adobe Commerce, read [Install on Adobe Commerce](adobe-commerce.md) as well.

## 1. Require the theme

`mage-obsidian/theme-default` pulls in `theme-base`, the framework, the Vite harness and the full storefront module stack:

```bash
composer require mage-obsidian/theme-default:^4.0
```

## 2. Register the modules

```bash
bin/magento setup:upgrade
```

## 3. Activate the theme

In the Admin, go to **Content › Design › Configuration**, edit the scope you want and pick **MageObsidian — Default (Obsidian)** as the applied theme.

## 4. Generate the PHP ↔ JS contract

```bash
bin/magento mage-obsidian:frontend:config --generate
```

## 5. Prepare the Vite harness

The `vite/` harness must be in the Magento root. If `vite/package.json` is missing, copy it from the installed package:

```bash
[ -f vite/package.json ] || { rm -rf vite && cp -r vendor/mage-obsidian/component-modern-frontend/vite vite; }
```

Create `vite/.env` from `vite/.env.sample` with the values for your host, then install the Node dependencies exactly as locked:

```bash
cd vite
pnpm install --frozen-lockfile
```

The `.env` carries `VITE_SERVER_HOST`, `VITE_SERVER_PORT`, `VITE_SERVER_SECURE`, `VITE_HMR_PATH`, `MAGENTO_HOST` and `VITE_SERVER_ALLOWED_HOSTS`. Without it, the build stops in a non-interactive shell.

## 6. Build the theme

From the `vite/` directory:

```bash
pnpm build:theme MageObsidian/default
```

## 7. Deploy the static content and flush the cache

Back in the Magento root:

```bash
bin/magento setup:static-content:deploy
bin/magento cache:flush
```

Open the storefront: the home page renders with its Vue islands. For production, see [Deploy to production](deploy.md).

> **Note:** The install includes the optional [Twig engine](../guides/twig.md) by default (a `.twig` engine alongside `.phtml`). It changes nothing about your existing `.phtml` templates; if you don't want it, [disable it](../guides/twig.md#disabling-twig) with `bin/magento module:disable MageObsidian_ModernFrontendTwig`.

## Next steps

- [Your first child theme](first-theme.md) to customize the theme.
- [Development workflow](development.md) for live reload with HMR.
- [Why MageObsidian](../why/index.md) and the [theme guide](../guides/themes/obsidian.md).
