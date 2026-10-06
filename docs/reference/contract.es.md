---
description: El XML de compatibilidad que aporta un módulo o tema, el archivo generado app/etc/mage_obsidian_frontend_modules.json y lo que valida el motor de build.
---

# XML de compatibilidad y contrato

PHP y el motor de build nunca se llaman entre sí. Comparten dos cosas: el XML de compatibilidad que un módulo o tema aporta para participar, y el archivo de contrato que PHP genera a partir de él y que el motor lee.

## `etc/mage_obsidian_compatibility.xml`

Un módulo o tema participa en el build del frontend solo si aporta este archivo. `bin/magento mage-obsidian:frontend:config --generate` busca el archivo en los módulos y temas habilitados.

=== "Módulo"

    ```xml title="etc/mage_obsidian_compatibility.xml"
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

=== "Tema"

    ```xml title="etc/mage_obsidian_compatibility.xml"
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

El archivo se valida contra un XSD que viene con `MageObsidian_ModernFrontend` en `etc/xsd/`:

| Esquema | Se usa para | Elementos bajo `<features>` |
|---|---|---|
| `mage_obsidian_compatibility.xsd` | Módulos | `compatibility` (booleano, obligatorio) y `universal` (booleano, opcional). |
| `mage_obsidian_theme_compatibility.xsd` | Temas | `compatibility` (booleano, obligatorio). |

| Elemento | Efecto |
|---|---|
| `compatibility` | Debe estar presente. Un módulo o tema con `false` queda fuera del contrato. |
| `universal` | Solo módulos. Con `true`, el layout del módulo se recoge incluso bajo temas que no son temas de MageObsidian. Se escribe en el contrato como `"universal": true`. |

## `app/etc/mage_obsidian_frontend_modules.json`

`bin/magento mage-obsidian:frontend:config --generate` escribe este archivo, junto con una copia `.php` de sus cuatro primeras claves, y lo valida contra un esquema JSON antes de escribirlo. El motor de build lo resuelve relativo al directorio de trabajo de Vite, en `../app/etc/mage_obsidian_frontend_modules.json`.

Versión actual del esquema: **`1.1.0`** (`ConfigInterface::SCHEMA_VERSION`).

| Clave | Tipo | Contenido |
|---|---|---|
| `schema_version` | string | La versión de la forma del archivo, `1.1.0`. |
| `mode` | string | El modo de Magento: `developer`, `default` o `production`. El motor trata todo lo que no sea `production` como desarrollo. |
| `modules` | objeto | Una entrada por módulo compatible, indexada por nombre de módulo. Cada entrada tiene `src`, la ruta del módulo, y opcionalmente `universal`. |
| `themes` | objeto | Una entrada por tema compatible, indexada por código de tema. Cada entrada tiene `src`, la ruta del tema, y `parent`, el código del tema padre o `null`. |
| `allModules` | string[] | Todos los nombres de módulos de Magento habilitados, sean compatibles o no. |
| `VUE_COMPONENTS_PATH` | string | Carpeta de componentes Vue: `components`. |
| `JS_PATH` | string | Carpeta de archivos JavaScript: `js`. |
| `FOLDERS_TO_WATCH` | string[] | Carpetas que vigila el servidor de desarrollo: `components` y `js`. |
| `ALLOWED_EXTENSIONS` | string[] | Extensiones de archivo que recoge el build: `js`, `vue`, `cjs`, `ts`. |
| `MODULE_CSS_EXTEND_FILE` | string | `module.extend.css`. |
| `MODULE_CONFIG_FILE` | string | `module.config.ts`. |
| `THEME_CONFIG_FILE` | string | `theme.config.js`. |
| `THEME_CSS_SOURCE_FILE` | string | `theme.source.css`. |
| `THEME_FILES_PATH` | string | `Theme`. |
| `LIB_PATH` | string | `lib`. |

Las rutas de `modules` y `themes` se guardan relativas a la raíz de Magento y el motor las vuelve absolutas al cargar el archivo.

```json title="app/etc/mage_obsidian_frontend_modules.json (abreviado)"
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

Las rutas de arriba son ilustrativas; el archivo generado lista los módulos y temas de tu tienda. El esquema JSON contra el que valida PHP rechaza cualquier clave que no esté en la tabla.

## Qué valida el motor

Cuando el build arranca, el motor lee el archivo y se niega a continuar si falla alguna comprobación. El error lista cada problema y sugiere volver a ejecutar `bin/magento mage-obsidian:frontend:config --generate`.

| Comprobación | Fallo |
|---|---|
| El archivo es un objeto JSON. | `Contract is not a JSON object.` |
| `schema_version` es una que el motor entiende. Este motor acepta `1.0.0` y `1.1.0`. | `Schema version mismatch: this build engine supports "1.0.0", "1.1.0" but the contract is "…".` |
| Está presente cada clave de primer nivel de la tabla de arriba. | `Missing required key "…".` |
| La herencia de temas termina: ningún tema es ancestro de sí mismo. | `Theme inheritance is cyclic: A -> B -> A.` |

Los mensajes de error del motor están en inglés. Regenera el archivo cada vez que habilites, deshabilites o muevas un módulo o tema. `bin/magento mage-obsidian:frontend:doctor` informa de un contrato que se desvió de los módulos y temas habilitados de la tienda.
