# Registro de cambios

MageObsidian se distribuye como un conjunto de paquetes versionados de forma independiente, pero sus
funcionalidades rara vez viven en uno solo: un checkout cacheable es un flag del core, un módulo de
compatibilidad y una plantilla del tema aterrizando juntos. Esta página sigue al **stack**, para que
puedas leer qué cambió sin tener que recomponerlo a partir de una docena de feeds de releases.

Cada entrada nombra los paquetes y versiones que la traen. Para el historial a nivel de commit de un
paquete concreto, consulta sus releases en [GitHub](https://github.com/mage-obsidian).

!!! note "Dónde empieza esto"
    Todo el stack se etiquetó como `2.0.0` a la vez el **22 de junio de 2026**, y ahí empieza este
    registro. Lo anterior queda fuera de la línea actual.

---

## Septiembre 2026

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
- **module-storefront** 3.22.0, **module-showcase** 1.5.0 — incluir el diccionario `en_US` recolectado
- Piso de PHP 8.3: **module-catalog-search** 2.2.0, **module-checkout** 3.12.0, **module-customer**
  2.4.0, **module-downloadable** 2.2.0, **module-gift-message** 2.2.0, **module-instant-purchase**
  2.2.0, **module-inventory-stock-visualizer** 1.2.0, **module-modern-frontend-twig** 2.7.0,
  **module-multishipping** 2.1.0, **module-persistent** 2.1.0, **module-product-alert** 2.1.0,
  **module-review** 2.3.0, **module-sales** 2.4.0, **module-search** 1.3.0, **module-send-friend**
  2.2.0, **module-vault** 2.3.0, **module-wishlist** 2.3.0

---

## Agosto 2026

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

## Julio 2026

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

## Junio 2026 — la línea 2.0.0

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
