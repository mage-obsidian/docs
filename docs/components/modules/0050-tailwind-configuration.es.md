# Configuración de Tailwind

**{{ config.extra.components_name }}** usa **Tailwind CSS 4**, que es **CSS-first**: los tokens de diseño se declaran en CSS (`@import "tailwindcss";` y luego `@theme { … }`), no en un config de JavaScript. Un tema declara sus tokens en `web/css/theme.source.css` (ver [Configuración de CSS](../themes/0030-css-configuration.md)); un módulo aporta tokens/utilidades a través de su `view/frontend/web/css/module.extend.css`.

> Para la personalización de Tailwind 4 (el bloque `@theme`, las directivas `@utility` y `@source`) consulta la documentación oficial:
> [Tailwind CSS — Theme variables](https://tailwindcss.com/docs/theme) · [Detecting classes in source files](https://tailwindcss.com/docs/detecting-classes-in-source-files).

---

## Cómo se detectan las clases (escaneo de fuentes)

Tailwind solo genera las clases de utilidad que realmente encuentra en tus archivos fuente. En este stack la **detección automática de Tailwind no alcanza el árbol de Magento** (su ruta base es el harness de Vite, no `app/`), así que el engine registra las fuentes explícitamente — **con herencia completa**, igual que ya hace con los componentes:

- **Componentes Vue/JS** de cada módulo compatible y del tema, resueltos a través de la cadena tema → padre.
- **Templates Twig/phtml** — el directorio `view/frontend/templates` de cada módulo compatible, **más toda la cadena de herencia de temas** (tema → padre → …).

Como resultado, una clase usada en **cualquier** template/componente de módulo, o en **cualquier** tema de la cadena de herencia (incluido un tema padre), se genera automáticamente. **No** necesitas añadir un `@source` manual para tus templates.

---

## Excluir un módulo del escaneo

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

Es la contraparte —a nivel de escaneo de fuentes— de [`ignoredCssFromModules`](../themes/0030-css-configuration.md), que excluye el **CSS** de un módulo (`module.extend.css`) del build.

---

## Prioridad y overrides

- El CSS de módulo (`module.extend.css`) se importa **antes** que el CSS del tema, de modo que el `theme.source.css` de un tema puede sobrescribir los tokens de módulo mediante la cascada normal de CSS.
- El orden de carga de módulos sigue la `sequence` declarada en cada `module.xml`. Ver la [documentación oficial de Magento](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

---

## Nota sobre el legado (Tailwind 3)

Las versiones anteriores usaban un objeto `tailwind` con `content` / `theme.extend` / `plugins` dentro de `module.config.js`. **Tailwind 4 es CSS-first y ese objeto ya no se lee.** Los tokens y utilidades ahora viven en `module.extend.css` / `theme.source.css`, y la detección de clases la maneja el engine como se describe arriba — no hay ningún array `content` que mantener.
