---
description: "Qué cambió en cada versión de MageObsidian, seguido a través de los paquetes que lo incluyen."
---
# Registro de cambios

Desde 4.0.0, el framework y el storefront publican cada uno todos sus paquetes bajo una misma versión.
Antes de 4.0, los paquetes estaban versionados de forma independiente; ese historial se conserva más abajo.
Las funcionalidades rara vez viven en un solo paquete: un checkout cacheable es un flag del core, un módulo de
compatibilidad y una plantilla del tema aterrizando juntos. Esta página sigue al **stack**, para que
puedas leer qué cambió sin tener que recomponerlo a partir de una docena de feeds de releases.

Cada entrada nombra los paquetes y versiones que la traen. Para el historial a nivel de commit de un
paquete concreto, consulta sus releases en [GitHub](https://github.com/mage-obsidian).

---

## Framework 4.1.3 y storefront 4.2.1 — 2026-10-25

En una tienda cuyas store views usan temas distintos, MageObsidian actúa ahora solo en las store views cuyo tema es un tema MageObsidian. Una store view con cualquier otro tema recibe el comportamiento propio de Magento, como si MageObsidian no estuviera instalado. Las store views con un tema MageObsidian no cambian.

### Cambiado

- **module-modern-frontend** — la Content Security Policy estricta, en la que un script o un estilo inline solo corre con un nonce o un hash, se aplica durante la petición y solo bajo un tema MageObsidian. `config.xml` ya no fija `csp/policies/storefront/scripts/inline` ni `csp/policies/storefront/styles/inline`. El checkout y el paso de facturación con varias direcciones conservan los estilos inline, como antes, salvo que la tienda haya configurado esas páginas por su cuenta.

### Corregido

- **Widgets** (`module-catalog`, `module-sales`) — bajo otro tema, los widgets de lista de productos, productos nuevos, vistos recientemente, comparados recientemente y pedidos y devoluciones conservan las plantillas de Magento. Antes pasaban a plantillas que solo tiene un tema MageObsidian y salían vacíos.
- **Contenido CMS** (`module-storefront`) — bajo otro tema, las páginas y los bloques ya no se envuelven en `div.cms-content`, y el contenido de Page Builder sale del filtro tal como lo escribió Magento: sin estilos entregados para calcular su hash, sin dimensiones de imagen añadidas y sin scripts de comportamiento. Eso incluye los correos que envían esas store views.
- **Metadatos del head** (`module-storefront`) — bajo otro tema, no se deriva la meta descripción, no se amplía `robots` y no se añaden metadatos sociales.
- **Showcase** (`module-showcase`) — un perfil de demo que un visitante trae de otra store view del mismo dominio no cambia nada bajo otro tema: ni sobrescritura de configuración, ni variación de caché, ni telemetría.

### Notas de actualización

Solo una tienda con alguna store view en un tema que no es MageObsidian nota la diferencia. En esas store views, después del siguiente `cache:flush`:

- los widgets, el contenido CMS y el `<head>` se renderizan como los renderiza Magento;
- la Content Security Policy es la que producen Magento y la configuración propia de la tienda. Para que esas store views sigan tan estrictas como antes, fija `csp/policies/storefront/scripts/inline` y `csp/policies/storefront/styles/inline` en `0` para su sitio web. `config:set` rechaza estas rutas, porque `Magento_Csp` no las declara en `system.xml`; escríbelas en la sección `system` de `app/etc/env.php` o de `app/etc/config.php`.

Una store view cuenta como store view MageObsidian cuando su tema figura en el contrato. Un tema que hereda de `MageObsidian/default` tiene que traer su propio [`etc/mage_obsidian_compatibility.xml`](../reference/contract.md#etcmage_obsidian_compatibilityxml); heredar no alcanza. Para comprobarlo:

```bash
bin/magento mage-obsidian:frontend:config --show --themes
bin/magento mage-obsidian:frontend:doctor
```

El primero lista los temas del contrato. En el segundo, un aviso *Contract drift* significa que el contrato es anterior a los temas habilitados; `bin/magento mage-obsidian:frontend:config --generate` lo regenera, y también lo hace cada despliegue de contenido estático.

---

## Framework 4.1.2 — 2026-10-15

### Corregido

- **module-modern-frontend** — un bloque en caché guarda solo los hashes de Content Security Policy de los estilos y scripts inline que renderizó él mismo, incluidos los de sus hijos. La caché de bloques de Magento guardaba todos los hashes recogidos en la petición hasta ese bloque y los restauraba en cada acierto, así que en un listado con navegación por capas la lista de `style-src` crecía con cada combinación de filtros visitada, hasta que la cabecera de la respuesta superaba el buffer del servidor web y la página respondía 502.

### Notas de actualización

La corrección reemplaza `Magento\Csp\Model\BlockCache` mediante una preference. Si otro módulo también declara una preference para esa clase, solo se aplica una de las dos.

Los bloques cacheados antes de actualizar conservan los hashes que acumularon. Limpia la caché de bloques una vez después del deploy:

```bash
bin/magento cache:clean block_html
```

---

## Storefront 4.2.0 y theme-default 4.2.0 — 2026-10-15

`theme-default` 4.2.0 requiere storefront `^4.2`: su página de producto depende de estilos que trae `module-storefront` 4.2.0. Actualízalos juntos.

### Añadido

- **Botones de comparar y de lista de deseos** (`module-storefront`) — muestran el progreso mientras corre la petición: un anillo alrededor de los botones redondos de las tarjetas y un indicador en lugar del icono en los botones anchos. Con movimiento reducido, el indicador queda quieto.
- **Página de producto** (`theme-default`) — lista de deseos y comparar son dos botones lado a lado bajo agregar al carrito, y dicen "Quitar de la lista de deseos" y "Quitar de comparar" cuando el producto ya está en la lista. Los enlaces de alerta de precio, alerta de stock y enviar a un amigo forman una lista aparte.
- **Página de comparar** (`theme-default`) — cada producto muestra su imagen con un botón para quitarlo encima, luego agregar al carrito o elegir opciones, y la lista de deseos como icono.

### Corregido

- **Listados** (`module-storefront`) — en las tarjetas que un filtro, un orden o un cambio de página traen, los botones de comparar y de lista de deseos indican si el producto ya está en la lista. Antes aparecían sin marcar, y al pulsarlos se quitaba el producto.
- **Catálogo** (`module-catalog`) — el botón redondo de comparar de un producto comparado se rellena con el color de acento y mantiene visible su icono.
- **Formularios** (`module-storefront`) — los selects dibujan su propia flecha con espacio respecto del borde, y el texto seleccionado ya no choca con ella.
- **Lista de deseos** (`theme-default`, `module-wishlist`) — quitar y editar van sobre la imagen como iconos, cantidad y agregar al carrito comparten una fila que se ajusta en tarjetas estrechas, y el campo de nota es compacto.
- **Cabecera** (`theme-default`) — la barra fija vuelve a desenfocar la página que se desplaza por debajo. Desde 4.1.0 el contenido se veía nítido a través de ella, porque el nombre que la cabecera lleva para las transiciones entre páginas impedía que el desenfoque alcanzara la página; ahora lo lleva solo mientras corre una transición.
- **Búsqueda** (`theme-default`) — los términos de búsqueda relacionados ya no quedan entre dos líneas.

### Notas de actualización

Regenera el critical CSS después de actualizar. La copia inline conserva la regla de cabecera de 4.1.0, y con ella la cabecera sigue sin desenfoque hasta que se regenera:

```bash
bin/magento mage-obsidian:frontend:critical-css --handle=catalog_category_view
```

Repítelo para cada handle para el que generas critical CSS; consulta [Generar el critical CSS](../guides/features/performance.md#generar-el-critical-css).

---

## Framework 4.1.1 — 2026-10-13

### Cambiado

- **component-modern-frontend** — el harness de Vite requiere el motor `^4.1.0`, así que los builds reciben los cambios del motor 4.1.0 descritos abajo.

### Notas de actualización

Instala 4.1.1, no 4.1.0 sola. Los scripts que trae `module-modern-frontend` 4.1.0 importan módulos del runtime que solo existen desde el motor 4.1.0, y el harness de 4.1.0 todavía instala el motor 4.0.1, así que un build del tema con él falla en el import.

El motor 4.1.0 se publicó el 2026-10-13 a las 13:38 UTC. Hasta el 2026-10-14 a las 13:38 UTC, pnpm 11 lo rechaza por `minimumReleaseAge`. Espera, o exime esa versión concreta durante la instalación:

```bash
pnpm_config_minimum_release_age_exclude='["mage-obsidian@4.1.0"]' pnpm install --frozen-lockfile
```

---

## Framework 4.1.0 — 2026-10-13

### Añadido

- **js-package-utils** (`mage-obsidian` en npm) — el build escribe un hash `sha384` en `integrity` para cada chunk del manifest de Vite.
- **module-modern-frontend** — en el checkout, la confirmación del pedido y el paso de facturación del checkout con varias direcciones, los scripts de módulo, los enlaces `modulepreload` y el import map llevan `integrity` y `crossorigin`. Consulta [Subresource Integrity en las páginas de pago](../getting-started/deploy.md#subresource-integrity-en-las-paginas-de-pago).
- **module-modern-frontend** — `setup:static-content:deploy` compara cada script publicado con su hash del manifest y avisa de los que difieren, porque los navegadores se negarían a ejecutarlos en las páginas de pago; con `MAGE_OBSIDIAN_STRICT_DEPLOY=1` hace fallar el deploy.
- **js-package-utils** — las cookies que escribe el runtime del escaparate usan la ruta, el dominio, la duración y la marca `Secure` que publica la tienda, en lugar de valores fijos.

### Corregido

- **js-package-utils**, **module-modern-frontend** — las secciones privadas en caché quedan ligadas al sitio web, la vista de tienda y la moneda que las produjeron. Una caché de otro ámbito, o guardada antes de que existiera esa separación, se descarta en vez de mostrarse.
- **js-package-utils** — borrar una cookie también borra su variante de solo host, y la cookie que marca la sesión sigue siendo de solo host.
- **module-modern-frontend**, **module-modern-frontend-twig** — cuando el `style-src` de la página permite estilos inline, la etiqueta Twig `style` y el CSS crítico se entregan desde un script con nonce que los adopta como hoja de estilos.
- **module-modern-frontend-twig** — el filtro `number` devuelve sin cambios un valor que no es numérico, en vez de formatearlo.
- **js-package-utils** — un tema sin `web/theme.config.js` se construye como si tuviera uno vacío y hereda los valores de sus padres. Hasta 4.0.2 el build se detenía con `Cannot read properties of null (reading 'ignoredCssFromModules')`.

### Notas de actualización

Reemplazada por 4.1.1; consulta la entrada anterior.

---

## Storefront 4.1.0 y theme-default 4.1.0 — 2026-10-13

Los paquetes de la storefront requieren el framework `^4.1`, y `theme-default` requiere la storefront `^4.1`. Actualízalos juntos.

### Añadido

- **Configuración de la tienda respetada** — los atributos de cliente, los campos de dirección y la política de contraseñas configurados, en los formularios de cuenta y de checkout; la configuración de visualización de impuestos en los precios del carrito, del checkout y del producto; los límites del mini carrito y la redirección al carrito; los contadores de la navegación por capas, la longitud de búsqueda, los destinatarios de «enviar a un amigo» y otros límites del catálogo; se ocultan los enlaces a funciones que la tienda desactivó.
- **Checkout y carrito** — direcciones de facturación guardadas, instrucciones de pago offline y número de orden de compra, mensajes de validación del carrito y de sus líneas, carrito paginado, ventas cruzadas que se añaden a la bolsa, a la lista de deseos y a la comparación, un punto de extensión para renderizar transportistas, e impresión, descargas y la oferta de cuenta en la página de éxito.
- **Retiro en tienda** — paquete nuevo `module-inventory-in-store-pickup`: un selector del método de entrega y un buscador de puntos de retiro sobre los endpoints de retiro de MSI. Consulta [Retiro en tienda](../guides/modules/in-store-pickup.md).
- **CAPTCHA y reCAPTCHA** — el CAPTCHA de inicio de sesión cuando los intentos fallidos lo exigen, y reCAPTCHA en el formulario de cupón del carrito y en el de compartir la lista de deseos.
- **Catálogo** — muestras de configurables en las tarjetas del listado, con la variante completa con precio y añadida desde la tarjeta; la imagen de la categoría; precios por cantidad, incrementos de cantidad y stock en la página de producto; una fachada que carga los videos de proveedores al hacer clic; sugerencias de búsqueda; visitas a productos y términos de búsqueda registrados desde páginas en caché; widgets de productos nuevos, vistos y comparados recientemente.
- **Cuenta y ventas** — opciones, valoraciones, notas y cambios de cantidad guardados en la lista de deseos; comentarios, estado, impresión, volver a pedir y seguimiento en los documentos del pedido; líneas de bundle, descargables e impuestos fijos en los correos del pedido; la barra lateral de pedidos recientes y el widget de pedidos y devoluciones.
- **Estructura del escaparate** — selector de grupo de tiendas, logo configurado, mensaje de bienvenida y copyright; barras laterales de comparación y lista de deseos; accesos a la cuenta en el menú móvil; etiquetas de Google Ads y registro de conversiones; descubrimiento y enlaces de feeds RSS; baja de las alertas de stock desde el enlace del correo; filas de Page Builder a todo el ancho; el saludo del carrito persistente con «¿no eres tú?».
- **Seguridad** — los scripts propios del escaparate llevan Subresource Integrity en las páginas de pago, con el framework 4.1.

### Corregido

- **Checkout** — a un invitado cuyo email ya tiene cuenta se le ofrece iniciar sesión y puede seguir como invitado, como en Luma. Antes se bloqueaba.
- **Lista de deseos** — al compartir se envía la lista que se está viendo, no la predeterminada.
- **Catálogo** — las tarjetas de producto de una misma fila tienen la misma altura, con sus acciones alineadas abajo.
- **Cabecera** — la barra principal queda fija arriba al hacer scroll.
- **Páginas en caché** — la configuración del sitio publica la vista de tienda y la moneda, así que no se muestran secciones en caché de otra vista de tienda o moneda.

---

## Framework 4.0.2 — 2026-10-07

### Cambiado

- **component-modern-frontend** — el harness de Vite requiere el motor `^4.0.1` y Vue `^3.5.42`. Los builds reciben ahora las dos correcciones del motor 4.0.1: un tema hijo hereda los valores del `theme.config.js` de sus padres, y las fuentes CSS de los ancestros se detienen en `includeCssSourceFromParentThemes: false`.

### Seguridad

- **component-modern-frontend** — el lockfile del harness resuelve `@vue/server-renderer` 3.5.43, `source-map-js` 1.2.2 y `brace-expansion` 2.1.7, que cierran los avisos abiertos contra el harness.

### Notas de actualización

Ejecuta `composer update 'mage-obsidian/*'` y después `pnpm install` en `vite/`. `mage-obsidian` 4.0.2 en npm lleva el mismo código de motor que 4.0.1; solo cambiaron sus herramientas de desarrollo.

---

## Framework 4.0.1 — 2026-10-06

### Corregido

- **js-package-utils** (`mage-obsidian` en npm) — un tema hijo hereda los valores del `theme.config.js` de sus padres. Los valores por defecto se aplican después de la combinación, así que un `vue.runtimeOnly: true` o un `ignoredCssFromModules: "all"` del padre ya no se reinicia en el hijo.
- **js-package-utils** — las fuentes CSS de los temas ancestros se detienen en el ancestro más cercano que declara `includeCssSourceFromParentThemes: false`, en lugar de llegar siempre hasta el tema raíz.
- **module-modern-frontend** — un contrato regenerado con `mage-obsidian:frontend:config --generate` tiene efecto sin recargar PHP-FPM, también con `opcache.validate_timestamps=0`.
- **module-modern-frontend-cli** — `mage-obsidian:generate:theme` escribe `includeCssSourceFromParentThemes`, la clave que lee el motor, en lugar de `includeParentThemes`, que nada leía.

### Notas de actualización

`^4.0` ya resuelve los paquetes PHP a 4.0.1. El harness de Vite todavía instala el motor 3.2, así que las dos correcciones del motor llegan a un build cuando el harness pase a requerir el motor 4.0.1.

---

## Storefront 4.0.1 — 2026-10-06

### Corregido

- **theme-base** — nueve plantillas fallaban con un error fatal en PHP 8.3 y 8.4, porque la cabecera de licencia estaba en un bloque PHP cerrado antes de `declare(strict_types=1)`.
- **theme-base** — `root.phtml` leía `$headAssets`, que Magento 2.4.7 nunca asigna, así que todas las páginas devolvían HTTP 500 en 2.4.7.

### Notas de actualización

No hay nada que hacer: `^4.0` ya resuelve a 4.0.1.

---

## 4.0.0 — 2026-10-06 { #4-0-0 }

### Destacados

- **Estable.** 4.0.0 es la primera versión estable de la era monorepo.
- **Dos trenes de versiones.** El framework y el storefront publican cada uno todos sus paquetes bajo una misma versión.
- **Monorepos.** El framework y el storefront viven ahora en un repositorio cada uno.

### Notas de actualización

Consulta la [guía de actualización de 3.x a 4.0](../upgrade/3-to-4.md).

### Obsoleto

Nada.

### Mapa de versiones

Última versión de cada paquete antes de 4.0 y la versión 4.0.0.

| Paquete | Última antes de 4.0 | 4.0.0 |
|---|---|---|
| mage-obsidian/module-modern-frontend | 2.22.0 | 4.0.0 |
| mage-obsidian/module-modern-frontend-cli | 2.9.0 | 4.0.0 |
| mage-obsidian/module-modern-frontend-twig | 2.7.1 | 4.0.0 |
| mage-obsidian/component-modern-frontend | 2.7.0 | 4.0.0 |
| mage-obsidian (npm) | 3.2.0 | 4.0.0 |
| mage-obsidian/module-catalog | 3.12.0 | 4.0.0 |
| mage-obsidian/module-catalog-search | 2.2.0 | 4.0.0 |
| mage-obsidian/module-checkout | 3.12.1 | 4.0.0 |
| mage-obsidian/module-customer | 2.4.1 | 4.0.0 |
| mage-obsidian/module-downloadable | 2.2.0 | 4.0.0 |
| mage-obsidian/module-gift-message | 2.2.0 | 4.0.0 |
| mage-obsidian/module-instant-purchase | 2.2.0 | 4.0.0 |
| mage-obsidian/module-multishipping | 2.1.0 | 4.0.0 |
| mage-obsidian/module-persistent | 2.1.0 | 4.0.0 |
| mage-obsidian/module-product-alert | 2.1.0 | 4.0.0 |
| mage-obsidian/module-review | 2.3.0 | 4.0.0 |
| mage-obsidian/module-sales | 2.4.0 | 4.0.0 |
| mage-obsidian/module-search | 1.3.0 | 4.0.0 |
| mage-obsidian/module-send-friend | 2.2.0 | 4.0.0 |
| mage-obsidian/module-showcase | 1.5.0 | 4.0.0 |
| mage-obsidian/module-storefront | 3.23.0 | 4.0.0 |
| mage-obsidian/module-vault | 2.3.0 | 4.0.0 |
| mage-obsidian/module-wishlist | 2.3.0 | 4.0.0 |
| mage-obsidian/theme-base | 3.13.1 | 4.0.0 |
| mage-obsidian/theme-default | 3.21.3 | 4.0.0 |

---

## Antes de 4.0

!!! note "Dónde empieza esto"
    Todo el stack se etiquetó como `2.0.0` a la vez el **22 de junio de 2026**, y ahí empieza este
    registro. Lo anterior queda fuera de la línea actual.

---

## Septiembre 2026 { #2026-09 }

### Navegación sin frames en blanco

Seguir un enlace dentro de la tienda ya no muestra una pantalla en blanco ni una cabecera sobre un
cuerpo vacío en un teléfono lento. La página anterior se mantiene en pantalla hasta que la siguiente
analizó su contenido principal, y una barra de progreso fina y un anuncio para lectores de pantalla
confirman el clic en el acto. Las primeras visitas, las llegadas desde otros sitios y las recargas
siguen pintando de forma progresiva, así que las métricas de primera carga no cambian. Ver
[Continuidad de navegación](../guides/themes/navigation.md).

- **module-storefront** 3.23.0 — retiene la página anterior hasta que la siguiente tiene su
  contenido principal (`mage_obsidian/navigation/retain`, activado por defecto); indicador de
  progreso al hacer clic; requiere el núcleo ^2.22
- **module-modern-frontend** 2.22.0 — los scripts que se incrustan en el head se imprimen sin la
  cabecera de licencia de su archivo (`RuntimeScriptReader`)
- **module-modern-frontend-twig** 2.7.1 — `inline_view_file` quita la cabecera de licencia del
  archivo que incrusta
- **theme-default** 3.21.3 — traducción del anuncio de progreso

### Builds sin base de datos

Una tienda ahora puede construir MageObsidian en una fase sin base de datos y en otra ruta raíz, y
desplegar el resultado después: el modelo de Adobe Commerce Cloud y de cualquier pipeline que
entrega un artefacto. El deploy estático regenera el contrato del frontend desde el filesystem, con
rutas relativas a la raíz de Magento, y el build de Vite se puede saltar, comprueba que puede
escribir antes de vaciar nada y respeta las exclusiones de temas. Ver
[Adobe Commerce](../getting-started/adobe-commerce.md#build-sin-base-de-datos).

- **mage-obsidian** 3.2.0 — resolver las rutas del contrato contra la raíz de Magento; aceptar el
  schema 1.1.0; `MAGE_OBSIDIAN_BUILD_CONCURRENCY`
- **component-modern-frontend** 2.7.0 — requerir el motor ^3.2.0
- **module-modern-frontend** 2.21.0 — temas leídos del filesystem; contrato regenerado en el deploy
  estático con rutas relativas a la raíz (schema 1.1.0); `MAGE_OBSIDIAN_SKIP_VITE_BUILD`,
  comprobación de escritura y exclusiones de temas en el build de Vite; critical CSS leído de
  `web/critical/`; estado de la baseline CMS por tema
- **module-modern-frontend-cli** 2.9.0 — critical CSS escrito en `<tema>/web/critical/` con URLs
  de fuentes relativas, que el core resuelve para la tienda que lo sirve; fila de baseline CMS en
  el doctor; requiere core ^2.21

**Al actualizar:** regenera el critical CSS de cada tema; el archivo viejo en
`web/generated/critical/` desaparece con el siguiente build de Vite.

### Checkout de invitado que pide iniciar sesión, y mensajes que se repiten

Con un producto descargable en el carrito, Magento rechaza por defecto el checkout de invitado. En el
nativo, los botones de checkout le piden al invitado que inicie sesión; los nuestros navegaban a
`/checkout`, que rebotaba al carrito, y el mensaje "Guest checkout is disabled." solo salía la primera
vez. Ahora los botones llevan al invitado a iniciar sesión con un `referer` de vuelta al checkout, la
página de login lo devuelve ahí, y un mensaje de sesión que el servidor vuelve a enviar siempre se
muestra.

- **module-checkout** 3.12.1 — los botones de checkout del carrito y del minicart llevan al invitado a
  iniciar sesión cuando el carrito no admite invitados
- **module-customer** 2.4.1 — un inicio de sesión que trae `referer` vuelve a él
- **module-storefront** 3.22.1 — mostrar un mensaje de sesión repetido cuando su cookie se borró
- **theme-default** 3.21.2 — pasar la URL de login a los botones de checkout

### Instalaciones que funcionan fuera de nuestro entorno

Arreglos que salieron al instalar el stack en una tienda que no se construyó con él: valores por
defecto que solo servían en nuestro entorno, chequeos que tumbaban un deploy sano y una política que
bloqueaba las páginas de pago.

**Una instalación nueva sirve los assets construidos.** `module-modern-frontend` venía con el HMR
encendido, y Magento solo anula ese flag en modo production, así que una tienda nueva en el modo
por defecto le pedía cada asset a un dev server de Vite que no estaba corriendo: todos devolvían
404 y ninguna isla montaba. Ahora el HMR viene **apagado por defecto** y se activa a propósito.
`mage-obsidian:frontend:hmr --enable` y `mage-obsidian:frontend:dev --up` lo siguen encendiendo.
Si usas el dev server y nunca guardaste el flag, corre `bin/magento mage-obsidian:frontend:hmr
--enable` una vez después de actualizar; el doctor avisa "HMR disabled" hasta que lo hagas.

**El doctor informa la cobertura de Adobe Commerce.** En una instalación de Adobe Commerce,
`mage-obsidian:frontend:doctor` añade una sección con las familias de storefront exclusivas de
Commerce, los módulos de Commerce detrás de cada una y si un módulo de MageObsidian la cubre.

**El build de producción ya no pide ajustes del dev server.** `mage-obsidian` 3.1.0 valida las
variables del dev server solo con `--dev-server`, y solo `VITE_SERVER_HOST` y `VITE_SERVER_PORT` son
obligatorias. Sin terminal nunca pregunta. Antes, un build sin `vite/.env` abría un prompt, salía con
1 y abortaba `setup:static-content:deploy` en cualquier CI.

**Se requiere PHP 8.3.** Todos los módulos Magento de MageObsidian declaran `"php": ">=8.3"`, y
`module-modern-frontend` requiere Magento 2.4.7 o posterior. El código usa typed class constants, así
que con PHP 8.2 Composer instalaba los paquetes y después `setup:di:compile` fallaba con un parse
error. **Se deja de soportar PHP 8.2.**

**Un compile fallido conserva el delta CMS que tenías.** Cuando el binario de Tailwind faltaba,
superaba el timeout o fallaba, `module-modern-frontend` escribía un delta vacío encima del último
bueno, y las clases que el build no cubría perdían sus estilos hasta el siguiente guardado exitoso.
Ahora la hoja anterior se queda. Un compile que falla con el binario instalado se registra en el
log; si falta el binario, lo informa el doctor, como ya hacía.

**El contrato del frontend se regenera solo cuando se escribe la lista de módulos.** Cada escritura de
`config.php` o `env.php` lo regeneraba, así que una falla ahí rompía `deploy:mode:set` y
`setup:config:set`. Ahora corre solo cuando se escribe la sección `modules`, y una falla se registra
con el comando a correr en lugar de hacer fallar la escritura. Un contrato que no pasa su schema
tampoco deja reescrito el `.php`: los dos archivos se escriben solo después de validar.

**Las páginas de pago vuelven a permitir estilos inline, y el prepaint resiste una política
estricta.** Magento aplica la política en `checkout_index_index` y `multishipping_checkout_billing`,
y nuestro `styles/inline=0` de todo el storefront bloqueaba ahí los estilos inline que inyectan las
extensiones de pago. Las dos páginas vuelven al valor por defecto de Magento. El prepaint aplica sus
reglas con una hoja construible, que `style-src` no controla, y solo usa un `<style>` en navegadores
que no las soportan.

**El deploy estático avisa de los temas sin build de Vite.** Un tema cuya salida faltaba o estaba
vacía pasaba el deploy en silencio. Ahora se nombra en un aviso. Con `MAGE_OBSIDIAN_STRICT_DEPLOY=1`,
ese aviso y una falla al publicar el build hacen fallar el deploy.

**Los comandos que escriben código fuente rechazan el modo production.**
`mage-obsidian:generate:module`, `:theme`, `:component` y `mage-obsidian:i18n:collect` salen con un
error en modo production en lugar de fallar a mitad de una escritura. `mage-obsidian:frontend:dev` no
cambia.

**Las clases de Page Builder quedan fuera del delta CMS.** Las clases `pagebuilder-*` nunca resuelven
a una regla de Tailwind y llenaban la lista de no resueltas del delta. Se omiten por defecto; la lista
de prefijos es el argumento `ignoredClassPrefixes` de `ContentExporter` en `di.xml`.

**El harness de Vite se instala fuera de nuestro entorno.** `component-modern-frontend` publicaba
`vite/pnpm-workspace.yaml` con el store de pnpm en `/home/www` y el control de antigüedad de
publicaciones apagado, dos ajustes de nuestro entorno local. En cualquier máquina donde `/home/www`
no se podía escribir, `pnpm install` fallaba. Ya no están; si dependías de esa ruta del store,
define `pnpm_config_store_dir` en tu entorno. El harness declara ahora `engines.node >=22.13`, el
piso de la versión de pnpm que fija. Al actualizar una instalación cuyo `vite/node_modules` se creó con la ruta vieja del store,
borra `vite/node_modules` una vez; si no, pnpm aborta sin terminal con
`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`.

- **module-modern-frontend** 2.20.0 — HMR apagado por defecto; contrato validado antes de escribir y
  regenerado solo al escribir la lista de módulos; delta CMS conservado si el compile falla y clases
  de Page Builder omitidas; estilos inline de vuelta en las páginas de pago y prepaint por CSSOM;
  aviso en el deploy para temas sin build de Vite; inventario del storefront de Adobe Commerce;
  PHP 8.3 y Magento 2.4.7
- **module-modern-frontend-cli** 2.8.0 — sección de Adobe Commerce en el doctor; los comandos que
  escriben código fuente rechazan el modo production; requiere core ^2.20
- **component-modern-frontend** 2.6.0 — quitar del harness los ajustes de pnpm de nuestro
  entorno; requerir el motor ^3.1.0 y Node 22.13
- **mage-obsidian** 3.1.0 — validar los ajustes del dev server solo con `--dev-server`
- **module-catalog** 3.12.0 — ubicar la columna de filtros donde la declara el page layout
- **theme-base** 3.13.1 — dar a las columnas laterales de `2columns-right` y `3columns` las
  clases que necesita la columna de filtros
- **module-storefront** 3.22.0, **module-showcase** 1.5.0 — incluir el diccionario `en_US` recolectado
- Piso de PHP 8.3: **module-catalog-search** 2.2.0, **module-checkout** 3.12.0, **module-customer**
  2.4.0, **module-downloadable** 2.2.0, **module-gift-message** 2.2.0, **module-instant-purchase**
  2.2.0, **module-inventory-stock-visualizer** 1.2.0, **module-modern-frontend-twig** 2.7.0,
  **module-multishipping** 2.1.0, **module-persistent** 2.1.0, **module-product-alert** 2.1.0,
  **module-review** 2.3.0, **module-sales** 2.4.0, **module-search** 1.3.0, **module-send-friend**
  2.2.0, **module-vault** 2.3.0, **module-wishlist** 2.3.0

---

## Agosto 2026 { #2026-08 }

### Checkout servido desde la Full Page Cache

El checkout pasa a ser un shell público cacheable con la mitad privada entregada por customer-data,
en lugar de una página no cacheable. El shell se activa por tienda.

- **module-checkout** 3.3.0 — servir el checkout desde la FPC; sembrar la isla desde la sección de
  customer-data; rellenar el formulario de envío desde la libreta de direcciones; mostrar las opciones
  seleccionadas bajo cada línea del resumen
- **module-modern-frontend** 2.14.0 — flag del shell de checkout cacheable
- **module-modern-frontend** 2.15.0 — el section store informa si su snapshot cacheado está desincronizado
- **theme-default** 3.8.0 — inyectar en línea solo la mitad cacheable de la config del checkout;
  etiquetar el selector de direcciones guardadas

### Fragmentos cacheables de listado

La navegación por capas, el orden y la paginación se sirven como fragmentos cacheables, de modo que un
listado filtrado ya no cuesta el render completo de una página sin caché.

- **module-search** 1.0.0 — módulo nuevo: filtros, orden y paginación como fragmentos cacheables
- **module-storefront** 3.7.0 — anunciar la navegación del listado para que los enhancers se
  re-enganchen tras un swap

### Panel de funcionalidades para tiendas de demo

- **module-showcase** 1.0.0 – 1.2.0 — módulo nuevo: alternar funcionalidades de MageObsidian por
  visitante, ofrecer el checkout cacheable como interruptor y reportar el conjunto activo como
  atributos de New Relic

### Verificación del deploy estático

**La verificación del deploy estático ya no da falsas alarmas.** El chequeo añadido en
`module-modern-frontend` 2.15.0 leía el valor por defecto de `--language`, `all`, como si fuera un
locale, así que buscaba en un `pub/static/<área>/<tema>/all/` que Magento nunca escribe y reportaba
un deploy impecable como enteramente ausente. Ahora resuelve el centinela a través del propio
`LocaleResolver` de Magento, respeta `--theme`, `--exclude-theme` y `--exclude-language`, y
**advierte en vez de abortar** el deploy.

- **module-modern-frontend** 2.15.1 — resolver `--language all` con `LocaleResolver`; advertir en
  vez de abortar

---

## Julio 2026 { #2026-07 }

El mes en que la línea del storefront pasó a `3.x` (21 de julio) y luego creció una capa reactiva
encima.

### UI optimista y un bus de eventos tipado del storefront

Toda mutación de carrito, wishlist, comparación, catálogo y checkout despacha ahora eventos
`before` / `after` / `failed` sobre un bus tipado. La UI proyecta el cambio antes de que el servidor
lo confirme y se asienta cuando lo hace: los contadores destellan, los toasts se disparan y las
operaciones en vuelo se registran de forma centralizada.

- **js-package-utils** 2.5.0 — gestor de eventos estilo observer
- **js-package-utils** 2.6.0 — eventos del storefront tipados con despacho sticky y espejo en el DOM;
  `patchSection` para proyectar un cambio por delante del servidor; seguimiento de operaciones en
  vuelo; config de UI optimista en runtime
- **module-modern-frontend** 2.11.0 — singleton del gestor de eventos del storefront
- **module-modern-frontend** 2.12.0 — eventos de ciclo de vida de islas y parcheo de secciones cableados
  al runtime; flag de UI optimista
- **module-storefront** 3.2.0 – 3.4.0 — eventos alrededor de cada mutación del carrito; eventos de
  carrito, wishlist y comparación; eventos de búsqueda desde el autocompletado; toasts dirigidos por el
  evento de notificación; capa de feedback optimista para botones, avisos y destellos de valor
- **module-checkout** 3.1.0 — página de carrito dirigida por el bus de eventos; eventos de mutación y
  cambio de paso del checkout; ítems del minicarrito eliminados de forma optimista
- **module-catalog** 3.1.0, 3.3.0 — eventos de variantes, bundles, galería y opciones de producto

### Islas que hidratan sobre marcado renderizado en servidor

Las islas ya no aparecen de golpe sobre un contenedor vacío: el servidor renderiza el marcado que la
isla adopta, y las builds de desarrollo reportan la deriva de hidratación cuando ambos discrepan.

- **module-modern-frontend** 2.9.0 — placeholder de servidor dentro de los marcadores de isla
- **module-modern-frontend** 2.11.0 — islas renderizadas con marcado hidratable; deriva de hidratación
  reportada en builds de desarrollo; el doctor señala islas eager que renderizan un contenedor vacío
- **js-package-utils** 2.5.0 — montar islas desde marcado de servidor y comparar para detectar deriva;
  CLI `island-ssr` para renderizar el marcado inicial de una isla
- **js-package-utils** 2.6.1 — marcar un marcador cuando su isla ha terminado de renderizar
- **module-modern-frontend-twig** 2.3.0 — marcado de islas y clases de iconos expuestos a las plantillas
- **theme-default** 3.2.0 — renderizar en servidor el marcado que adoptan las islas al hidratar

### Contenido personalizado dibujado antes del primer pintado

Los contadores de customer-data y el estado de sesión se pintan a partir de una declaración en
`di.xml`, antes del primer frame, de modo que la personalización ya no llega como un parpadeo visible.

- **module-modern-frontend** 2.12.1 — dibujar los contadores de customer-data antes del primer pintado
- **module-storefront** 3.4.3 — declarar los contadores de la cabecera
- **module-customer** 2.0.4 — declarar el flag de cuenta y condicionar el placeholder de inicio de sesión
- **theme-default** 3.4.5 — el runtime de pre-pintado toma el control del placeholder de inicio de sesión

### Tailwind para contenido CMS

Las clases escritas en páginas y bloques CMS eran invisibles para el build. Ahora el contenido se
exporta, se escanea y se compila bajo demanda, y se sirve como hoja de estilos delta tras una URL
estable y un ETag.

- **module-modern-frontend** 2.11.0 — compilar clases de Tailwind que el build nunca vio; exportar
  contenido para escanearlo; hoja delta desde una URL estable con ETag; exclusión por página o bloque;
  componente `Icon` e islas Vue colocables desde el contenido vía widget y directiva
- **module-modern-frontend-cli** 2.4.0 — comandos `cms:export` y `cms:jit`, cableados al doctor
- **js-package-utils** 2.5.0 — escanear el contenido CMS exportado en busca de clases de Tailwind y fijar
  la lista por tema

### View transitions entre documentos

- **module-storefront** 3.3.0, 3.4.0 — transiciones acotadas a los movimientos de catálogo; tarjetas de
  producto reordenadas con los nombres duplicados protegidos
- **module-catalog** 3.2.0, 3.3.0 — la imagen de la galería nombrada como destino del morph de la
  tarjeta; tarjetas clasificadas y el intercambio de galería suavizado
- **theme-default** 3.3.0, 3.4.0 — el chrome se mantiene quieto durante las transiciones; reglas movidas
  a una hoja de estilos, animando tarjetas y líneas del carrito

### Sistema de campos y primitivas de UI

- **module-storefront** 3.4.0 — componente de campo compartido con estados de requerido y error;
  primitivas de checkbox y slot; primitivas de botón, enlace y campo como componentes por capas

### Navegación

- **module-storefront** 2.1.0 — isla de navegación primaria priority+ con menú de desbordamiento
- **module-storefront** 2.2.0 — mega menú anidado con flyouts en escritorio y acordeón en móvil; marca y
  enlace de inicio configurables en el menú móvil
- **module-storefront** 3.1.0 — bloque de navegación con cache tags para fragmentos ESI; árbol de menú
  cacheado en `block_html` con TTL de 1 h; búsquedas de URL rewrite de categoría agrupadas en una consulta
- **module-catalog** 3.5.0 — navegación por capas como drawer en móvil
- **theme-default** 3.1.0, 3.4.0, 3.7.0 — bloques de navegación servidos como fragmentos ESI con TTL; la
  navegación primaria se corta con container queries en lugar de medir en cliente; filtros en drawer y
  barra de herramientas de dos filas en móvil

### Layout de checkout en una página

El checkout se distribuye en dos layouts tras un flag de configuración: el asistente por pasos o un
layout reactivo de una sola página.

- **module-checkout** 2.1.0 — layout reactivo de checkout en una página
- **module-modern-frontend** 2.8.0 — flag de configuración del modo de layout del checkout
- **module-checkout** 2.2.0 — configuración nativa del checkout respetada (agreements, login de invitado,
  tope del resumen, `display_billing_address_on`)

### Visualizador de stock MSI

- **module-inventory-stock-visualizer** 1.0.0 — módulo nuevo: panel de disponibilidad enrutado por tipo
  de producto, rediseñado alrededor de un raíl de fuentes segmentado, renderizado en servidor y omitido
  por completo para productos sin stock

### Motor Twig

- **module-modern-frontend-twig** 2.1.0 – 2.5.0 — marcado de placeholder reenviado a través de
  `render_vue`; alias de namespace y herencia de plantillas con `@parent`; `inline_view_file` para
  incrustar un view file literalmente; `script()` para cargar un enhancer de Vite sin un bloque de render

### Diagnósticos

- **module-modern-frontend** 2.10.0, 2.11.0 — detectar una clave de page cache que ignora
  `X-Magento-Vary`; reportar el binario de Tailwind y las clases CMS sin resolver
- **module-modern-frontend-cli** 2.3.0, 2.4.0 — reporte del manejo de vary en la page cache; plantillas
  escaneadas en busca de islas eager sin hidratación

### Speculation rules

- **module-storefront** 3.6.0 — speculation rules configurables

---

## Junio 2026 — la línea 2.0.0 { #2026-06 }

Todo el stack se etiquetó a la vez el 22 de junio: motor core, CLI, harness de Vite, motor JS, el motor
Twig opcional, `module-storefront`, ambos temas y los módulos de compatibilidad para catálogo, búsqueda,
checkout, cliente, ventas, wishlist, reseñas, vault, gift message, downloadable, multishipping,
persistent, product alert, send-friend e instant purchase.

### Islas Vue

- **module-modern-frontend** 2.0.0 — componentes Vue renderizados como islas de hidratación diferida;
  interfaces `@api`, detección de deriva y endurecimiento
- **js-package-utils** 2.0.0 — runtime de hidratación de islas
- **module-modern-frontend** 2.1.0 — hidratación de las secciones de customer-data diferida al idle,
  fuera de la ruta crítica
- **module-modern-frontend** 2.2.0, 2.2.1 — `modulepreload` del grafo de dependencias de las islas eager,
  emitido en línea por marcador para cubrir también las islas al final del body

### Critical CSS

- **js-package-utils** 2.4.0 — extractor de critical CSS con Beasties
- **module-modern-frontend** 2.4.0 — ruta de critical CSS y exclusión de minificado HTML por tema
- **module-modern-frontend-cli** 2.2.0 — comando de generación de critical CSS
- **theme-base** 2.1.0 — hoja de estilos diferida por página cuando existe critical CSS

### Motor Twig opcional

- **module-modern-frontend-twig** 2.0.0 — motor `.twig` coexistiendo con `.phtml`, con filtros de i18n,
  montaje eager y html-safe, un helper `image` responsive, un helper `json_ld` y extensiones registradas
  por DI

### SEO, imágenes e i18n

- **module-modern-frontend** 2.0.0 — JSON-LD de schema.org (Organization, WebSite, BreadcrumbList,
  Product); helper de render de imágenes orientado a CWV
- **js-package-utils** 2.2.0 — fachada de i18n para enhancers ESM planos
- **module-modern-frontend-cli** 2.0.2 — frases `$t` recolectadas desde fuentes `.ts` y `.js`
- **theme-base** 2.0.1 — diccionario de traducciones precargado fuera de la cadena de arranque de las islas

### Flujo de desarrollo

- **module-modern-frontend** 2.0.0, 2.3.0 — núcleo de diagnósticos de desarrollo y guarda del dev server
  en cliente; ciclo de vida del dev server de Vite gestionado por grupo de procesos; snippet de proxy de
  nginx derivado de la configuración; `DevWorkflow` y `ThemeSelector`
- **module-modern-frontend-cli** 2.0.0, 2.1.0 — el doctor reporta archivos de configuración ignorados;
  scaffolding de `jsconfig` y `.gitignore` para los tipos del editor; `--up`/`--down` de una sola pasada
  y selector de tema para `frontend:dev`
- **js-package-utils** 2.3.0 — selector de tema cuando `--dev-server` omite `--theme`
