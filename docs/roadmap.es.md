# Hoja de ruta

Dónde está el proyecto y hacia dónde va. Esta hoja de ruta es deliberadamente de alto nivel y puede cambiar — sigue las [GitHub Discussions](https://github.com/mage-obsidian/module-modern-frontend/discussions) para novedades.

## ✅ Disponible hoy

- **Motor core** — build de Vite con HMR dentro de Magento, Tailwind CSS 4, ESM nativo, resolución de herencia de temas, interceptores de JS y precompilación por tema.
- **Islas Vue 3** — componentes interactivos montados de forma diferida sobre páginas renderizadas en servidor, con `modulepreload` automático del grafo de islas eager.
- **Motor Twig (opcional)** — escribe plantillas `.twig` junto a `.phtml`.
- **CLI** — generación del contrato de configuración, gestión de HMR, inspección de módulos/temas.
- **Características de rendimiento** — generación opt-in de critical CSS, datos estructurados JSON-LD (Organization, WebSite, BreadcrumbList, Product).
- **Storefront** — `module-storefront` más módulos de compatibilidad para catálogo, búsqueda, cliente, ventas, wishlist, reseñas y más, junto con el tema OBSIDIAN. Míralo funcionando en la [demo en vivo]({{ config.extra.demo_url }}).
- **Checkout completo** — un checkout de una página que lleva un carrito hasta un pedido realizado: invitado y con sesión, direcciones, selección de método de envío, totales, cupones, mensajes de regalo, multishipping, compra instantánea y tarjetas guardadas.
- **Punto de extensión para métodos de pago** — un método de pago puede dibujar su propia interfaz dentro de la isla del checkout, pedir sus propios campos y entregar al comprador a una pasarela y traerlo de vuelta. Lo verificado es el mecanismo, ejercitado con un método de prueba construido para el harness; ninguna pasarela comercial ha sido verificada (ver abajo).
- **Traducciones** — `bin/magento mage-obsidian:i18n:collect` recolecta frases de `.vue`, `.ts`, `.js` y `.twig` hacia el `i18n/<locale>.csv` de cada componente; el tema default distribuye `en_US` y `es_ES`.

## 📊 Qué se ha verificado

Medido el 2026-09-22 contra **Magento Open Source 2.4.9** con el
[harness de verificación](https://github.com/mage-obsidian/storefront-verification), sobre el
par `theme-default` / `theme-base`:

| Registro | Cifra |
|---|---|
| Entradas de paridad | 485 — 317 cubiertas, 138 fuera de alcance, 27 resueltas, 3 bloqueadas |
| Page layouts | 15 entradas, 13 cubiertas por una prueba ejecutada, 2 fuera de alcance |
| Pruebas unitarias del motor de build | 321 |
| Pruebas unitarias del harness | 268 |

Una entrada "cubierta" significa que una prueba se ejecutó y observó el comportamiento en esa
plataforma; una declaración en un tema nunca cuenta como cobertura por sí sola.

**Lo que estas cifras no dicen:**

- **Ninguna pasarela de pago comercial ha sido verificada.** El punto de extensión de pagos se
  ejercita con un método simulado construido para el harness. Una pasarela real necesita su
  propia verificación.
- **Una plataforma, una versión.** Todo lo anterior se observó en Magento Open Source 2.4.9.
  Nada aquí afirma compatibilidad con Adobe Commerce ni con otra minor 2.4.x.
- **Entradas aún abiertas.** Las 3 bloqueadas y las 138 fuera de alcance llevan su razón en el
  registro; no se cuentan en silencio como funcionando.

## 🚧 En progreso

- **Paridad total con Luma para el tema default** — cerrar las entradas que el registro sigue
  listando como bloqueadas o no cubiertas, para que una tienda pueda cambiarse a MageObsidian
  sin perder funcionalidad estándar.
- **Adobe Commerce** — `mage-obsidian:frontend:doctor` ahora detecta Adobe Commerce e
  inventaria qué familias del storefront exclusivas de Commerce tiene habilitadas una tienda,
  y cuáles de ellas tienen un módulo de MageObsidian instalado. El inventario reporta qué está
  instalado; no afirma que nada de eso haya sido verificado en esa plataforma.

## 🔜 Planificado

- **Release estable** al alcanzar la paridad, con notas de versión curadas y una guía de actualización.
- **Vitrina** de tiendas usando MageObsidian en producción — [¡cuéntanos de la tuya!](https://github.com/mage-obsidian/module-modern-frontend/discussions)

!!! note "Una nota sobre el ritmo"
    MageObsidian se desarrolla en el tiempo libre de su mantenedor. Si te ahorra tiempo, considera [apoyar el proyecto](support/project.md) — eso acelera directamente esta hoja de ruta.
