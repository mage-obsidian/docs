# Por qué MageObsidian

> **Nota:** Este proyecto es desarrollado en mi tiempo libre, lo que puede significar que el progreso sea más lento de lo esperado. Si deseas apoyar el desarrollo y acelerar su progreso, considera contribuir económicamente. Más detalles en la sección [Apoyo al Proyecto](../project/sponsor.md).

## Qué es

El proyecto **{{ config.site_name }}** surge como una propuesta disruptiva para revolucionar la experiencia del desarrollo frontend en Magento. Durante años, el frontend de Magento ha estado limitado por herramientas y prácticas que, aunque útiles en su momento, han añadido complejidad innecesaria al ecosistema. Tecnologías como Less, Knockout y RequireJS han transformado el desarrollo en un proceso desafiante que abruma incluso a los desarrolladores experimentados.

<div style="display: grid; justify-content: center; grid-template-columns: repeat(auto-fit, minmax(40px, 100px)); gap: 40px; justify-items: center; align-items: center; margin-top: 20px;">
  <a href="https://magento.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/magento-logo.png" alt="Magento" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://vitejs.dev" target="_blank" rel="noopener noreferrer">
     <img src="/assets/vite-logo.png" alt="Vite" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://vuejs.org" target="_blank" rel="noopener noreferrer">
     <img src="/assets/vuejs-logo.png" alt="Vue.js" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://tailwindcss.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/tailwind-logo.png" alt="TailwindCSS" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://twig.symfony.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/twig-logo.png" alt="Twig" style="max-width: 100%; height: auto;" />
  </a>
</div>


**{{ config.extra.components_name }}** busca simplificar y modernizar el desarrollo frontend en Magento mediante una alternativa innovadora y Open Source. Este proyecto introduce dos aspectos clave:

1. **{{ config.extra.components_name }}:** Ya disponibles y Open Source, estas herramientas han sido creadas para implementar un enfoque completamente nuevo en la creación de temas para Magento. Estas herramientas permiten integrar tecnologías modernas como **Vite**, **TailwindCSS**, **Vue.js** y **ESM** (Módulos de JavaScript nativos), ofreciendo una experiencia de desarrollo más accesible, eficiente y amigable. [Más sobre {{ config.extra.components_name }}](index.md).

2. **{{ config.extra.theme_name }}:** El tema base está construido por completo sobre las herramientas mencionadas y ya es funcional. No hereda nada de los temas tradicionales como **Blank** y **Luma**, lo que permite un diseño completamente nuevo, alineado con prácticas modernas y libre de las restricciones históricas del frontend de Magento. Hoy apunta a Magento Open Source; Adobe Commerce y Mage-OS son técnicamente compatibles desde el core 2.6.0 pero aún sin pruebas completas. [Más sobre {{ config.extra.theme_name }}](../guides/themes/obsidian.md) — o míralo funcionando en la [demo en vivo]({{ config.extra.demo_url }}){target=_blank rel=noopener}.

Una de las principales fortalezas de **{{ config.extra.components_name }}** es que **no sigue el enfoque de una PWA**. En lugar de ello, se apoya en el sistema existente de Layouts, Bloques y Templates de Magento, preservando su arquitectura nativa. Este enfoque permite a los desarrolladores aprovechar herramientas modernas y estándares actuales sin necesidad de alterar la compatibilidad con módulos y funcionalidades existentes, ofreciendo una experiencia de desarrollo más fluida y eficiente.

Sobre esa base nativa, **{{ config.extra.components_name }}** añade bloques de construcción modernos: los componentes Vue se montan como **[islas](../guides/vue/islands.md) con hidratación perezosa**, una capa de **[i18n](../guides/vue/i18n.md)** integrada los traduce con los diccionarios nativos de Magento, y un **[motor Twig](../guides/twig.md)** opcional —incluido por defecto y totalmente compatible con `.phtml`— está disponible para quien quiera auto-escaping de HTML y herencia de plantillas limpia.

