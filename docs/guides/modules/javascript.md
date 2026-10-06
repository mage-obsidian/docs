# JavaScript & imports

## JavaScript Configuration

In **{{ config.extra.components_name }}**, all JavaScript files should be placed in the following directories:  
```
view/frontend/web/js
```
or  
```
view/frontend/web/components
```

#### **Important Recommendation**

While it is possible to use the `components` directory for specific scripts, **we strongly recommend using the `js` directory for custom scripts**. This ensures better organization and separation of concerns, maintaining a clear and modular development structure.

> The `components` directory should be reserved only for logic that is tightly coupled to specific frontend components.

---

### Modifying Scripts in Themes

JavaScript files can be overridden in themes to provide custom functionality or adaptations specific to a project. This feature allows for flexibility while maintaining the original structure of the module.

> More details about overriding scripts will be provided in the section about themes.

---

### Best Practices

- **Structure and Organization**: Use the `js` directory as the primary location for all your custom scripts and logic. This promotes maintainability and ensures a clear project structure.
- **Integrating Node.js Packages**: You can integrate Node.js packages into your scripts to enhance functionality, or write plain JavaScript if no external dependencies are needed.
- **Default JavaScript Format**: All scripts should use **ESM (ECMAScript Modules)** by default. This ensures compatibility with modern browsers and promotes a modular architecture.

---

### How It Works

1. **Build Process with Vite**  
    All JavaScript files are processed and compiled by **Vite**, resulting in an optimized output. This ensures:
    - Improved performance through modern bundling techniques.
    - Tree-shaking to include only the code necessary for the final bundle.
    - Faster builds and hot module replacement (HMR) during development.

2. **Optimized Downloads**  
    **{{ config.extra.components_name }}** takes a performance-first approach:
    - Only JavaScript files explicitly used in the frontend are downloaded.
    - Unused code is excluded from the final bundle, reducing load times and improving efficiency.

3. **Integration with Views**  
    JavaScript files can be included in your views or `.phtml` templates as needed. Specific examples on how to integrate scripts will be provided later in this documentation.

---

### Example Directory Structure

Here is a suggested structure for your JavaScript files:

```
view/
└── frontend/
    └── web/
        ├── js/
        │   ├── main.js         // Entry point for custom logic
        │   ├── utils.js        // Reusable utility functions
        │   └── services/
        │       └── api.js      // API integration logic
        └── components/
            ├── navbar.vue      // Vue component for navbar
            └── modal.vue       // Vue component for modal
```

This structure ensures that the `js` directory is the primary location for custom scripts, while the `components` directory can be used for component-specific logic if absolutely necessary.

---

### Benefits

- **Modularity**: Keeping scripts in dedicated directories ensures clean and maintainable code.
- **Flexibility**: Scripts can be overridden in themes to adapt to specific requirements.
- **Performance**: By leveraging Vite’s build process, only the necessary JavaScript is included in the final bundle, reducing page load times.
- **Scalability**: The ability to integrate Node.js packages and write modular JavaScript ensures your codebase can grow with your project’s needs.

---

### Key Notes

- **Use the `js` directory as the primary location for custom scripts.**
- All JavaScript files must use **ESM (ECMAScript Modules)** as the default format.
- Files located in `view/frontend/web/js` and `view/frontend/web/components` are automatically tracked and processed.
- JavaScript files can be overridden in themes. Details about this will be covered in the section about themes.
- The system ensures that only scripts explicitly included in your frontend are downloaded, adhering to a performance-first approach.
- Examples of how to include JavaScript files in `.phtml` templates will be provided in later sections.

## Importing Between Magento Modules

In **{{ config.extra.components_name }}**, importing JavaScript files and Vue components follows flexible conventions that apply specifically to files in the `js` and `components` directories. This approach ensures compatibility, modularity, and seamless overwriting of components by themes.

---

### Supported Import Methods

1. **NPM Modules**  
   NPM packages can be imported normally without any special configuration:
   ```javascript
   import _ from 'lodash';
   import axios from 'axios';
   ```

2. **Relative and Absolute Imports**  
   Files in the `js` and `components` directories can be imported using relative or absolute paths:
   ```javascript
   import Button from './components/Button.vue';  // Relative
   import Navbar from '/view/frontend/web/components/Navbar.vue';  // Absolute
   ```

