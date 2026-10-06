---
description: "Cada comando bin/magento mage-obsidian con sus opciones y ejemplos."
---
# Comandos CLI

Todos los comandos se ejecutan con `bin/magento` desde la raíz de Magento. Además de las opciones listadas, aceptan las opciones globales de Symfony Console (`--help`, `--quiet`, `--verbose`, `--no-interaction`, `--ansi`).

## `mage-obsidian:cms:export` { data-toc-label="cms:export" }

Exporta el contenido de las páginas y bloques CMS para que Tailwind pueda leer las clases escritas en él.

```bash
bin/magento mage-obsidian:cms:export
```

Sin opciones.

## `mage-obsidian:cms:jit` { data-toc-label="cms:jit" }

Reconstruye el CSS de las clases de Tailwind escritas en contenido CMS después de la última compilación.

```bash
bin/magento mage-obsidian:cms:jit [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--show` | Informa el estado actual sin reconstruir. | — |

## `mage-obsidian:frontend:config` { data-toc-label="frontend:config" }

Gestiona la configuración de los módulos y temas activos compatibles con el frontend moderno.

```bash
bin/magento mage-obsidian:frontend:config [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--generate` | Genera o actualiza el archivo de configuración de los módulos y temas compatibles activos. | — |
| `--show` | Muestra la configuración actual de los módulos y temas compatibles. | — |
| `--modules` | Muestra solo la configuración de los módulos (requiere `--show`). | — |
| `--themes` | Muestra solo la configuración de los temas (requiere `--show`). | — |

## `mage-obsidian:frontend:critical-css` { data-toc-label="frontend:critical-css" }

Extrae el CSS crítico above-the-fold de un handle de layout en el directorio `web/critical` del tema.

```bash
bin/magento mage-obsidian:frontend:critical-css [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--handle=HANDLE` | Handle de layout para el que se genera el CSS crítico. | `cms_index_index` |
| `--url=URL` | URL a renderizar; repítela una vez por cada forma de página que sirve el handle (por defecto: la URL base segura de la tienda). Se puede repetir. | — |
| `--min-coverage=MIN-COVERAGE` | Falla cuando el CSS crítico cubre menos de esta proporción (0..1) de las clases con estilo. | `0` |
| `--store=STORE` | Código o id de la tienda a emular (por defecto: la vista de tienda predeterminada). | — |
| `--insecure` | Omite la verificación TLS (certificados de desarrollo autofirmados). | — |
| `--resolve=RESOLVE` | Entrada `--resolve` de curl con formato `host:port:ip` (desarrollo). | — |
| `--cookie=COOKIE` | Cabecera Cookie para handles que necesitan sesión (un checkout necesita un carrito con productos). | — |
| `--bin=BIN` | Ruta al binario node de critical-css. | — |
| `--node=NODE` | Binario de node. | `node` |

## `mage-obsidian:frontend:dev` { data-toc-label="frontend:dev" }

Gestiona el flujo de desarrollo de MageObsidian (`--up`/`--down` de un solo paso, `.env` de Vite, servidor de desarrollo).

```bash
bin/magento mage-obsidian:frontend:dev [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--up` | Un solo paso: modo developer + HMR activado + sincroniza `.env` + flush + inicia el servidor de desarrollo (comprueba primero si ya corre). | — |
| `--down` | Un solo paso: detiene el servidor de desarrollo + desactiva HMR + flush + reconstruye los assets en disco. | — |
| `--no-start` | Con `--up`: solo fija el estado, no inicia el servidor de desarrollo (lo ejecuta el entorno). | — |
| `--production` | Con `--down`: además cambia Magento a modo production (`di:compile` + static deploy). | — |
| `--sync-env` | Escribe el `.env` del harness de Vite (`vite/.env`) a partir de la configuración actual de Magento. | — |
| `--show` | Imprime las variables de entorno derivadas de la configuración de Magento sin escribir ningún archivo. | — |
| `--start` | Inicia el servidor de desarrollo local de Vite. Elige un tema de forma interactiva si se omite `--theme`. | — |
| `--stop` | Detiene el servidor de desarrollo local de Vite iniciado con `--start`. | — |
| `--status` | Informa si el proceso del servidor de desarrollo local está en ejecución y es accesible. | — |
| `--print-nginx` | Imprime el fragmento de proxy de nginx (derivado de la configuración) para pegarlo en tu bloque server. | — |
| `--theme=THEME` | Tema a servir o compilar (por ejemplo `Vendor/theme`). Se pregunta cuando se omite en una terminal. | — |
| `--watch` | Con `--start`: ejecuta el servidor de desarrollo con HMR. | Predeterminado con `--start` |
| `--no-watch` | Con `--start`: compila el tema una vez en disco en lugar de ejecutar el servidor de desarrollo. | — |

