# Hoja de ruta

Dónde está el proyecto y hacia dónde va. Esta hoja de ruta es deliberadamente de alto nivel y puede cambiar — sigue las [GitHub Discussions](https://github.com/mage-obsidian/module-modern-frontend/discussions) para novedades.

## ✅ Disponible hoy

- **Motor core** — build de Vite con HMR dentro de Magento, Tailwind CSS 4, ESM nativo, resolución de herencia de temas, interceptores de JS y precompilación por tema.
- **Islas Vue 3** — componentes interactivos montados de forma diferida sobre páginas renderizadas en servidor, con `modulepreload` automático del grafo de islas eager.
- **Motor Twig (opcional)** — escribe plantillas `.twig` junto a `.phtml`.
- **CLI** — generación del contrato de configuración, gestión de HMR, inspección de módulos/temas.
- **Características de rendimiento** — generación opt-in de critical CSS, datos estructurados JSON-LD (Organization, WebSite, BreadcrumbList, Product).
- **Base del storefront** — `module-storefront` más módulos de compatibilidad para catálogo, búsqueda, checkout (carrito), cliente, ventas, wishlist, reseñas y más, junto con el tema OBSIDIAN. Míralo funcionando en la [demo en vivo]({{ config.extra.demo_url }}).

## 🚧 En progreso

- **Paridad total con Luma para el tema default** — completar los dominios restantes del storefront y el QA end-to-end para que una tienda pueda cambiarse a MageObsidian sin perder funcionalidad estándar.

## 🔜 Planificado

- **Release estable** al alcanzar la paridad, con notas de versión curadas y una guía de actualización.
- **Vitrina** de tiendas usando MageObsidian en producción — [¡cuéntanos de la tuya!](https://github.com/mage-obsidian/module-modern-frontend/discussions)

!!! note "Una nota sobre el ritmo"
    MageObsidian se desarrolla en el tiempo libre de su mantenedor. Si te ahorra tiempo, considera [apoyar el proyecto](support/project.md) — eso acelera directamente esta hoja de ruta.
