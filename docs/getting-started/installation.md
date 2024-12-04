# Installation

The installation of **{{ config.site_name }}** consists of two main parts: the **components**, which are already available, and the **theme**, which is still under development.

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
bin/magento obsidian:frontend:config --generate
```

### 5. Ready to develop

The components are configured and ready to be used in your project! You can now start developing your theme with the modern tools offered by **{{ config.extra.components_name }}**.

## More Information

For more details on customizing the components, starting theme development, and understanding all the benefits and advantages, see the [Detailed Components Documentation](../../components).

---

## {{ config.extra.theme_name }}

The theme based on **{{ config.extra.components_name }}** is still under development and is not yet available for installation. Once completed, it will provide a modern, SEO-friendly, and highly customizable design for Magento stores.

### Current Status
- The design is in progress and will be available soon.
- In the meantime, you can explore the components to start building custom solutions.

## More Information

For more information about the theme, visit the [Theme](../../theme) section.