Además, aunque el uso de paquetes de **NPM** siempre fue posible en Magento, **{{ config.extra.components_name }}** lo hace más sencillo y directo. Ahora, de manera elegante, se puede aprovechar el vasto ecosistema de herramientas y librerías disponibles, alineando el frontend de Magento con las mejores prácticas globales del desarrollo web.

## Características clave

### Componentes

- **Independencia de los temas tradicionales:** **{{ config.extra.components_name }}** elimina por completo la dependencia de temas como **Blank** y **Luma**, permitiendo un diseño moderno y flexible, libre de las limitaciones históricas que han complicado el frontend de Magento.

- **Integración con herramientas modernas:** Aprovecha tecnologías de vanguardia como **Vite**, **TailwindCSS**, **Vue.js** y **ESM** (Módulos de JavaScript nativos), ofreciendo una experiencia de desarrollo ágil y alineada con las mejores prácticas globales.

- **Actualizaciones instantáneas con Hot Module Replacement (HMR):** Proporciona una experiencia de desarrollo fluida al eliminar tiempos de espera y permitir actualizaciones inmediatas durante el desarrollo.

- **Acceso simplificado al ecosistema de NPM:** Facilita la integración de herramientas y librerías modernas mediante un acceso optimizado a **NPM**, alineando el frontend de Magento con los estándares actuales del desarrollo web.

- **Control centralizado de la representación visual:** Introduce un enfoque donde el control principal de la representación visual recae en el tema, aunque los módulos aún pueden realizar modificaciones específicas. Esto asegura una separación clara de responsabilidades, fomentando un desarrollo más modular, organizado y flexible.

- **Modernización aprovechando la base nativa:** Se apoya en el sistema nativo de Layouts, Bloques y Templates de Magento para modernizar el frontend, integrando lo mejor del ecosistema frontend de Magento con herramientas modernas.

- **Islas Vue interactivas:** Los componentes Vue se montan como **islas independientes con hidratación perezosa** —los componentes por debajo del pliegue no cuestan nada hasta entrar en el viewport, y una página sin islas no envía Vue en absoluto. Consulta [Islas Vue](../guides/vue/islands.md).

- **Internacionalización integrada:** Traduce frases en los componentes con `$t('…')` contra el `js-translation.json` nativo de Magento, con un comando recolector para las fuentes `.vue`. Consulta [Internacionalización](../guides/vue/i18n.md).

- **Datos estructurados integrados (JSON-LD):** Emite automáticamente markup de schema.org (Organization, WebSite, Breadcrumb, Product) para rich results —cacheable, sin JavaScript adicional, con un helper `json_ld` para tipos personalizados. Consulta [Datos estructurados](../guides/features/structured-data.md).

- **Helper de imágenes para Core Web Vitals:** Un helper `image` renderiza `<img>`/`<picture>` con `width`/`height` (auto-detectados en assets) para eliminar el CLS, más `loading`/`fetchpriority` para priorizar la imagen LCP. Consulta [Imágenes responsivas](../guides/features/images.md).

- **Estado compartido opt-in (Pinia):** Las islas pueden compartir estado reactivo mediante una única Pinia a nivel de página —cargada solo por los componentes que importan un store (ninguno para el resto)— con un puente `useCustomerData` listo que espeja las secciones de carrito/cliente de Magento, compatible con FPC. Consulta [Estado compartido](../guides/vue/state.md).

- **Motor Twig opcional, incluido por defecto:** Un motor de plantillas [Twig](../guides/twig.md) viene junto al `.phtml` nativo —totalmente compatible, nunca obligatorio (se deshabilita con un comando). Añade auto-escaping de HTML y herencia de plantillas limpia para quien la quiera.

- **Generadores de scaffolding:** `bin/magento mage-obsidian:generate:{module,theme,component}` crean módulos, temas y componentes Vue ya cableados para el frontend. Consulta [Generadores](../getting-started/scaffolding.md).

