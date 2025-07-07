# Configuración de Temas

En **{{ config.extra.components_name }}**, cada tema compatible puede incluir configuraciones adicionales creando un archivo de configuración en:

```
web/theme.config.js
```

Este archivo es un **módulo ESM (ECMAScript)** que hace `export default` de un objeto de configuración que **{{ config.extra.components_name }}** utiliza para personalizar y controlar el comportamiento del tema.

---

## ¿Cómo Funciona?

1. **Ubicación del Archivo de Configuración**  
    El archivo de configuración del tema debe colocarse en la siguiente ruta relativa al directorio del tema:

    ```
    app/design/frontend/Vendor/Theme/web/theme.config.js
    ```

2. **Ejemplo de Archivo de Configuración**  
    Un ejemplo básico de un archivo `theme.config.js` podría verse así:

    ```javascript
    export default {
        ignoredCssFromModules: [
            'Vendor_ModuleNameA',           // Excluir el CSS de este módulo del build
        ],
        includeCssSourceFromParentThemes: true,
        exposeNpmPackages: [
            {
                exposePath: 'pinia',         // Ruta usada para importarlo
                package: 'pinia',           // Nombre real del paquete NPM
            },
        ],
    };
    ```

> **Los tokens de Tailwind viven en CSS, no aquí.** Con [Tailwind 4](../modules/0050-tailwind-configuration.md) los design tokens del tema se declaran en `web/css/theme.source.css` (`@theme { … }`), así que `theme.config.js` solo lleva las opciones de build de abajo. Consulta [Configuración de CSS](0030-css-configuration.md).

---

## Opciones de Configuración

### 1. **`ignoredCssFromModules`**  
   - **Tipo**: `Array` o `String ('all')`  
   - **Por defecto**: `[]`  
   - **Descripción**: Especifica los módulos cuyo CSS debe excluirse de la compilación final. Si se establece en `'all'`, se excluye el CSS de todos los módulos.  

### 2. **`includeCssSourceFromParentThemes`**  
   - **Tipo**: `Boolean`  
   - **Por defecto**: `true`  
   - **Descripción**: Determina si los archivos fuente de CSS de los temas principales deben incluirse en la compilación final.  

### 3. **`exposeNpmPackages`**  
   - **Tipo**: `Array de Objetos`  
   - **Por defecto**: `[]`  
   - **Descripción**: Permite exponer paquetes NPM específicos para su uso en el JavaScript del frontend del tema. Cada objeto en el array debe definir:
     - `exposePath`: Ruta expuesta para importar el paquete.
     - `package`: Nombre real del paquete NPM.

   - **Uso en Plantillas**:  
     Las librerías expuestas pueden ser fácilmente accesibles en archivos `.phtml` utilizando el método `$block->getViewLibFileUrl()`. Por ejemplo:
     ```php
     <script type="module" src="<?= $block->getViewLibFileUrl('pinia') ?>"></script>
     ```

   - **Ejemplo**:
     ```javascript
     exposeNpmPackages: [
         {
             exposePath: 'pinia',        // Importar como "pinia"
             package: 'pinia',           // Nombre del paquete NPM
         },
         {
             exposePath: 'axios',        // Importar como "axios"
             package: 'axios',           // Nombre del paquete NPM
         },
     ]
     ```

---

## Beneficios de la Configuración de Temas

1. **Personalización**:  
    Los temas pueden definir sus propias configuraciones, asegurando flexibilidad para el comportamiento y diseño del frontend.

2. **Herencia**:  
    Los temas principales pueden pasar configuraciones a los temas secundarios, simplificando la configuración y manteniendo la consistencia.

3. **Control de Exclusión**:  
    Elimina el CSS no deseado de módulos específicos o de todos los módulos, manteniendo una compilación final limpia y optimizada.

4. **Integración de Paquetes NPM**:  
    Exponer paquetes NPM simplifica la gestión de dependencias, permitiendo a los temas usar directamente librerías de terceros. Estas pueden incluirse en las plantillas mediante `$block->getViewLibFileUrl()`.

---

## Notas Clave

- El archivo de configuración es un módulo **ESM** (`export default`), coherente con el engine de build ESM-only.
- El CSS de módulos excluido se omite por completo, reduciendo estilos innecesarios.
- Exponer paquetes NPM como objetos permite una integración precisa con librerías de terceros.
- Los tokens de Tailwind se configuran CSS-first en `web/css/theme.source.css` (`@theme`), no en este archivo.

Aprovechando este sistema de configuración, **{{ config.extra.components_name }}** garantiza que los temas sean potentes, personalizables y eficientes para todas las necesidades del frontend.