## `mage-obsidian:frontend:doctor` { data-toc-label="frontend:doctor" }

Diagnostica el entorno de desarrollo de MageObsidian (HMR, servidor de Vite, contrato, configuración).

```bash
bin/magento mage-obsidian:frontend:doctor
```

Sin opciones.

## `mage-obsidian:frontend:hmr` { data-toc-label="frontend:hmr" }

Gestiona la configuración de Hot Module Replacement (HMR) para los módulos y temas compatibles con el frontend moderno.

```bash
bin/magento mage-obsidian:frontend:hmr [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--show` | Muestra el estado actual de HMR. | — |
| `--enable` | Activa HMR. | — |
| `--disable` | Desactiva HMR. | — |

## `mage-obsidian:generate:component` { data-toc-label="generate:component" }

Genera un componente Vue integrado con el frontend de MageObsidian.

```bash
bin/magento mage-obsidian:generate:component [options] [--] <name>
```

| Argumento | Descripción |
|---|---|
| `name` | Nombre del componente o ruta bajo `components/` (por ejemplo `Button` o `elements/Button`). |

| Opción | Descripción | Por defecto |
|---|---|---|
| `--module=MODULE` | Módulo de destino (`Vendor_Module`). | — |
| `--theme=THEME` | Tema de destino (`Vendor/theme`). | — |
| `--wire` | Genera además un stub phtml que renderiza el componente. | — |
| `-f, --force` | Sobrescribe los archivos si ya existen. | — |

## `mage-obsidian:generate:module` { data-toc-label="generate:module" }

Genera un módulo nuevo en `app/code` ya preparado para el frontend de MageObsidian.

```bash
bin/magento mage-obsidian:generate:module [options] [--] <name>
```

| Argumento | Descripción |
|---|---|
| `name` | Nombre del módulo con formato `Vendor_Module`. |

| Opción | Descripción | Por defecto |
|---|---|---|
| `-f, --force` | Sobrescribe los archivos si ya existen. | — |

## `mage-obsidian:generate:theme` { data-toc-label="generate:theme" }

Genera un tema de frontend nuevo en `app/design` ya preparado para MageObsidian.

```bash
bin/magento mage-obsidian:generate:theme [options] [--] <path>
```

| Argumento | Descripción |
|---|---|
| `path` | Código del tema con formato `Vendor/theme` (por ejemplo `Acme/aurora`). |

| Opción | Descripción | Por defecto |
|---|---|---|
| `--parent=PARENT` | Tema padre (por ejemplo `Magento/blank`). | — |
| `--title=TITLE` | Título legible del tema. | — |
| `-f, --force` | Sobrescribe los archivos si ya existen. | — |

## `mage-obsidian:i18n:collect` { data-toc-label="i18n:collect" }

Recopila las frases traducibles de `.vue`, `.ts`, `.js` y `.twig` en el CSV i18n de cada componente.

```bash
bin/magento mage-obsidian:i18n:collect [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `--locale=LOCALE` | Locale del diccionario CSV a escribir (por ejemplo `en_US`). | `en_US` |

## `mage-obsidian:twig:namespaces` { data-toc-label="twig:namespaces" }

Muestra los namespaces de plantillas Twig (`@alias/path.twig`) y sus módulos.

```bash
bin/magento mage-obsidian:twig:namespaces [options]
```

| Opción | Descripción | Por defecto |
|---|---|---|
| `-f, --filter=FILTER` | Muestra solo los alias o módulos que contengan esta cadena. | — |
