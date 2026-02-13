# Tailwind Configuration

**{{ config.extra.components_name }}** uses **Tailwind CSS 4**, which is **CSS-first**: design tokens are declared in CSS (`@import "tailwindcss";` then `@theme { … }`), not in a JavaScript config. A theme declares its tokens in `web/css/theme.source.css` (see [CSS Configuration](../themes/0030-css-configuration.md)); a module contributes tokens/utilities through its `view/frontend/web/css/module.extend.css`.

> For Tailwind 4 customization (the `@theme` block, the `@utility` and `@source` directives) refer to the official documentation:
> [Tailwind CSS — Theme variables](https://tailwindcss.com/docs/theme) · [Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files).

---

## How classes are detected (source scanning)

Tailwind only generates the utility classes it actually finds in your source files. In this stack Tailwind's **automatic detection does not reach the Magento tree** (its base path is the Vite harness, not `app/`), so the engine registers the sources explicitly — with **full inheritance**, exactly like it already does for components:

- **Vue/JS components** of every compatible module and of the theme, resolved through the theme → parent chain.
- **Twig/phtml templates** — the `view/frontend/templates` directory of every compatible module, **plus the whole theme inheritance chain** (theme → parent → …).

As a result, a class used in **any** module template/component, or in **any** theme of the inheritance chain (including a parent theme), is generated automatically. You do **not** need to add a manual `@source` for your templates.

---

## Opting a module out of scanning

A theme can exclude specific modules from class detection with `ignoredTailwindConfigFromModules` in its `web/theme.config.js`:

```javascript
export default {
    // Exclude these modules' components AND templates from Tailwind scanning…
    ignoredTailwindConfigFromModules: ['Vendor_ModuleA', 'Vendor_ModuleB'],
    // …or exclude every module with the literal string "all".
    // ignoredTailwindConfigFromModules: 'all',
};
```

- A **list of module names** excludes those modules' components **and** templates from the generated `@source` set.
- The literal **`"all"`** excludes every module. The theme's own files are **always** scanned.
- The list **merges down the theme inheritance chain**: a child theme inherits its parent's exclusions and can add more (the same merge applied to `ignoredCssFromModules`).

This is the source-scanning counterpart of [`ignoredCssFromModules`](../themes/0030-css-configuration.md), which excludes a module's **CSS** (`module.extend.css`) from the build.

---

## Prioritization & overrides

- Module CSS (`module.extend.css`) is imported **before** the theme CSS, so a theme's `theme.source.css` can override module tokens through the normal CSS cascade.
- Module load order follows the `sequence` declared in each `module.xml`. See the [official Magento documentation](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

---

## Legacy note (Tailwind 3)

Earlier versions used a `tailwind` object with `content` / `theme.extend` / `plugins` inside `module.config.js`. **Tailwind 4 is CSS-first and that object is no longer read.** Tokens and utilities now live in `module.extend.css` / `theme.source.css`, and class detection is handled by the engine as described above — there is no `content` array to maintain.
