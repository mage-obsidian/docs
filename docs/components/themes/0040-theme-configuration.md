# Theme Configuration

In **{{ config.extra.components_name }}**, each compatible theme can include additional configurations by creating a configuration file at:

```
web/theme.config.js
```

This file is an **ESM (ECMAScript module)** that `export default`s a configuration object **{{ config.extra.components_name }}** uses to customize and control the theme’s behavior.

---

## How It Works

1. **Configuration File Location**  
    The theme configuration file should be placed in the following path relative to your theme’s directory:

    ```
    app/design/frontend/Vendor/Theme/web/theme.config.js
    ```

2. **Example Configuration File**  
    A basic example of a `theme.config.js` file might look like this:

    ```javascript
    export default {
        ignoredCssFromModules: [
            'Vendor_ModuleNameA',           // Exclude this module's CSS from the build
        ],
        includeCssSourceFromParentThemes: true,
        exposeNpmPackages: [
            {
                exposePath: 'pinia',         // Path used to import it
                package: 'pinia',           // Actual NPM package name
            },
        ],
    };
    ```

> **Tailwind tokens live in CSS, not here.** With [Tailwind 4](../modules/0050-tailwind-configuration.md) the theme's design tokens are declared in `web/css/theme.source.css` (`@theme { … }`), so `theme.config.js` carries only the build options below. See [CSS Configuration](0030-css-configuration.md).

---

## Configuration Options

### 1. **`ignoredCssFromModules`**  
   - **Type**: `Array` or `String ('all')`  
   - **Default**: `[]`  
   - **Description**: Specifies modules whose CSS should be excluded from the final build. If set to `'all'`, all module CSS files are excluded.  

### 2. **`includeCssSourceFromParentThemes`**  
   - **Type**: `Boolean`  
   - **Default**: `true`  
   - **Description**: Determines whether the CSS source files from parent themes should be included in the final build.  

### 3. **`exposeNpmPackages`**  
   - **Type**: `Array of Objects`  
   - **Default**: `[]`  
   - **Description**: Allows specific NPM packages to be exposed for use in the theme's frontend JavaScript. Each object in the array must define:
     - `exposePath`: The exposed path for importing the package.
     - `package`: The actual NPM package name.

   - **Usage in Templates**:  
     Exposed libraries can be easily accessed in `.phtml` files using the `$block->getViewLibFileUrl()` method. For example:
     ```php
     <script type="module" src="<?= $block->getViewLibFileUrl('pinia') ?>"></script>
     ```

   - **Example**:
     ```javascript
     exposeNpmPackages: [
         {
             exposePath: 'pinia',        // Import as "pinia"
             package: 'pinia',           // NPM package name
         },
         {
             exposePath: 'axios',        // Import as "axios"
             package: 'axios',           // NPM package name
         },
     ]
     ```

---

## Benefits of Theme Configuration

1. **Customizability**:  
    Themes can define their own configurations, ensuring flexibility for frontend behavior and design.

2. **Inheritance**:  
    Parent themes can pass down configurations to child themes, simplifying setup and maintaining consistency.

3. **Exclusion Control**:  
    Unwanted module CSS—from specific modules or all of them—can be excluded, keeping the final build clean and optimized.

4. **NPM Package Integration**:  
    Exposing NPM packages simplifies dependency management, allowing themes to directly use third-party libraries. These can be included in templates using `$block->getViewLibFileUrl()`.

---

## Key Notes

- The configuration file is an **ESM** module (`export default`), consistent with the ESM-only build engine.
- Excluded module CSS is ignored completely, reducing unnecessary styles.
- Exposing NPM packages as objects allows for precise integration with third-party libraries.
- Tailwind tokens are configured CSS-first in `web/css/theme.source.css` (`@theme`), not in this file.

By leveraging this configuration system, **{{ config.extra.components_name }}** ensures that themes remain powerful, customizable, and efficient for all frontend needs.
