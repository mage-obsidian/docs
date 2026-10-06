---
description: "Qué cambia al instalar MageObsidian en Adobe Commerce 2.4.9: claves de Composer, paquetes que no aplican y problemas conocidos."
---
# Adobe Commerce

{{ verified('adobe-commerce') }}

**{{ config.extra.components_name }}** se instala y funciona sobre **Adobe Commerce 2.4.9** con
los mismos paquetes que en Magento Open Source. Esta página cubre lo que cambia: las claves de
Composer, los paquetes que no aplican y los problemas que te puedes encontrar en el camino.

## Qué significa "compatible" aquí

Los paquetes publicados se instalaron sobre Adobe Commerce 2.4.9 (PHP 8.5, modo `default`) y se
recorrió la tienda completa en un navegador: home, búsqueda, categoría, ficha de producto,
carrito, un checkout de invitado hasta confirmar el pedido, registro, la cuenta del cliente,
cierre de sesión e inicio de sesión. No apareció ningún error de consola, de red ni en los logs
del servidor, y el pedido quedó registrado con los totales correctos.

Lo que eso **no** cubre:

- **Las funciones de storefront exclusivas de Commerce** (gift cards, store credit, puntos de
  recompensa, gift registry, pedido por SKU, invitaciones y el resto) todavía no tienen
  storefront de MageObsidian. Corre `bin/magento mage-obsidian:frontend:doctor` para ver cuáles
  tiene habilitadas tu tienda.
