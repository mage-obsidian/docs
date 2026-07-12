# Elegir un frontend: MageObsidian vs Hyvä vs Luma

Magento 2 tiene más de una respuesta a "¿cómo debería construirse el frontend de mi tienda?". Esta página es una comparación honesta para ayudarte a decidir — incluyendo cuándo **no** elegir MageObsidian.

## De un vistazo

| | **MageObsidian** | **Hyvä** | **Luma / Blank** |
|---|---|---|---|
| Licencia | MIT (gratis, open source) | Theme open source (OSL 3.0 / AFL 3.0, gratis desde nov 2025); Checkout, Enterprise y UI siguen siendo de pago | Incluido con Magento |
| CSS | Tailwind CSS 4 | Tailwind CSS | LESS |
| JavaScript | Islas Vue 3 + ESM nativo | Alpine.js | RequireJS + jQuery + Knockout |
| Tooling de build | Vite (dev server + HMR) | Build propio | Grunt / deploy estático |
| Plantillas | `.phtml` + motor Twig opcional | `.phtml` (sistema de temas propio) | `.phtml` |
| Layout XML de Magento | Nativo — layouts, bloques y herencia de temas siguen funcionando | Reemplazado por su propio enfoque simplificado | Nativo |
| Ecosistema de extensiones | Joven — módulos de compatibilidad para los dominios core | Grande — amplia cobertura de terceros | Universal |
| Madurez | Pre-1.0, en desarrollo activo | Probado en producción desde 2021 | Default legacy |
| Rendimiento | Lighthouse 100/100/100/100 en la [demo en vivo]({{ config.extra.demo_url }}) | Excelente | Pobre sin mucho tuning |

## Qué hace diferente a MageObsidian

La decisión de diseño central: **modernizar el toolchain sin reemplazar la arquitectura frontend de Magento.**

- Tu **layout XML, bloques, ViewModels y herencia de temas** funcionan exactamente como los define el core de Magento. Un desarrollador que conoce el theming de Magento ya sabe cómo se organiza un tema de MageObsidian.
- Los módulos extienden el JavaScript de otros módulos mediante **interceptores** — el mismo patrón de plugins `before`/`around`/`after` que Magento usa en PHP, portado al build de JS.
- El ciclo de desarrollo es **Vite con HMR**: edita una plantilla, una clase de Tailwind o un componente Vue y velo al instante, dentro de una instancia real de Magento.
- Todo tiene **licencia MIT**, desde el motor de build hasta el tema del storefront.

## Cuándo elegir cada uno

**Elige Hyvä** si necesitas hoy un stack probado en producción — el theme ahora es gratuito y open source — con productos premium de pago (Checkout, Enterprise) y un gran ecosistema de extensiones compatibles. Es un producto excelente y la opción más segura para muchas agencias en este momento.

**Elige MageObsidian** si quieres un stack completamente open source, prefieres Vue sobre Alpine, valoras conservar el sistema de layouts nativo de Magento y te sientes cómodo adoptando un proyecto que aún está completando la paridad total con Luma (mira la [hoja de ruta](../roadmap.md)).

**Quédate en Luma** solo si mantienes una tienda existente con mucha inversión en personalizaciones sobre Luma y todavía no hay presupuesto para migrar.

!!! tip "Pruébalo en minutos"
    La forma más rápida de formarte una opinión es la [demo en vivo]({{ config.extra.demo_url }}) y la [guía de instalación](../getting-started/installation.md) en una instancia de prueba.
