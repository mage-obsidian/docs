# Características clave

## Componentes

- **Independencia de los temas tradicionales:** **{{ config.extra.components_name }}** elimina por completo la dependencia de temas como **Blank** y **Luma**, permitiendo un diseño moderno y flexible, libre de las limitaciones históricas que han complicado el frontend de Magento.

- **Integración con herramientas modernas:** Aprovecha tecnologías de vanguardia como **Vite**, **TailwindCSS**, **Vue.js** y **ESM** (Módulos de JavaScript nativos), ofreciendo una experiencia de desarrollo ágil y alineada con las mejores prácticas globales.

- **Actualizaciones instantáneas con Hot Module Replacement (HMR):** Proporciona una experiencia de desarrollo fluida al eliminar tiempos de espera y permitir actualizaciones inmediatas durante el desarrollo.

- **Acceso simplificado al ecosistema de NPM:** Facilita la integración de herramientas y librerías modernas mediante un acceso optimizado a **NPM**, alineando el frontend de Magento con los estándares actuales del desarrollo web.

- **Control centralizado de la representación visual:** Introduce un enfoque donde el control principal de la representación visual recae en el tema, aunque los módulos aún pueden realizar modificaciones específicas. Esto asegura una separación clara de responsabilidades, fomentando un desarrollo más modular, organizado y flexible.

- **Modernización aprovechando la base nativa:** Se apoya en el sistema nativo de Layouts, Bloques y Templates de Magento para modernizar el frontend, integrando lo mejor del ecosistema frontend de Magento con herramientas modernas.

- **Islas Vue interactivas:** Los componentes Vue se montan como **islas independientes con hidratación perezosa** —los componentes por debajo del pliegue no cuestan nada hasta entrar en el viewport, y una página sin islas no envía Vue en absoluto. Consulta [Islas Vue](../components/modules/0105-vue-islands.md).

- **Internacionalización integrada:** Traduce frases en los componentes con `$t('…')` contra el `js-translation.json` nativo de Magento, con un comando recolector para las fuentes `.vue`. Consulta [Internacionalización](../components/modules/0107-i18n.md).

- **Datos estructurados integrados (JSON-LD):** Emite automáticamente markup de schema.org (Organization, WebSite, Breadcrumb, Product) para rich results —cacheable, sin JavaScript adicional, con un helper `json_ld` para tipos personalizados. Consulta [Datos estructurados](../components/modules/0130-structured-data.md).

- **Motor Twig opcional, incluido por defecto:** Un motor de plantillas [Twig](../twig/index.md) viene junto al `.phtml` nativo —totalmente compatible, nunca obligatorio (se deshabilita con un comando). Añade auto-escaping de HTML y herencia de plantillas limpia para quien la quiera.

- **Generadores de scaffolding:** `bin/magento mage-obsidian:generate:{module,theme,component}` crean módulos, temas y componentes Vue ya cableados para el frontend. Consulta [Generadores](../getting-started/scaffolding.md).

- **Experiencia amigable para desarrolladores:** Diseñado para ser intuitivo y agradable, **{{ config.extra.components_name }}** promueve la creatividad y simplifica el uso de herramientas ampliamente adoptadas en la industria, haciendo del desarrollo frontend una tarea mucho más placentera.

- **Soporte multi-tema:** Compatible con una estructura que permite gestionar múltiples temas derivados, evitando la duplicidad de código y lógica. Esto facilita el mantenimiento de diversos diseños específicos para cada tienda o marca dentro de un mismo ecosistema.

- **Herencia entre temas:** Implementa una jerarquía de herencia que permite extender y reutilizar temas existentes. Esto significa que los temas compatibles con esta nueva estructura pueden compartir funcionalidades y estilos comunes, reduciendo el esfuerzo de desarrollo y mantenimiento.

## Tema

- **SEO-friendly desde su base:** Diseñado para garantizar tiempos de carga rápidos, URLs limpias, y una estructura que maximiza el rendimiento en motores de búsqueda. El tema aprovecha el soporte de componentes optimizados para generar un frontend ágil y bien estructurado.

- **Rendimiento excepcional:** Gracias a los componentes subyacentes, el tema está optimizado para cargar solo lo necesario, lo que resulta en tiempos de carga ultrarrápidos. Esto mejora tanto la experiencia del usuario como las métricas de rendimiento, como las Core Web Vitals de Google.

- **Diseño moderno y personalizable:** Construido con los estándares más recientes, el tema permite una personalización completa para adaptarse a las necesidades de cualquier negocio. Su flexibilidad asegura que los desarrolladores puedan crear experiencias únicas sin comprometer el rendimiento.

- **Actualizaciones sencillas y rápidas:** El diseño del tema facilita su mantenimiento, asegurando que las mejoras y actualizaciones se puedan implementar sin afectar la estabilidad del sitio.

- **Diseño modular:** El tema permite extender y modificar partes específicas sin afectar la estructura global, facilitando la creación de variaciones únicas para cada marca o línea de productos.

- **Preparado para futuros estándares:** Desarrollado con un enfoque en el futuro, el tema se adapta fácilmente a los avances en tecnología frontend y las necesidades cambiantes de los negocios.


