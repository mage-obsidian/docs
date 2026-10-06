# Module configuration

## CSS Configuration

In **{{ config.extra.components_name }}**, including custom CSS from modules is straightforward and efficient. The system automatically tracks the following entry point in compatible modules:  
```
/var/www/html/app/code/Vendor/ModuleName/view/frontend/web/css/module.extend.css
```

This file will be included for each module that defines it, unless explicitly excluded by the theme configuration (more details on this functionality will be covered later).

### How It Works

1. **Import Order**  
    CSS files are loaded based on the **module priority** defined in Magento. The order is determined by the `sequence` configuration in each module’s `module.xml` file. This allows you to control the import order of module CSS. Additionally, all module CSS is loaded **before theme CSS**.

    > For more details on configuring the module load order, see the official Magento documentation:  
    [Configuring Component Load Order](https://developer.adobe.com/commerce/php/development/build/component-load-order).

    A typical import order might look like this:

    ```css
    /* Module CSS */
    @import "/var/www/html/app/code/Vendor/ModuleA/view/frontend/web/css/module.extend.css"; /* Module A */
    @import "/var/www/html/app/code/Vendor/ModuleB/view/frontend/web/css/module.extend.css"; /* Module B */
    
    /* Theme CSS */
    @import "/var/www/html/app/design/frontend/Vendor/ThemeParent/web/css/theme.source.css"; /* Parent theme */
    @import "/var/www/html/app/design/frontend/Vendor/CurrentTheme/web/css/theme.source.css"; /* Current theme */
    ```

    - **Modules**: If a module wants to include custom CSS, it should use the file located at `view/frontend/web/css/module.extend.css` as its entry point. **{{ config.extra.components_name }}** automatically tracks these files for compatible modules.
    - **Themes**: The CSS entry point for themes is always `theme.source.css`.

2. **Flexibility with Theme Configuration**  
    As mentioned earlier, the theme configuration allows you to **exclude CSS entries from specific modules**. This provides flexibility in determining which styles are included in the final build.

### Optimized CSS Output

**{{ config.extra.components_name }}** leverages **Tailwind CSS** and tree-shaking techniques to generate a single, optimized CSS file. This final file includes only the styles required for the frontend, ensuring minimal size and maximum performance.

### Key Benefits

- **Modularity**: CSS from modules is automatically integrated without additional effort.
- **Control**: Adjust the import order using the `sequence` configuration in `module.xml`, or selectively include/exclude module CSS via theme settings.
- **Performance**: The final optimized CSS file improves load times and reduces unnecessary styles.

## Module Configuration

In **{{ config.extra.components_name }}**, each compatible module can include additional configurations by creating a configuration file at:

```
view/frontend/web/module.config.ts
```

This file is an **ESM (ECMAScript module)** that `export default`s a configuration object read by **{{ config.extra.components_name }}**.

### How It Works

1. **Configuration File Loading**  
    Configuration files are loaded in the order defined by the `sequence` configuration in each module's `module.xml` file.
    
    > For more details on how to define the sequence of modules, see the official Magento documentation:  
    [Configuring Component Load Order](https://developer.adobe.com/commerce/php/development/build/component-load-order).

2. **Example Configuration File**  
    A basic example of a `module.config.ts` file might look like this:

    ```javascript
    export default {
         tailwind: {
              // Tailwind CSS configuration
         }
    };
    ```

    Currently, the only supported configuration option is for **Tailwind CSS**, but future updates will expand this functionality to allow additional module-specific options.

3. **Overriding Module Configurations**  
    Module configurations can be overridden directly in themes by creating a corresponding configuration file. For example:

    ```
    app/design/frontend/Vendor/Theme/Vendor_Module/web/module.config.ts
    ```

    - When this file exists, it **completely replaces** the original configuration provided by the module.
    - The theme configuration is not treated as an extension or a merged version of the module's configuration; instead, it fully overrides the original settings.

---

### Benefits and Future Potential

- **Customizability**: Module configurations can be tailored to fit the needs of specific projects or themes without altering the module code.
- **Scalability**: The configuration system is designed to support additional options beyond Tailwind in future versions, providing greater flexibility for module developers.
- **Control**: Themes have the ability to fully override module configurations, ensuring a clean separation of concerns and avoiding unwanted side effects.

---

### Key Notes

- The file is an **ESM** module (`export default`), consistent with the ESM-only build engine.
- Configurations are loaded in the sequence defined in `module.xml`. For detailed guidance, refer to the [official Magento documentation](https://developer.adobe.com/commerce/php/development/build/component-load-order).
- Overriding configurations in themes fully replaces the module's original settings, without merging or extending them.

## Tailwind Configuration

**{{ config.extra.components_name }}** uses **Tailwind CSS 4**, which is **CSS-first**: design tokens are declared in CSS (`@import "tailwindcss";` then `@theme { … }`), not in a JavaScript config. A theme declares its tokens in `web/css/theme.source.css` (see [CSS Configuration](../themes/css.md)); a module contributes tokens/utilities through its `view/frontend/web/css/module.extend.css`.

> For Tailwind 4 customization (the `@theme` block, the `@utility` and `@source` directives) refer to the official documentation:
> [Tailwind CSS — Theme variables](https://tailwindcss.com/docs/theme) · [Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files).

---

### How classes are detected (source scanning)

Tailwind only generates the utility classes it actually finds in your source files. In this stack Tailwind's **automatic detection does not reach the Magento tree** (its base path is the Vite harness, not `app/`), so the engine registers the sources explicitly — with **full inheritance**, exactly like it already does for components:

- **Vue/JS components** of every compatible module and of the theme, resolved through the theme → parent chain.
- **Twig/phtml templates** — the `view/frontend/templates` directory of every compatible module, **plus the whole theme inheritance chain** (theme → parent → …).

As a result, a class used in **any** module template/component, or in **any** theme of the inheritance chain (including a parent theme), is generated automatically. You do **not** need to add a manual `@source` for your templates.

---

### Opting a module out of scanning

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

This is the source-scanning counterpart of [`ignoredCssFromModules`](../themes/css.md), which excludes a module's **CSS** (`module.extend.css`) from the build.

---

### Prioritization & overrides

- Module CSS (`module.extend.css`) is imported **before** the theme CSS, so a theme's `theme.source.css` can override module tokens through the normal CSS cascade.
- Module load order follows the `sequence` declared in each `module.xml`. See the [official Magento documentation](https://developer.adobe.com/commerce/php/development/build/component-load-order).

---

### Legacy note (Tailwind 3)

Earlier versions used a `tailwind` object with `content` / `theme.extend` / `plugins` inside `module.config.js`. **Tailwind 4 is CSS-first and that object is no longer read.** Tokens and utilities now live in `module.extend.css` / `theme.source.css`, and class detection is handled by the engine as described above — there is no `content` array to maintain.
