---
description: "Una comparación honesta de MageObsidian, Hyvä y Luma, incluyendo cuándo no elegir MageObsidian."
---
# Elegir un frontend: MageObsidian vs Hyvä vs Luma

Magento 2 tiene más de una respuesta a "¿cómo debería construirse el frontend de mi tienda?". Esta página es una comparación honesta para ayudarte a decidir — incluyendo cuándo **no** elegir MageObsidian.

## De un vistazo

<div class="mo-table-scroll" tabindex="0" role="region" aria-label="Comparación" markdown>

<table markdown>
<thead markdown>
<tr markdown>
<th scope="col" markdown>Característica</th>
<th scope="col" markdown>**MageObsidian**</th>
<th scope="col" markdown>**Hyvä**</th>
<th scope="col" markdown>**Luma / Blank**</th>
</tr>
</thead>
<tbody markdown>
<tr markdown>
<th scope="row" markdown>Licencia</th>
<td markdown>MIT (gratis, open source)</td>
<td markdown>Theme open source (OSL 3.0 / AFL 3.0, gratis desde nov 2025); Checkout, Enterprise y UI siguen siendo de pago</td>
<td markdown>Incluido con Magento</td>
</tr>
<tr markdown>
<th scope="row" markdown>CSS</th>
<td markdown>Tailwind CSS 4</td>
<td markdown>Tailwind CSS</td>
<td markdown>LESS</td>
</tr>
<tr markdown>
<th scope="row" markdown>JavaScript</th>
<td markdown>Islas Vue 3 + ESM nativo</td>
<td markdown>Alpine.js</td>
<td markdown>RequireJS + jQuery + Knockout</td>
</tr>
<tr markdown>
<th scope="row" markdown>Tooling de build</th>
<td markdown>Vite (dev server + HMR)</td>
<td markdown>Build propio</td>
<td markdown>Grunt / deploy estático</td>
</tr>
<tr markdown>
<th scope="row" markdown>Plantillas</th>
<td markdown>`.phtml` + motor Twig opcional</td>
<td markdown>`.phtml` (sistema de temas propio)</td>
<td markdown>`.phtml`</td>
</tr>
<tr markdown>
<th scope="row" markdown>Layout XML de Magento</th>
<td markdown>Nativo — layouts, bloques y herencia de temas siguen funcionando</td>
<td markdown>Reemplazado por su propio enfoque simplificado</td>
<td markdown>Nativo</td>
</tr>
<tr markdown>
<th scope="row" markdown>Ecosistema de extensiones</th>
<td markdown>Joven — módulos de compatibilidad para los dominios core</td>
<td markdown>Grande — amplia cobertura de terceros</td>
<td markdown>Universal</td>
</tr>
<tr markdown>
<th scope="row" markdown>Madurez</th>
<td markdown>Estable (4.0, octubre de 2026)</td>
<td markdown>Probado en producción desde 2021</td>
<td markdown>Default legacy</td>
</tr>
<tr markdown>
<th scope="row" markdown>Rendimiento</th>
<td markdown>Lighthouse 100/100/100/100 en la [demo en vivo]({{ config.extra.demo_url }})</td>
<td markdown>Excelente</td>
<td markdown>Pobre sin mucho tuning</td>
</tr>
</tbody>
</table>

</div>

## Qué hace diferente a MageObsidian

La decisión de diseño central: **modernizar el toolchain sin reemplazar la arquitectura frontend de Magento.**

- Tu **layout XML, bloques, ViewModels y herencia de temas** funcionan exactamente como los define el core de Magento. Un desarrollador que conoce el theming de Magento ya sabe cómo se organiza un tema de MageObsidian.
- Los módulos extienden el JavaScript de otros módulos mediante **interceptores** — el mismo patrón de plugins `before`/`around`/`after` que Magento usa en PHP, portado al build de JS.
- El ciclo de desarrollo es **Vite con HMR**: edita una plantilla, una clase de Tailwind o un componente Vue y velo al instante, dentro de una instancia real de Magento.
- Todo tiene **licencia MIT**, desde el motor de build hasta el tema del storefront.

## Cuándo elegir cada uno

**Elige Hyvä** si necesitas hoy un stack probado en producción — el theme ahora es gratuito y open source — con productos premium de pago (Checkout, Enterprise) y un gran ecosistema de extensiones compatibles. Es un producto excelente y la opción más segura para muchas agencias en este momento.

**Elige MageObsidian** si quieres un stack completamente open source, prefieres Vue sobre Alpine, valoras conservar el sistema de layouts nativo de Magento y te sientes cómodo adoptando un proyecto que aún está completando la paridad total con Luma (mira la [hoja de ruta](../project/roadmap.md)).

**Quédate en Luma** solo si mantienes una tienda existente con mucha inversión en personalizaciones sobre Luma y todavía no hay presupuesto para migrar.

!!! tip "Pruébalo en minutos"
    La forma más rápida de formarte una opinión es la [demo en vivo]({{ config.extra.demo_url }}) y la [guía de instalación](../getting-started/installation.md) en una instancia de prueba.
