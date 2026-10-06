---
description: Las claves que el motor de build lee de theme.config.js y module.config.ts, con tipo, valor por defecto y efecto.
---

# Configuración del build

El motor de build lee dos archivos de configuración. Un tema aporta `theme.config.js` y un módulo aporta `module.config.ts`; ambos son módulos ES con una exportación por defecto.

!!! warning "Un error tipográfico no hace nada"
    Las claves desconocidas en `theme.config.js` se ignoran en silencio; un error tipográfico no hace nada y tampoco produce un error. Si una opción parece no tener efecto, compara su escritura con las tablas de abajo.

## `theme.config.js`

Está en `web/theme.config.js` dentro del tema. El motor carga el archivo de cada tema de la cadena de herencia y los combina en profundidad, con el tema hijo por encima de sus padres. Esa combinación concatena los arrays, de modo que un tema hijo suma a la lista que declaró su padre.

Desde el motor 4.0.1 (`mage-obsidian` en npm), los valores por defecto se aplican **después** de la combinación, así que un tema hijo que omite una clave hereda el valor de su padre: un `vue.runtimeOnly: true` o un `ignoredCssFromModules: "all"` del padre pasa al hijo. Hasta 4.0.0 los valores por defecto se aplicaban al hijo antes de la combinación, y esas claves había que repetirlas en el hijo. El harness de Vite de framework 4.0.1 todavía instala el motor 3.2, así que un build tiene este comportamiento cuando el harness pase a requerir el motor 4.0.1.

`includeCssSourceFromParentThemes` es la excepción: describe la relación del propio tema con sus padres, así que nunca se hereda y vale `true` por defecto en cada tema.

| Clave | Tipo | Valor por defecto | Efecto |
|---|---|---|---|
| `includeCssSourceFromParentThemes` | `boolean` | `true` | Importa el `theme.source.css` de los temas ancestros, desde la raíz hacia abajo, hasta el ancestro más cercano que declara `false`: ese ancestro se incluye y los que están por encima no. Con `false`, solo se importa el `theme.source.css` del tema activo. Hasta el motor 4.0.0 se importaba toda la cadena hasta la raíz. |
| `ignoredCssFromModules` | `string[]` o `"all"` | `[]` | Módulos cuyo `module.extend.css` **no** se importa en el build. `"all"` omite todos los módulos. |
| `ignoredTailwindConfigFromModules` | `string[]` o `"all"` | sin definir | Módulos cuyos archivos Tailwind **no** escanea en busca de clases (componentes Vue y plantillas `.twig` / `.phtml`). `"all"` omite todos los módulos. Los archivos del propio tema siempre se escanean. |
| `scanCmsContent` | `boolean` | sin definir (se escanea) | Con `false`, el build no escanea el contenido CMS exportado con `bin/magento mage-obsidian:cms:export`. Cualquier otro valor, o ninguno, mantiene el escaneo activo. |
| `vue.runtimeOnly` | `boolean` | `false` | Hace que `vue` apunte a la build solo de runtime, sin el compilador de plantillas. En producción el alias apunta a la build de producción; en otro caso, a la de desarrollo. |
| `exposeNpmPackages` | `{ package: string, exposePath: string }[]` | `[]` | Paquetes npm que el build expone a todas las islas y módulos como una única instancia compartida. `package` es el nombre usado en `import`; `exposePath` es la ruta del paquete resuelta desde `node_modules`. |

Los nombres de módulo en `ignoredCssFromModules` y `ignoredTailwindConfigFromModules` usan la forma de Magento, `Vendor_Module`.

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
    Las tiendas que importan `MageObsidian_ModernFrontend::js/customer-data` necesitan `pinia` en `exposeNpmPackages`; si falta, el build falla con un mensaje que nombra el paquete ausente.

## `module.config.ts`

Está en `view/frontend/web/module.config.ts` dentro de un módulo, o en `Vendor_Module/web/module.config.ts` dentro de un tema para sobrescribir el archivo del módulo. El motor combina el archivo de cada módulo habilitado, y la copia de un tema reemplaza la del propio módulo.

La única clave que el motor lee es `interceptors`. Un módulo sin nada que configurar exporta un objeto vacío.

| Clave | Tipo | Valor por defecto | Efecto |
|---|---|---|---|
| `interceptors` | `Record<string, Interceptor>` | ninguno | Registra interceptores JS, el port del sistema de plugins de Magento. La clave del objeto es el nombre del interceptor. |

Cada `Interceptor` acepta estos campos:

| Campo | Tipo | Valor por defecto | Efecto |
|---|---|---|---|
| `name` | `string` | ninguno | Nombre del interceptor, repetido desde su clave. Lo identifica en los errores del build. |
| `target` | `string` | obligatorio | El módulo interceptado, como `Vendor_Module::path/to/file.js`. Un interceptor sin `target` se omite. |
| `interceptor` | `string` | obligatorio | El módulo que contiene las funciones interceptoras, como `Vendor_Module::path/to/file.js`. Se ejecutan sus exportaciones llamadas `before…`, `around…` y `after…` seguidas del nombre de la función del objetivo. |
| `sortOrder` | `number` | `10` | Orden de ejecución entre los interceptores del mismo objetivo; el menor se ejecuta primero. |
| `active` | `boolean` | `true` | Con `false`, el interceptor queda fuera. |

Dos módulos que declaran el mismo nombre de interceptor para el mismo objetivo se combinan campo por campo, de modo que una declaración posterior puede cambiar `sortOrder` o `active` sin repetir el resto. Consulta [Interceptores JS](../guides/modules/interceptors.md).

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

## Archivos relacionados

| Archivo | Dónde | Propósito |
|---|---|---|
| `theme.source.css` | `web/css/` en un tema | La entrada de Tailwind del tema. |
| `module.extend.css` | `view/frontend/web/css/` en un módulo | CSS que un módulo añade al build de cada tema. |

Los nombres de los cuatro archivos vienen del [contrato generado](contract.md).
