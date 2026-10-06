---
description: The keys the build engine reads from theme.config.js and module.config.ts, with type, default and effect.
---

# Build configuration

The build engine reads two configuration files. A theme ships `theme.config.js` and a module ships `module.config.ts`; both are plain ES modules with a default export.

!!! warning "A typo is a no-op"
    Unknown keys in `theme.config.js` are ignored silently; a typo is a no-op, not an error. If an option seems to have no effect, compare its spelling with the tables below.

## `theme.config.js`

Located at `web/theme.config.js` inside the theme. The engine loads the file of every theme in the inheritance chain and deep-merges them, with the child theme winning over its parents. Arrays are concatenated by that merge, so a child theme adds to the list its parent declared.

Since engine 4.0.1 (`mage-obsidian` on npm), defaults are applied **after** the merge, so a child theme that omits a key inherits its parent's value: a parent's `vue.runtimeOnly: true` or `ignoredCssFromModules: "all"` carries over to the child. Up to 4.0.0 the defaults were applied to the child before the merge, and those keys had to be repeated in the child. The Vite harness of framework 4.0.1 still installs engine 3.2, so a build gets this behaviour once the harness requires engine 4.0.1.

`includeCssSourceFromParentThemes` is the exception: it describes the theme's own relation to its parents, so it is never inherited and defaults to `true` in every theme.

| Key | Type | Default | Effect |
|---|---|---|---|
| `includeCssSourceFromParentThemes` | `boolean` | `true` | Imports the `theme.source.css` of the ancestor themes, from the root down, stopping at the nearest ancestor that sets `false`: that ancestor is included and the ones above it are not. With `false`, only the active theme's own `theme.source.css` is imported. Up to engine 4.0.0 the whole chain up to the root was imported. |
| `ignoredCssFromModules` | `string[]` or `"all"` | `[]` | Modules whose `module.extend.css` is **not** imported into the build. `"all"` skips every module. |
| `ignoredTailwindConfigFromModules` | `string[]` or `"all"` | not set | Modules whose files Tailwind does **not** scan for classes (Vue components and `.twig` / `.phtml` templates). `"all"` skips every module. The theme's own files are always scanned. |
| `scanCmsContent` | `boolean` | not set (scanned) | With `false`, the build does not scan the CMS content exported by `bin/magento mage-obsidian:cms:export`. Any other value, or no value, keeps the scan on. |
| `vue.runtimeOnly` | `boolean` | `false` | Aliases `vue` to the runtime-only build, without the template compiler. In production the alias points to the production build, otherwise to the development one. |
| `exposeNpmPackages` | `{ package: string, exposePath: string }[]` | `[]` | npm packages the build exposes to every island and module as a single shared instance. `package` is the name used in `import`, `exposePath` is the package path resolved from `node_modules`. |

Module names in `ignoredCssFromModules` and `ignoredTailwindConfigFromModules` use the Magento form, `Vendor_Module`.

```js title="web/theme.config.js"
export default {
    includeCssSourceFromParentThemes: false,
    ignoredCssFromModules: [],
    ignoredTailwindConfigFromModules: [],
    vue: {
        runtimeOnly: true,
    },
    exposeNpmPackages: [
        {
            package: 'pinia',
            exposePath: 'pinia',
        },
    ],
}
```

!!! note
    Stores that import `MageObsidian_ModernFrontend::js/customer-data` need `pinia` in `exposeNpmPackages`; the build fails with a message naming the missing package otherwise.

## `module.config.ts`

Located at `view/frontend/web/module.config.ts` inside a module, or at `Vendor_Module/web/module.config.ts` inside a theme to override the module's file. The engine merges the file of every enabled module, and a theme's copy replaces the module's own.

The only key the engine reads is `interceptors`. A module with nothing to configure exports an empty object.

| Key | Type | Default | Effect |
|---|---|---|---|
| `interceptors` | `Record<string, Interceptor>` | none | Registers JS interceptors, the port of Magento's plugin system. The object key is the interceptor name. |

Each `Interceptor` takes these fields:

| Field | Type | Default | Effect |
|---|---|---|---|
| `name` | `string` | none | Name of the interceptor, repeated from its key. It identifies the interceptor in build errors. |
| `target` | `string` | required | The module being intercepted, as `Vendor_Module::path/to/file.js`. An interceptor without a `target` is skipped. |
| `interceptor` | `string` | required | The module that holds the interceptor functions, as `Vendor_Module::path/to/file.js`. Its exports named `before…`, `around…` and `after…` followed by the target function name are the ones that run. |
| `sortOrder` | `number` | `10` | Execution order among the interceptors of the same target; lower runs first. |
| `active` | `boolean` | `true` | With `false`, the interceptor is left out. |

Two modules that declare the same interceptor name for the same target are merged field by field, so a later declaration can change `sortOrder` or `active` without repeating the rest. See [JS interceptors](../guides/modules/interceptors.md).

```ts title="view/frontend/web/module.config.ts"
export default {
    interceptors: {
        CartTotalsLogger: {
            name: 'CartTotalsLogger',
            target: 'Vendor_Cart::js/totals.js',
            interceptor: 'Vendor_Logger::js/cart-totals-interceptor.js',
            sortOrder: 20,
            active: true,
        },
    },
};
```

## Related files

| File | Where | Purpose |
|---|---|---|
| `theme.source.css` | `web/css/` in a theme | The Tailwind entry of the theme. |
| `module.extend.css` | `view/frontend/web/css/` in a module | CSS a module adds to every theme's build. |

The names of all four files come from the [generated contract](contract.md).