3. **Module-Based Imports**  
   The most powerful feature is the ability to import files from other Magento modules using the following notation:
   ```javascript
   import Demo from 'Vendor_ModuleA::components/demo.vue';
   import Main from 'Vendor_ModuleF::js/main.js';
   ```

   - If the root directory (e.g., `components` or `js`) is omitted, it defaults to `components`:
     ```javascript
     import Demo from 'Vendor_ModuleA::demo.vue';  // Same as Vendor_ModuleA::components/demo.vue
     ```

4. **Theme-Based Imports**  
   Files from the theme can be imported using a similar notation:
   ```javascript
   import Navbar from 'Theme::nav.vue';
   ```

   This follows the same resolution rules as module-based imports, allowing themes to override components or scripts seamlessly.

---

### Application in `js` and `components`

This import system is specifically designed for files located in the `js` and `components` directories:
- **JavaScript files**: These are tracked in `view/frontend/web/js`.
- **Vue components**: These are tracked in `view/frontend/web/components`.

For example:
- `Vendor_ModuleF::js/main.js` references a file in the `js` directory.
- `Vendor_ModuleA::components/demo.vue` references a file in the `components` directory.

Any imports outside these directories must use standard relative or absolute paths.

---

### Why This Matters

#### Resolving Overwritten Components
When files are overridden in themes, **relative or absolute imports fail to reflect these changes**, leading to unexpected behavior.  

For example:
```javascript
import Bar from '../../bar.vue';
```
If the `bar.vue` component is overridden in the theme, this relative path will still reference the original module component, ignoring the theme's overwrite.

Conversely:
```javascript
import Bar from 'Vendor_Module::bar.vue';
```
When importing via the `Vendor_Module::` notation, **Vite automatically resolves the appropriate file**, respecting the overwrite hierarchy (module -> theme). This ensures the correct resource is always loaded.

---

### Best Practices for Imports

1. **Always Use Module-Based Imports**  
   Use the `Vendor_Module::` notation for importing resources from Magento modules. This ensures:
   - Proper resolution of overridden components or scripts in themes.
   - A modular and maintainable codebase.

   Example:
   ```javascript
   import Button from 'Vendor_Module::button.vue';
   ```

2. **Avoid Relative or Absolute Imports**  
   Unless specifically required, do not use relative or absolute paths for module resources in `js` or `components`. These bypass Vite's resolution mechanism, causing unexpected behavior if resources are overridden.

3. **Use Theme Imports for Overrides**  
   If you want to explicitly use a resource from the theme, use the `Theme::` notation:
   ```javascript
   import Navbar from 'Theme::navbar.vue';
   ```

4. **Consistency in Import Notation**  
   Maintain consistent use of the `Vendor_Module::` and `Theme::` notations throughout your project to prevent confusion and ensure compatibility.

---

### Examples

#### Importing from a Module
```javascript
import Card from 'Vendor_ModuleA::components/Card.vue';
import ApiService from 'Vendor_ModuleB::js/api-service.js';
```

#### Importing from the Theme
```javascript
import Header from 'Theme::header.vue';
```

#### Improper Import
```javascript
// Avoid this
import Footer from './Footer.vue'; // This will not reflect theme overrides
```

---

### Benefits of Using Module-Based and Theme Imports

1. **Seamless Theme Overrides**  
   Ensures the correct component or script is loaded, respecting the hierarchy of overwrites.

2. **Modularity**  
   Encourages a modular approach, making your codebase more maintainable and easier to scale.

3. **Flexibility**  
   Supports customizations without breaking the original structure of modules.

4. **Error Prevention**  
   Prevents unexpected behavior caused by hardcoded relative or absolute paths.

---

### Key Notes

- This system applies only to files in the `js` and `components` directories.
- Use the `Vendor_Module::` notation for all imports within Magento modules.
- Use the `Theme::` notation for resources explicitly from themes.
- Avoid relative or absolute paths unless necessary.
- Vite handles resolution and ensures that overridden components or scripts in themes are correctly loaded.

By following these guidelines, **{{ config.extra.components_name }}** enables a clean, flexible, and reliable workflow for managing JavaScript and Vue components across modules and themes.

## Import Tooling

The [`Vendor_Module::` notation](javascript.md) is a first-class part of the **{{ config.extra.components_name }}** workflow, not just a build-time convenience. Three pieces of tooling make it pleasant and safe to use: **editor autocomplete**, a **live dev watcher**, and a **fail-loud guard**.

You do not configure any of this — the build sets it up. This page explains what it does so the behavior is not surprising.

---

### Editor Autocomplete (`jsconfig.json`)