- **Experiencia amigable para desarrolladores:** Diseñado para ser intuitivo y agradable, **{{ config.extra.components_name }}** promueve la creatividad y simplifica el uso de herramientas ampliamente adoptadas en la industria, haciendo del desarrollo frontend una tarea mucho más placentera.

- **Soporte multi-tema:** Compatible con una estructura que permite gestionar múltiples temas derivados, evitando la duplicidad de código y lógica. Esto facilita el mantenimiento de diversos diseños específicos para cada tienda o marca dentro de un mismo ecosistema.

- **Herencia entre temas:** Implementa una jerarquía de herencia que permite extender y reutilizar temas existentes. Esto significa que los temas compatibles con esta nueva estructura pueden compartir funcionalidades y estilos comunes, reduciendo el esfuerzo de desarrollo y mantenimiento.

### Tema

- **SEO-friendly desde su base:** Diseñado para garantizar tiempos de carga rápidos, URLs limpias, y una estructura que maximiza el rendimiento en motores de búsqueda. El tema aprovecha el soporte de componentes optimizados para generar un frontend ágil y bien estructurado.

- **Rendimiento excepcional:** Gracias a los componentes subyacentes, el tema está optimizado para cargar solo lo necesario, lo que resulta en tiempos de carga ultrarrápidos. Esto mejora tanto la experiencia del usuario como las métricas de rendimiento, como las Core Web Vitals de Google.

[![Reporte de Lighthouse: 100 en Rendimiento, Accesibilidad, Buenas prácticas y SEO](/assets/lighthouse-100.png)]({{ config.extra.demo_url }}){ .lighthouse-shot target=_blank rel=noopener }

- **Diseño moderno y personalizable:** Construido con los estándares más recientes, el tema permite una personalización completa para adaptarse a las necesidades de cualquier negocio. Su flexibilidad asegura que los desarrolladores puedan crear experiencias únicas sin comprometer el rendimiento.

- **Actualizaciones sencillas y rápidas:** El diseño del tema facilita su mantenimiento, asegurando que las mejoras y actualizaciones se puedan implementar sin afectar la estabilidad del sitio.

- **Diseño modular:** El tema permite extender y modificar partes específicas sin afectar la estructura global, facilitando la creación de variaciones únicas para cada marca o línea de productos.

- **Preparado para futuros estándares:** Desarrollado con un enfoque en el futuro, el tema se adapta fácilmente a los avances en tecnología frontend y las necesidades cambiantes de los negocios.

## Cómo encaja todo

**{{ config.extra.components_name }}** es un kit de herramientas moderno y de código abierto
diseñado para redefinir la experiencia de desarrollo frontend en Magento. Al abordar desafíos
históricos y aprovechar las mejores prácticas actuales de desarrollo web,
{{ config.extra.components_name }} simplifica y moderniza la creación de temas para Magento.

Este enfoque introduce un flujo de trabajo más accesible, eficiente y amigable para los desarrolladores.

### Beneficios

!!! tip "Por qué los equipos eligen {{ config.extra.components_name }}"

    - **Eficiencia:** Reduce el tiempo de desarrollo con herramientas y flujos de trabajo optimizados.
    - **Flexibilidad:** Crea soluciones personalizadas manteniendo la compatibilidad con las funcionalidades principales de Magento.
    - **Accesibilidad:** Una configuración simplificada facilita que nuevos desarrolladores comiencen rápidamente.
    - **Estándares modernos:** Aprovecha las mejores prácticas globales en desarrollo web para una experiencia fluida.

## ¿Es estable?

Sí: MageObsidian 4.0 es una versión estable, y la página [Novedades de 4.0](whats-new-4.md) lista lo que trae. [Versiones y soporte](../project/versioning.md) explica los dos trenes de versiones y qué cubre el contrato de 4.x.
