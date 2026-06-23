# {{ config.extra.theme_name }}

**{{ config.extra.theme_name }}** es el tema de referencia para storefront, construido por completo
con los **{{ config.extra.components_name }}**. Reemplaza el frontend Luma de Magento por un stack
moderno — plantillas **Twig**, **Vite**, **TailwindCSS 4** e **islas Vue** con hidratación diferida —
manteniendo los layouts, bloques y view models nativos de Magento. Ya es funcional y cubre el mismo
terreno que Luma (catálogo, checkout, cliente, búsqueda, carrito, wishlist, comparación, reseñas y
ventas).

Esta página es una guía práctica para **usar y extender** el tema. Para el mecanismo común a todo
tema compatible, consulta [Temas Compatibles](../components/themes/0010-overview.md).

!!! warning "Compatibilidad"

    - ✅ **Magento Open Source 2.4.6+** — soportado hoy.
    - 🚧 **Adobe Commerce** y **Mage-OS** — aún no soportados. El soporte está planeado para el futuro.

---

## Arquitectura: dos capas

El tema se entrega como dos temas apilados para separar limpiamente el diseño de la infraestructura:

<div class="grid cards" markdown>

-   :material-cube-outline:{ .lg .middle } __`MageObsidian/theme-base`__

    ---

    La base técnica neutral: cableado del build y plantillas estructurales, **sin** tokens de
    diseño. Suele ser el padre del que heredas cuando empiezas un look completamente nuevo.

-   :material-palette-swatch:{ .lg .middle } __`MageObsidian/default`__

    ---

    La piel **OBSIDIAN**: tokens de diseño, plantillas Twig estilizadas y una capa demo de moda
    reemplazable. Hereda de ella si quieres conservar OBSIDIAN y ajustar; reemplaza sus tokens para
    rebrandear.

</div>

La herencia se declara con el `theme.xml` nativo de Magento:

```xml
<theme xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:noNamespaceSchemaLocation="urn:magento:framework:Config/etc/theme.xsd">
    <title>MageObsidian — Default (Obsidian)</title>
    <parent>MageObsidian/theme-base</parent>
</theme>
```

El directorio de un tema se ve así:

```text
app/design/frontend/MageObsidian/default/
├── theme.xml                         # título + padre
├── registration.php
├── etc/
│   └── mage_obsidian_compatibility.xml   # opt-in al build de MageObsidian
├── web/
│   ├── theme.config.js               # opciones de build (ESM)
│   ├── css/
│   │   └── theme.source.css          # tokens de diseño @theme + estilos globales
│   └── generated/                    # salida del build de Vite (no editar)
└── Magento_Theme/                    # overrides de Twig por módulo
    └── templates/
        └── html/
            ├── header.twig
            └── footer.twig
```

---

## Activar el tema

1. Selecciónalo en el Admin en **Stores → Configuration → General → Design → Design Theme**
   (o vía `bin/magento config:set`) y aplícalo a tu store view.
2. Regenera el contrato PHP ↔ JS para que el motor de build vea el tema:

    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

3. Compila los assets del frontend a disco:

    ```bash
    mage-obsidian:build-themes --theme <theme>   # omite --theme para compilar todos
    ```

Consulta [Instalación](../getting-started/installation.md) para la configuración inicial.

---

## Desarrollar con recarga en vivo (HMR)

Para el día a día, levanta el dev server de Vite para que los cambios en `.vue`, CSS y Twig se
recarguen en caliente en el navegador. Habilita HMR y conecta nginx una vez, luego arranca el
server por sesión:

```bash
bin/magento deploy:mode:set developer
bin/magento mage-obsidian:frontend:hmr --enable                # una vez: HMR es un flag de developer mode
bin/magento mage-obsidian:frontend:dev --print-nginx           # una vez: pega el snippet en tu server block de nginx
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme   # por sesión
```