On every build (and live in dev) the engine writes a `jsconfig.json` at the theme source root that teaches the editor how to resolve `Vendor_Module::` specifiers. Each specifier is mapped to the **real source file** it resolves to, derived from the exact same inheritance map the build uses — so what the editor sees always matches what the build produces.

What you get in VS Code (with the Vue/Volar extension) or PhpStorm:

- **Autocomplete** for `Vendor_Module::` import paths.
- **Go-to-definition** (Ctrl/Cmd+click) jumps straight to the actual `.vue`/`.js` file, even when the file lives in another module or a parent theme.
- Both the full form (`Vendor_Module::components/Card`) and the shorthand (`Vendor_Module::Card`) resolve.
- A `"*"` wildcard also points npm packages (`vue`, `@heroicons/...`, `pinia`, …) at the build harness's `node_modules`, so those resolve in the editor too.

> **Important:** The generated `jsconfig.json` is **managed by the build** — it carries a `// Generated by mage-obsidian` marker on the first line, is git-ignored, and is rewritten on every build. Do not edit it. If a hand-written `jsconfig.json` (without the marker) already exists, the build leaves it untouched and warns you; remove it so the build can take over.

> **Tip:** After the first build (or if resolution looks stale), run **Restart TS Server** in your editor so it re-reads the regenerated `jsconfig.json`.

#### Containers and mounts

When the build runs inside a container but you edit the files at a different host path (a bind-mount), the absolute paths baked into `jsconfig.json` would point at container paths the editor cannot open. Set `MAGE_OBSIDIAN_TYPES_PATH_MAP` to remap them:

```dotenv
# from=>to[,from2=>to2]; longest prefix wins
MAGE_OBSIDIAN_TYPES_PATH_MAP=/var/www/html/vite=>/home/me/project/component-modern-frontend/vite,/var/www/html=>/home/me/project/magento-root
```

When the build and the editor share a filesystem, leave it unset — the identity mapping is correct.

---

### Live Dev Watcher

The inheritance map is computed once when the dev server starts and cached. Adding or removing a `.vue`/`.js` source would normally be invisible until a restart — both to the runtime resolver and to the editor `jsconfig.json`.

A dev-only watcher fixes that. When you **create or delete** a component or JS source under a watched directory (every opted-in module's `web` dir, plus the theme and its parent chain), it:

1. Invalidates the cached inheritance map for the theme.
2. Invalidates the compiled interceptor set, so a plugin added or retargeted while the server is up takes effect on the next build.
3. Rewrites the persisted resolution map (so `Vendor_Module::` resolves the new file at runtime).
4. Regenerates the theme `jsconfig.json` (so the editor sees it too).

The resolver plugins read that map **per request** rather than capturing it when the server boots, which is what makes the refresh visible without a restart.

It logs `sources changed — refreshed <theme> import resolution`. Changes are debounced and writes are idempotent, so editing file *contents* (as opposed to adding/removing files) does not trigger it — Vite's own HMR handles that.

---

### Fail-Loud Guard

A `Vendor_Module::` specifier that does not resolve used to be **silently externalized** by the bundler, only to break at runtime with no clear cause. A guard now runs **last** in the resolver chain: if a `::` specifier reaches it, none of the real resolvers could handle it — a typo or a missing file — so it throws a build/dev error instead.

The error names the unresolved specifier, the importer, and the closest valid alternatives:

```text
[mage-obsidian] Unresolved import "Acme_Catalog::ProductsCard".
  imported by: .../components/Page.vue
  Did you mean:
    - Acme_Catalog::ProductCard
    - Acme_Catalog::products/Card
```

For an asset path, it tells you exactly where the file was expected:

```text
[mage-obsidian] Unresolved import "Acme_Catalog::assets/logo.svg".
  imported by: .../components/Header.vue
  Asset not found. Expected a theme override at <theme>/Acme_Catalog/web/assets/logo.svg
  or the module at <module>/view/frontend/web/assets/logo.svg.
```

And when nothing is registered under the namespace at all, it reminds you to enable the module/theme and regenerate the contract:

```text
  Nothing is registered under "Acme_Catalog". Is the module/theme enabled and
  compatible, and the contract regenerated (bin/magento mage-obsidian:frontend:config --generate)?
```

---

### Key Notes

- `jsconfig.json` is generated, git-ignored, and must not be hand-edited.
- Use `Restart TS Server` after the first build to pick up autocomplete.
- A broken `::` import fails the build with suggestions — it never silently ships.
- The dev watcher keeps autocomplete and runtime resolution in sync as you add/remove files, no restart needed.
