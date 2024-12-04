# Configuración de Temas

En **{{ config.extra.components_name }}**, cada tema compatible puede incluir configuraciones adicionales creando un archivo de configuración en:

```
web/theme.config.cjs
```

Este archivo utiliza el formato **CJS (CommonJS)** por razones de compatibilidad y exporta un objeto de configuración que **{{ config.extra.components_name }}** utiliza para personalizar y controlar el comportamiento del tema.

---

## ¿Cómo Funciona?

1. **Ubicación del Archivo de Configuración**  
    El archivo de configuración del tema debe colocarse en la siguiente ruta relativa al directorio del tema:

    ```
    app/design/frontend/Vendor/Theme/web/theme.config.cjs
    ```

2. **Ejemplo de Archivo de Configuración**  
    Un ejemplo básico de un archivo `theme.config.cjs` podría verse así:

    ```javascript
    module.exports = {
        tailwind: {
            theme: {
                extend: {
                    // Agrega configuraciones personalizadas de Tailwind aquí
                },
            },
            plugins: [],
            content: [
                './**/*.{vue,js}',            // Rastrear clases en archivos Vue y JS
                '../**/*.phtml',             // Rastrear clases en plantillas PHTML
                '../*/page_layout/override/base/*.xml', // Rastrear clases en diseños XML
            ],
        },
        ignoredTailwindConfigFromModules: [],
        ignoredCssFromModules: [
            'Vendor_ModuleNameA',           // Excluir CSS de módulos específicos
        ],
        includeTailwindConfigFromParentThemes: true,
        includeCssSourceFromParentThemes: true,
        exposeNpmPackages: [
            {
                exposePath: 'pinia',         // Ruta expuesta para importar
                package: 'pinia',           // Nombre real del paquete
            },
        ],
    };
    ```

---

## Opciones de Configuración

### 1. **`tailwind`**  
   - **Tipo**: `Object`  
   - **Por defecto**: `{}`  
   - **Descripción**: Define configuraciones personalizadas de Tailwind CSS para el tema. Esto puede incluir `theme`, `plugins` y un array de `content`.  
   - **Ejemplo**:
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
> Para más detalles sobre cómo estructurar una configuración de Tailwind CSS, consulta la documentación oficial:  
[Configuración de Tailwind CSS](https://tailwindcss.com/docs/configuration)

### 2. **`ignoredTailwindConfigFromModules`**  
   - **Tipo**: `Array` o `String ('all')`  
   - **Por defecto**: `[]`  
   - **Descripción**: Lista las configuraciones específicas de Tailwind de los módulos que se deben ignorar. Si se establece en `'all'`, se excluirán las configuraciones de todos los módulos.  

### 3. **`ignoredCssFromModules`**  
   - **Tipo**: `Array` o `String ('all')`  
   - **Por defecto**: `[]`  
   - **Descripción**: Especifica los módulos cuyo CSS debe excluirse de la compilación final. Si se establece en `'all'`, se excluirá el CSS de todos los módulos.  

### 4. **`includeTailwindConfigFromParentThemes`**  
   - **Tipo**: `Boolean`  
   - **Por defecto**: `true`  
   - **Descripción**: Determina si el tema debe heredar las configuraciones de Tailwind de sus temas principales.  

### 5. **`includeCssSourceFromParentThemes`**  
   - **Tipo**: `Boolean`  
   - **Por defecto**: `true`  
   - **Descripción**: Determina si los archivos fuente de CSS de los temas principales deben incluirse en la compilación final.  

### 6. **`exposeNpmPackages`**  
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
    Elimina configuraciones de CSS o Tailwind no deseadas de módulos específicos o de todos los módulos, manteniendo una compilación final limpia y optimizada.

4. **Integración con Tailwind**:  
    Los temas pueden aprovechar al máximo Tailwind CSS con un enfoque basado en utilidades y control total sobre su configuración.

5. **Integración de Paquetes NPM**:  
    Exponer paquetes NPM simplifica la gestión de dependencias, permitiendo a los temas usar directamente librerías de terceros. Estas pueden incluirse en las plantillas mediante `$block->getViewLibFileUrl()`.

---

## Notas Clave

- El archivo de configuración utiliza el formato **CJS** para garantizar compatibilidad entre entornos.
- El CSS y las configuraciones de Tailwind excluidas de los módulos se omiten por completo, reduciendo estilos innecesarios.
- Exponer paquetes NPM como objetos permite una integración precisa con librerías de terceros.

Aprovechando este sistema de configuración, **{{ config.extra.components_name }}** garantiza que los temas sean potentes, personalizables y eficientes para todas las necesidades del frontend.