El snippet de nginx redirige las peticiones `/static` al dev server de Vite — el host y el puerto
salen de tu config, no los eliges a mano. HMR se ignora en modo producción. Recorrido completo y
solución de problemas en [Configuración de HMR](../components/modules/0110-hmr-configuration.md) y
[Flujo de Desarrollo](../getting-started/development.md).

---

## Desplegar a producción

**No hay un paso de build aparte**. MageObsidian se engancha al deploy de static-content estándar de
Magento: sus plugins excluyen los temas modernos del pipeline legacy de Less/RequireJS e inyectan la
salida de Vite (minificada, con tree-shaking y hashing) como parte del comando normal:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

Solo los temas que incluyen `etc/mage_obsidian_compatibility.xml` pasan por el pipeline de Vite; el
resto sigue el deploy nativo de Magento sin tocarse. Consulta
[Compilar Assets Estáticos](../components/modules/0120-vite-build.md).

---

## Re-tematizar: tokens de diseño

Re-pintar OBSIDIAN es **CSS-first**: cada color, fuente, radio y easing vive en el bloque `@theme`
de `web/css/theme.source.css`. Cambia esos tokens y todo el tema lo sigue — sin tocar configuración
JavaScript.

```css
@import "tailwindcss";

@theme {
  /* — Obsidiana: casi-negro vítreo, subtono violeta frío — */
  --color-obsidian-950: #08070b;
  --color-obsidian-900: #0d0c12;
  --color-obsidian-800: #16151d;

  /* — Alabastro: base clara mineral fría (no cream cálido) — */
  --color-alabaster: #eceaf0;
  --color-alabaster-raised: #f6f5f8;
  --color-paper: #ffffff;

  /* — Tinta (texto) + acentos funcionales contenidos — */
  --color-ink: #141319;
  --color-accent: #2f6e66;
  --color-sale: #9a5b3f;

  /* — Tipografía — */
  --font-display: "Bodoni Moda", Georgia, serif;
  --font-body: "Hanken Grotesk", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* — Filo conchoidal afilado + easing de firma — */
  --radius-edge: 2px;
  --ease-obsidian: cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

Las plantillas consumen estos tokens como utilidades de Tailwind (`font-display`, `text-ink`,
`bg-alabaster`, `rounded-edge`, …), así que editar un token re-fluye todas las pantallas a la vez.

!!! tip "No edites `default` en su lugar"

    Para rebrandear, crea tu propio tema hijo (más abajo) y sobrescribe solo los tokens que
    necesites. Así tus cambios quedan a salvo de actualizaciones. Para el conjunto completo de
    opciones de CSS y la exclusión de CSS de módulos, consulta
    [Configuración de CSS](../components/themes/0030-css-configuration.md).

---

## Construir tu propio tema encima

Crea un tema en `app/design/frontend/Vendor/Custom/` y hereda de `theme-base` (lienzo limpio) o de
`default` (conservar OBSIDIAN y ajustar):

!!! tip "¿`theme-base` o `default`?"

    Hereda de **`default`** cuando OBSIDIAN se acerca a lo que quieres — re-tematiza sus tokens y
    sobrescribe unas pocas plantillas. Es el camino más rápido y conservas el storefront ya
    estilizado y con paridad completa. Parte de **`theme-base`** solo cuando quieras un lienzo
    limpio y vayas a diseñar cada superficie desde cero.

1. **`registration.php`** y **`theme.xml`** con el padre de tu elección:

    ```xml
    <theme xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:noNamespaceSchemaLocation="urn:magento:framework:Config/etc/theme.xsd">
        <title>Acme — Storefront</title>
        <parent>MageObsidian/theme-base</parent>
    </theme>
    ```

2. **Haz opt-in** al build de MageObsidian con `etc/mage_obsidian_compatibility.xml`:

    ```xml
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

