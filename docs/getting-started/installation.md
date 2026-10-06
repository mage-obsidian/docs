# Installation

The installation of **{{ config.site_name }}** consists of two main parts: the **components**, which are available now, and the **theme**, which is published on Packagist as `mage-obsidian/theme-default`.

## {{ config.extra.components_name }}

The components are the core of **{{ config.site_name }}**, designed to provide a modern and efficient frontend for Magento. Follow these steps to install them:

### 1. Install via Composer

Use Composer to add the components to your project:

```bash
composer require mage-obsidian/component-modern-frontend
```

### 2: Install Node Dependencies

Ensure all necessary node dependencies are installed:

#### pnpm
```bash
pnpm --prefix vite install
```

#### npm
```bash
npm --prefix vite install
```

### 3. Configure Magento

Update Magento's configuration to register the components:

```bash
bin/magento setup:upgrade
```

### 4. Generate initial configuration

Run the following command to generate the initial configuration for the frontend components:

```bash
bin/magento mage-obsidian:frontend:config --generate
```

### 5. Ready to develop

The components are configured and ready to be used in your project! You can now start developing your theme with the modern tools offered by **{{ config.extra.components_name }}**.

> **Note:** The install includes the optional [Twig engine](../guides/twig.md) by default (a `.twig` engine alongside `.phtml`). It changes nothing about your existing `.phtml` templates; if you don't want it, [disable it](../guides/twig.md#disabling-twig) with `bin/magento module:disable MageObsidian_ModernFrontendTwig`.

## More Information

For more details on customizing the components, starting theme development, and understanding all the benefits and advantages, see the [Detailed Components Documentation](../why/index.md).

---

## {{ config.extra.theme_name }}

The theme based on **{{ config.extra.components_name }}** is available on Packagist as `mage-obsidian/theme-default`. It provides a modern, SEO-friendly, and highly customizable design for Magento stores.

## More Information

For more information about the theme, visit the [Theme](../guides/themes/obsidian.md) section.
