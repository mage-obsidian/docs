# Theme Configuration

In **{{ config.extra.components_name }}**, each compatible theme can include additional configurations by creating a configuration file at:

```
web/theme.config.cjs
```

This file follows the **CJS (CommonJS)** format for compatibility reasons and exports a configuration object that **{{ config.extra.components_name }}** uses to customize and control the theme’s behavior.

---

## How It Works

1. **Configuration File Location**  
    The theme configuration file should be placed in the following path relative to your theme’s directory:

    ```
    app/design/frontend/Vendor/Theme/web/theme.config.cjs
    ```

2. **Example Configuration File**  
    A basic example of a `theme.config.cjs` file might look like this:

    ```javascript
    module.exports = {
        tailwind: {
            theme: {
                extend: {
                    // Add custom Tailwind configurations here
                },
            },
            plugins: [],
            content: [
                './**/*.{vue,js}',            // Track classes in Vue and JS files
                '../**/*.phtml',             // Track classes in PHTML templates
                '../*/page_layout/override/base/*.xml', // Track classes in XML layouts
            ],
        },
        ignoredTailwindConfigFromModules: [],
        ignoredCssFromModules: [
            'Vendor_ModuleNameA',           // Exclude CSS from specific modules
        ],
        includeTailwindConfigFromParentThemes: true,
        includeCssSourceFromParentThemes: true,
        exposeNpmPackages: [
            {
                exposePath: 'pinia',         // Exposed path for importing
                package: 'pinia',           // Actual package name
            },
        ],
    };
    ```

---

## Configuration Options

### 1. **`tailwind`**  
   - **Type**: `Object`  
   - **Default**: `{}`  
   - **Description**: Defines custom Tailwind CSS configurations for the theme. This can include `theme`, `plugins`, and `content` arrays.  
   - **Example**:
     ```javascript
     tailwind: {
         theme: {
             extend: {
                 colors: {
                     brand: '#1a202c',
                 },
             },
         },
         plugins: [],
         content: [
             './**/*.{vue,js}',
             '../**/*.phtml',
         ],
     }
     ```
> For details on how to structure a Tailwind CSS configuration, refer to the official documentation:  
[Tailwind CSS Configuration](https://tailwindcss.com/docs/configuration)

### 2. **`ignoredTailwindConfigFromModules`**  
   - **Type**: `Array` or `String ('all')`  
   - **Default**: `[]`  
   - **Description**: Lists module-specific Tailwind configurations to ignore. If set to `'all'`, all module Tailwind configurations will be excluded.  

### 3. **`ignoredCssFromModules`**  
   - **Type**: `Array` or `String ('all')`  
   - **Default**: `[]`  
   - **Description**: Specifies modules whose CSS should be excluded from the final build. If set to `'all'`, all module CSS files will be excluded.  

### 4. **`includeTailwindConfigFromParentThemes`**  
   - **Type**: `Boolean`  
   - **Default**: `true`  
   - **Description**: Determines whether the theme should inherit Tailwind configurations from its parent themes.  

### 5. **`includeCssSourceFromParentThemes`**  
   - **Type**: `Boolean`  
   - **Default**: `true`  
   - **Description**: Determines whether the CSS source files from parent themes should be included in the final build.  

### 6. **`exposeNpmPackages`**  
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
    Unwanted CSS or Tailwind configurations from specific modules—or all modules—can be excluded, keeping the final build clean and optimized.

4. **Tailwind Integration**:  
    Themes can fully leverage Tailwind CSS for a utility-first approach, with complete control over its configuration.

5. **NPM Package Integration**:  
    Exposing NPM packages simplifies dependency management, allowing themes to directly use third-party libraries. These can be included in templates using `$block->getViewLibFileUrl()`.

---

## Key Notes

- The configuration file format is **CJS** to ensure compatibility across environments.
- Excluded CSS and Tailwind configurations from modules are ignored completely, reducing unnecessary styles.
- Exposing NPM packages as objects allows for precise integration with third-party libraries.

By leveraging this configuration system, **{{ config.extra.components_name }}** ensures that themes remain powerful, customizable, and efficient for all frontend needs.
