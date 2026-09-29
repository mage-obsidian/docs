# Adobe Commerce

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
- **Adobe Commerce Cloud.** Su build corre sin base de datos, y la generación del contrato del
  frontend todavía no lo soporta.
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