3. **`web/theme.config.js`** — opciones de build (ESM). Los tokens van en CSS, no aquí:

    ```javascript
    export default {
        includeParentThemes: false,
        ignoredCssFromModules: [],
        exposeNpmPackages: [
            { package: 'pinia', exposePath: 'pinia' },
        ],
    }
    ```

4. **`web/css/theme.source.css`** — tus tokens `@theme` (y cualquier override).

Luego ejecuta `--generate` y `mage-obsidian:build-themes` de nuevo. Referencia completa:
[Configuración de Compatibilidad](../components/themes/0020-compatibility-configuration.md) y
[Configuración del Tema](../components/themes/0040-theme-configuration.md).

---

## Sobrescribir plantillas (Twig)

Las plantillas viven en `<Vendor>_<Module>/templates/**/*.twig`. Para sobrescribir una, recrea la
misma ruta en tu tema — el fallback de Magento resuelve la versión más específica. Por ejemplo, el
título de página:

{% raw %}
```twig
{# Encabezado de página (<h1>). `block` es Magento\Theme\Block\Html\Title. #}
{% set heading = block.getPageHeading() %}
{% if heading|trim %}
<div class="page-title-wrapper mb-6{{ block.getCssClass() ? ' ' ~ block.getCssClass() }}">
    <h1 class="page-title font-display text-3xl leading-tight tracking-[0.01em] text-ink md:text-4xl">
        <span class="base" data-ui-id="page-title-wrapper" {{ block.getAddBaseAttribute()|raw }}>{{ heading }}</span>
    </h1>
    {{ child_html() }}
</div>
{% endif %}
```
{% endraw %}

Fíjate en los tokens de diseño aflorando como clases de utilidad (`font-display`, `text-ink`). Para
el runtime de Twig, helpers y filtros, consulta [Motor Twig](../twig/index.md) y
[Helpers y Filtros](../twig/helpers.md).

---

## Islas Vue y JavaScript

El tema `default` monta **islas Vue** interactivas para las partes dinámicas — búsqueda del header,
contadores de carrito / wishlist / comparación, el menú móvil, el switcher de tienda, drawers y
toasts — cada una hidratada de forma diferida para que la página siga siendo rápida. Extiendes el
tema añadiendo o sobrescribiendo componentes y exponiendo los paquetes NPM que necesites (Pinia ya
viene expuesto).

- Añade componentes y scripts bajo `web/` — consulta
  [Crear Scripts y Componentes](../components/themes/0050-components-workflow.md).
- Aprende cómo se montan las islas en
  [Islas Vue](../components/modules/0105-vue-islands.md).

---

## Qué incluye (paridad con Luma)

El tema cubre la misma superficie de storefront que Luma, reconstruida en Twig + Vue:

- **Chrome:** header, footer, navegación, menú móvil, switcher de tienda/moneda.
- **Catálogo:** listado de categoría, navegación por capas, página de detalle de producto, swatches.
- **Compra:** carrito, checkout, compra instantánea, mensajes de regalo, multishipping.
- **Cuenta:** login y cuenta de cliente, wishlist, comparación, reseñas, ventas/pedidos.
- **Búsqueda:** búsqueda rápida con autocompletado.

---

## Próximos pasos

<div class="grid cards" markdown>

-   :material-puzzle-outline:{ .lg .middle } __Temas Compatibles__

    ---

    El mecanismo completo detrás de los temas compatibles: compatibilidad, CSS, config y componentes.

    [:octicons-arrow-right-24: Resumen](../components/themes/0010-overview.md)

-   :material-leaf:{ .lg .middle } __Motor Twig__

    ---

    Escribe y sobrescribe plantillas en Twig, con helpers y filtros.

    [:octicons-arrow-right-24: Explorar Twig](../twig/index.md)

-   :material-rocket-launch:{ .lg .middle } __Primeros pasos__

    ---

    Instala los componentes y construye un tema desde cero.

    [:octicons-arrow-right-24: Requerimientos](../getting-started/requirements.md)

</div>
