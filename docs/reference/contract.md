---
description: The compatibility XML a module or theme ships, the generated app/etc/mage_obsidian_frontend_modules.json, and what the build engine validates.
---

# Compatibility XML & contract

PHP and the build engine never call each other. They share two things: the compatibility XML that a module or theme ships to opt in, and the contract file that PHP generates from it and the engine reads.

## `etc/mage_obsidian_compatibility.xml`

A module or theme takes part in the frontend build only if it ships this file. `bin/magento mage-obsidian:frontend:config --generate` scans the enabled modules and themes for it.

=== "Module"

    ```xml title="etc/mage_obsidian_compatibility.xml"
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

=== "Theme"

    ```xml title="etc/mage_obsidian_compatibility.xml"
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

The file is validated against an XSD that ships with `MageObsidian_ModernFrontend` under `etc/xsd/`:

| Schema | Used for | Elements under `<features>` |
|---|---|---|
| `mage_obsidian_compatibility.xsd` | Modules | `compatibility` (boolean, required) and `universal` (boolean, optional). |
| `mage_obsidian_theme_compatibility.xsd` | Themes | `compatibility` (boolean, required). |

| Element | Effect |
|---|---|
| `compatibility` | Must be present. A module or theme with `false` is left out of the contract. |
| `universal` | Modules only. With `true`, the module's layout is collected even under themes that are not MageObsidian themes. It is written to the contract as `"universal": true`. |

## `app/etc/mage_obsidian_frontend_modules.json`

`bin/magento mage-obsidian:frontend:config --generate` writes this file, together with a `.php` copy of its first four keys, and validates it against a JSON schema before writing. The build engine resolves it relative to the Vite working directory, at `../app/etc/mage_obsidian_frontend_modules.json`.

Current schema version: **`1.1.0`** (`ConfigInterface::SCHEMA_VERSION`).

| Key | Type | Content |
|---|---|---|
| `schema_version` | string | The version of the file shape, `1.1.0`. |
| `mode` | string | The Magento mode: `developer`, `default` or `production`. The engine treats everything except `production` as development. |
| `modules` | object | One entry per compatible module, keyed by module name. Each entry has `src`, the module path, and optionally `universal`. |
| `themes` | object | One entry per compatible theme, keyed by theme code. Each entry has `src`, the theme path, and `parent`, the parent theme code or `null`. |
| `allModules` | string[] | Every enabled Magento module name, compatible or not. |
| `VUE_COMPONENTS_PATH` | string | Folder of Vue components: `components`. |
| `JS_PATH` | string | Folder of JavaScript files: `js`. |
| `FOLDERS_TO_WATCH` | string[] | Folders the dev server watches: `components` and `js`. |
| `ALLOWED_EXTENSIONS` | string[] | File extensions the build picks up: `js`, `vue`, `cjs`, `ts`. |
| `MODULE_CSS_EXTEND_FILE` | string | `module.extend.css`. |
| `MODULE_CONFIG_FILE` | string | `module.config.ts`. |
| `THEME_CONFIG_FILE` | string | `theme.config.js`. |
| `THEME_CSS_SOURCE_FILE` | string | `theme.source.css`. |
| `THEME_FILES_PATH` | string | `Theme`. |
| `LIB_PATH` | string | `lib`. |

Paths in `modules` and `themes` are stored relative to the Magento root and made absolute by the engine when it loads the file.

```json title="app/etc/mage_obsidian_frontend_modules.json (abridged)"
{
    "schema_version": "1.1.0",
    "mode": "production",
    "modules": {
        "MageObsidian_ModernFrontend": { "src": "vendor/mage-obsidian/module-modern-frontend/src" }
    },
    "themes": {
        "MageObsidian/default": {
            "src": "app/design/frontend/MageObsidian/default",
            "parent": "MageObsidian/theme-base"
        }
    },
    "allModules": ["Magento_Catalog", "MageObsidian_ModernFrontend"],
    "MODULE_CONFIG_FILE": "module.config.ts",
    "THEME_CONFIG_FILE": "theme.config.js"
}
```

The paths above are illustrative; the generated file lists the modules and themes of your store. The JSON schema that PHP validates against rejects any key that is not in the table.

## What the engine validates

When the build starts, the engine reads the file and refuses to continue if any check fails. The error lists each problem and suggests running `bin/magento mage-obsidian:frontend:config --generate` again.

| Check | Failure |
|---|---|
| The file is a JSON object. | `Contract is not a JSON object.` |
| `schema_version` is one the engine understands. This engine accepts `1.0.0` and `1.1.0`. | `Schema version mismatch: this build engine supports "1.0.0", "1.1.0" but the contract is "…".` |
| Every top-level key in the table above is present. | `Missing required key "…".` |
| Theme inheritance ends: no theme is its own ancestor. | `Theme inheritance is cyclic: A -> B -> A.` |

Regenerate the file whenever a module or theme is enabled, disabled or moved. `bin/magento mage-obsidian:frontend:doctor` reports a contract that has drifted from the store's enabled modules and themes.