- **Adobe Commerce Cloud** no se probó en un proyecto real. El build sin base de datos está
  soportado y probado ([siguiente sección](#build-sin-base-de-datos)); falta verificar que
  ece-tools conserve el contrato entre el build y el deploy, que Node.js esté en el `PATH` de la
  imagen de build y la memoria del contenedor de build.
- **Pasarelas de pago.** Solo se probó Check / Money order.

## Requisitos

- **Adobe Commerce 2.4.7 o posterior.** El paquete core requiere Magento 2.4.7.
- **PHP 8.3 o posterior.** Todos los módulos Magento de MageObsidian declaran `"php": ">=8.3"`.
- **Node.js 22.13 o posterior** y **pnpm 11**, la versión que fija el harness de Vite.
- **Claves de `repo.magento.com` con acceso a Commerce**, en el `auth.json` del proyecto.
  MageObsidian viene de Packagist y no necesita claves.

## Instalación

```bash
composer require mage-obsidian/component-modern-frontend mage-obsidian/theme-default
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
pnpm --prefix vite install --frozen-lockfile
```

Asigna el tema en **Content → Design → Configuration** (**MageObsidian — Default
(Obsidian)**) y después construye y publica los assets:

```bash
bin/magento setup:static-content:deploy -f en_US
bin/magento cache:flush
```

`setup:static-content:deploy` corre el build de Vite de cada tema MageObsidian y comprueba que
su salida se haya publicado. Un tema sin build se informa en un aviso; define
`MAGE_OBSIDIAN_STRICT_DEPLOY=1` para que ese aviso haga fallar el deploy.

En modo production, corre `bin/magento setup:di:compile` antes del deploy estático, como en
cualquier tienda Magento.

## Desarrollo

El HMR viene **apagado por defecto**, así que una instalación nueva sirve los assets
construidos. Para trabajar con el dev server de Vite, sigue [Desarrollo](development.md):

```bash
bin/magento mage-obsidian:frontend:dev --up
```

## Build sin base de datos

Adobe Commerce Cloud, y cualquier pipeline que arma un artefacto y lo copia al servidor, corre
`setup:static-content:deploy` en una fase sin base de datos y en otra ruta raíz. MageObsidian lo
soporta:

- Commitea `app/etc/config.php` con todos los módulos y con las secciones `scopes` y `themes`:
  `bin/magento app:config:dump scopes themes`.
- La fase de build necesita Node.js 22.13 o posterior y pnpm, y el harness de Vite instalado con
  `pnpm --prefix vite install --frozen-lockfile`.
- `setup:static-content:deploy` regenera el contrato del frontend desde el filesystem antes de
  construir, así que nunca usa un contrato commiteado desde otra máquina. Las rutas dentro de la
  raíz de Magento se escriben relativas a ella, y el árbol construido se puede mover.

| Variable | Uso |
|---|---|
| `MAGE_OBSIDIAN_SKIP_VITE_BUILD=1` | Regenera el contrato pero salta el build de Vite, cuando un paso anterior ya construyó los temas. Úsala junto con `MAGE_OBSIDIAN_STRICT_DEPLOY=1`. |
| `MAGE_OBSIDIAN_STRICT_DEPLOY=1` | Hace fallar el deploy cuando un tema no tiene build de Vite, en vez de solo informarlo. |
| `MAGE_OBSIDIAN_BUILD_CONCURRENCY=<n>` | Temas construidos en paralelo. Por defecto, uno menos que la cantidad de CPU; bájalo si el contenedor de build se queda sin memoria. |

**Contenido CMS.** Sin base de datos el build no puede leer el contenido CMS, así que los temas se
construyen con una baseline de clases vacía y cada clase escrita en contenido CMS se genera en
runtime. Para que funcione hacen falta dos pasos:

1. Instala el CLI standalone de Tailwind en `bin/tailwindcss` durante el build, en la versión que
   usa el harness:

    ```bash
    V=$(node -p "require('./vite/node_modules/tailwindcss/package.json').version")
    curl -sL -o bin/tailwindcss "https://github.com/tailwindlabs/tailwindcss/releases/download/v$V/tailwindcss-linux-x64"
    chmod +x bin/tailwindcss
    ```

2. Corre `bin/magento mage-obsidian:cms:jit` en la primera fase con base de datos, antes de que la
   tienda reciba tráfico: `post_deploy` en Cloud, después de `setup:upgrade` en un pipeline propio.

La fila **CMS baseline** de `bin/magento mage-obsidian:frontend:doctor` informa la baseline de cada
tema.

**Critical CSS.** `mage-obsidian:frontend:critical-css` escribe en
`<tema>/web/critical/<handle>.css`, en las fuentes del tema. Genéralo en desarrollo y commitéalo
con el tema; el deploy lo publica como cualquier otro archivo estático.

Un `.magento.app.yaml` como este lo junta todo. Todavía no se probó en un proyecto Cloud real:

```yaml
hooks:
    build: |
        set -e
        composer install
        pnpm --prefix vite install --frozen-lockfile
        V=$(node -p "require('./vite/node_modules/tailwindcss/package.json').version")
        curl -sL -o bin/tailwindcss "https://github.com/tailwindlabs/tailwindcss/releases/download/v$V/tailwindcss-linux-x64"
        chmod +x bin/tailwindcss
        php ./vendor/bin/ece-tools run scenario/build/generate.xml
        php ./vendor/bin/ece-tools run scenario/build/transfer.xml
    deploy: |
        php ./vendor/bin/ece-tools run scenario/deploy.xml
    post_deploy: |
        php ./vendor/bin/ece-tools run scenario/post-deploy.xml
        php bin/magento mage-obsidian:cms:jit
```

## Paquetes que no aplican

La instalación estándar de arriba solo trae lo que necesita el tema. Hay dos paquetes de la
organización MageObsidian que no forman parte de ella y no deben ir en una tienda Adobe Commerce:

- **`mage-obsidian/module-inventory-stock-visualizer`** adapta un panel del fork de MSI
  `jeanmarcos/inventory`. Adobe Commerce no trae el módulo del que depende, así que Composer lo
  rechaza. Es lo esperado.
- **`mage-obsidian/module-showcase`** es el panel de funcionalidades de la tienda de demo.

## Solución de problemas

**Todos los assets dan 404 bajo `…/vite_generated/…` y ninguna isla monta.** El HMR está
encendido sin un dev server corriendo. Las versiones del core anteriores a 2.20.0 traían el HMR
encendido. Apágalo:

```bash
bin/magento mage-obsidian:frontend:hmr --disable
```

**`There are no commands defined in the "mage-obsidian" namespace`.** Busca en
`var/log/exception.log` la línea `Failed to load core Magento commands`. Magento descarta todos
los comandos de módulos cuando uno no se puede construir, y eso pasa cuando `generated/code`
tiene un interceptor de un constructor anterior. Regenera el código con
`bin/magento setup:di:compile`, o borra `generated/code` y corre `bin/magento cache:clean config`.

**`Cannot build Vite assets: "…" is not writable`.** El build de Vite escribe en `vite/` y en el
`web/generated/` de cada tema. Corre el deploy estático en una fase que pueda escribir en el árbol
de código; en Cloud, esa es la fase de build.

**`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` después de actualizar `component-modern-frontend`.**
Las versiones anteriores a 2.6.0 ubicaban el store de pnpm en otro lugar, y pnpm se niega a
reconstruir `vite/node_modules` sin terminal. Borra `vite/node_modules` una vez y vuelve a
instalar.

**`ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION`.** pnpm rechaza un paquete publicado hace menos de un
día. Espera, o exceptúa esa única versión durante la instalación:

```bash
pnpm_config_minimum_release_age_exclude='["mage-obsidian@3.1.0"]' pnpm --prefix vite install --frozen-lockfile
```

**Un invitado es enviado a iniciar sesión en vez de llegar al checkout.** El carrito tiene un
producto descargable y `catalog/downloadable/disable_guest_checkout` está activo, que es el
valor por defecto de Magento. Es el comportamiento nativo; pon esa opción en **No** para que los
invitados puedan comprar productos descargables.
