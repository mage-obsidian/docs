# Configuración del módulo

## Configuración de CSS

En **{{ config.extra.components_name }}**, la inclusión de CSS personalizado desde módulos es sencilla y eficiente. El sistema rastrea automáticamente el siguiente punto de entrada en los módulos compatibles:  
```
app/code/Vendor/ModuleName/view/frontend/web/css/module.extend.css
```

Este archivo será incluido para cada módulo que lo defina, a menos que se configure explícitamente en el tema que se debe excluir (más detalles sobre esta funcionalidad se tratarán más adelante).

### ¿Cómo Funciona?

1. **Orden de Importación**  
    Los archivos CSS se cargan según la **prioridad de los módulos** definida en Magento. El orden se determina mediante la configuración de `sequence` en el archivo `module.xml` de cada módulo. Esto permite controlar el orden de importación del CSS de los módulos. Además, todo el CSS de los módulos se carga **antes del CSS de los temas**.
    
    > Para más detalles sobre cómo configurar el orden de carga de los módulos, consulta la documentación oficial de Magento:  
    [Configurar el orden de carga de componentes](https://developer.adobe.com/commerce/php/development/build/component-load-order).

    Un ejemplo típico de orden de importación sería:

    ```css
    /* CSS de módulos */
    @import "/var/www/html/app/code/Vendor/ModuleA/view/frontend/web/css/module.extend.css"; /* Módulo A */
    @import "/var/www/html/app/code/Vendor/ModuleB/view/frontend/web/css/module.extend.css"; /* Módulo B */
    
    /* CSS de temas */
    @import "/var/www/html/app/design/frontend/Vendor/ThemeParent/web/css/theme.source.css"; /* Tema padre */
    @import "/var/www/html/app/design/frontend/Vendor/CurrentTheme/web/css/theme.source.css"; /* Tema actual */
    ```

    - **Módulos**: Si un módulo desea incluir CSS personalizado, debe usar el archivo ubicado en `view/frontend/web/css/module.extend.css` como su punto de entrada. **{{ config.extra.components_name }}** rastrea automáticamente estos archivos para módulos compatibles.
    - **Temas**: El punto de entrada del CSS de los temas siempre es `web/css/theme.source.css`.
     
2. **Flexibilidad con la Configuración del Tema**  
     Como se mencionó anteriormente, la configuración del tema permite **ignorar las entradas CSS de módulos específicos**. Esto brinda flexibilidad para determinar qué estilos se incluirán en la compilación final.

### Salida de CSS Optimizada

**{{ config.extra.components_name }}** utiliza **Tailwind CSS** y técnicas de tree-shaking para generar un único archivo CSS optimizado. Este archivo final incluye solo los estilos necesarios para el frontend, garantizando un tamaño mínimo y un rendimiento máximo.

### Beneficios Clave

- **Modularidad**: El CSS de los módulos se integra automáticamente sin esfuerzo adicional.
- **Control**: Ajusta el orden de importación utilizando la configuración de `sequence` en `module.xml`, o incluye/excluye CSS de módulos según las configuraciones del tema.
- **Rendimiento**: El archivo CSS final optimizado mejora los tiempos de carga y reduce el exceso de estilos innecesarios.

## Configuración de Módulos

En **{{ config.extra.components_name }}**, cada módulo compatible puede incluir configuraciones adicionales creando un archivo de configuración en:

```
view/frontend/web/module.config.ts
```

Este archivo es un **módulo ESM (ECMAScript)** que hace `export default` de un objeto de configuración leído por **{{ config.extra.components_name }}**.

### ¿Cómo Funciona?

1. **Carga de Archivos de Configuración**  
    Los archivos de configuración se cargan en el orden definido por la configuración de `sequence` en el archivo `module.xml` de cada módulo.
    
    > Para más detalles sobre cómo definir el orden de carga de los módulos, consulta la documentación oficial de Magento:  
    [Configurar el orden de carga de componentes](https://developer.adobe.com/commerce/php/development/build/component-load-order).

2. **Ejemplo de Archivo de Configuración**  
    Un ejemplo básico de un archivo `module.config.ts` sería:

    ```javascript
    export default {
         tailwind: {
              // Configuración de Tailwind CSS
         }
    };
    ```

    Actualmente, la única opción de configuración disponible es para **Tailwind CSS**, pero en futuras actualizaciones se ampliará esta funcionalidad para incluir más opciones específicas de los módulos.

3. **Sobrescribir Configuraciones de los Módulos**  
    Las configuraciones de los módulos pueden ser sobrescritas directamente en los temas creando un archivo de configuración correspondiente. Por ejemplo:

    ```
    app/design/frontend/Vendor/Theme/Vendor_Module/web/module.config.ts
    ```

    - Cuando este archivo existe, **reemplaza por completo** la configuración original proporcionada por el módulo.
    - La configuración en el tema no se trata como una extensión ni se combina (merge) con el archivo original; en su lugar, lo sobrescribe completamente.

---

### Beneficios y Potencial Futuro

- **Personalización**: Las configuraciones de los módulos se pueden adaptar para satisfacer las necesidades de proyectos o temas específicos sin modificar el código del módulo.
- **Escalabilidad**: El sistema de configuración está diseñado para admitir más opciones en futuras versiones, brindando mayor flexibilidad a los desarrolladores de módulos.
- **Control**: Los temas tienen la capacidad de sobrescribir completamente las configuraciones de los módulos, asegurando una separación clara de responsabilidades y evitando efectos no deseados.

---

### Notas Clave

- El archivo es un módulo **ESM** (`export default`), coherente con el engine de build ESM-only.
- Las configuraciones se cargan según la secuencia definida en `module.xml`. Para obtener más información, consulta la [documentación oficial de Magento](https://developer.adobe.com/commerce/php/development/build/component-load-order).
- Las configuraciones sobrescritas en los temas reemplazan completamente las configuraciones originales del módulo, sin combinarlas ni extenderlas.

## Configuración de Tailwind

**{{ config.extra.components_name }}** usa **Tailwind CSS 4**, que es **CSS-first**: los tokens de diseño se declaran en CSS (`@import "tailwindcss";` y luego `@theme { … }`), no en un config de JavaScript. Un tema declara sus tokens en `web/css/theme.source.css` (ver [Configuración de CSS](../themes/css.md)); un módulo aporta tokens/utilidades a través de su `view/frontend/web/css/module.extend.css`.

> Para la personalización de Tailwind 4 (el bloque `@theme`, las directivas `@utility` y `@source`) consulta la documentación oficial:
> [Tailwind CSS — Theme variables](https://tailwindcss.com/docs/theme) · [Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files).

---

### Cómo se detectan las clases (escaneo de fuentes)

Tailwind solo genera las clases de utilidad que realmente encuentra en tus archivos fuente. En este stack la **detección automática de Tailwind no alcanza el árbol de Magento** (su ruta base es el harness de Vite, no `app/`), así que el engine registra las fuentes explícitamente — **con herencia completa**, igual que ya hace con los componentes:

- **Componentes Vue/JS** de cada módulo compatible y del tema, resueltos a través de la cadena tema → padre.
- **Templates Twig/phtml** — el directorio `view/frontend/templates` de cada módulo compatible, **más toda la cadena de herencia de temas** (tema → padre → …).

Como resultado, una clase usada en **cualquier** template/componente de módulo, o en **cualquier** tema de la cadena de herencia (incluido un tema padre), se genera automáticamente. **No** necesitas añadir un `@source` manual para tus templates.

---

### Excluir un módulo del escaneo

Un tema puede excluir módulos concretos de la detección de clases con `ignoredTailwindConfigFromModules` en su `web/theme.config.js`:

```javascript
export default {
    // Excluye los componentes Y templates de estos módulos del escaneo de Tailwind…
    ignoredTailwindConfigFromModules: ['Vendor_ModuleA', 'Vendor_ModuleB'],
    // …o excluye todos los módulos con la cadena literal "all".
    // ignoredTailwindConfigFromModules: 'all',
};
```

- Una **lista de nombres de módulo** excluye los componentes **y** templates de esos módulos del conjunto de `@source` generado.
- La cadena literal **`"all"`** excluye todos los módulos. Los archivos del propio tema **siempre** se escanean.
- La lista **se mergea por la cadena de herencia de temas**: un tema hijo hereda las exclusiones de su padre y puede añadir más (el mismo merge aplicado a `ignoredCssFromModules`).

Es la contraparte —a nivel de escaneo de fuentes— de [`ignoredCssFromModules`](../themes/css.md), que excluye el **CSS** de un módulo (`module.extend.css`) del build.

---

### Prioridad y overrides

- El CSS de módulo (`module.extend.css`) se importa **antes** que el CSS del tema, de modo que el `theme.source.css` de un tema puede sobrescribir los tokens de módulo mediante la cascada normal de CSS.
- El orden de carga de módulos sigue la `sequence` declarada en cada `module.xml`. Ver la [documentación oficial de Magento](https://developer.adobe.com/commerce/php/development/build/component-load-order).

---

### Nota sobre el legado (Tailwind 3)

Las versiones anteriores usaban un objeto `tailwind` con `content` / `theme.extend` / `plugins` dentro de `module.config.js`. **Tailwind 4 es CSS-first y ese objeto ya no se lee.** Los tokens y utilidades ahora viven en `module.extend.css` / `theme.source.css`, y la detección de clases la maneja el engine como se describe arriba — no hay ningún array `content` que mantener.
