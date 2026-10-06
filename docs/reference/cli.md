---
description: "Every bin/magento mage-obsidian command with its options and examples."
---
# CLI commands

Every command runs through `bin/magento` from the Magento root. Besides the options listed, they accept the global Symfony Console options (`--help`, `--quiet`, `--verbose`, `--no-interaction`, `--ansi`).

## `mage-obsidian:cms:export` { data-toc-label="cms:export" }

Export CMS page and block content so Tailwind can scan the classes written in it.

```bash
bin/magento mage-obsidian:cms:export
```

No options.

## `mage-obsidian:cms:jit` { data-toc-label="cms:jit" }

Rebuild the CSS for Tailwind classes written in CMS content after the last build.

```bash
bin/magento mage-obsidian:cms:jit [options]
```

| Option | Description | Default |
|---|---|---|
| `--show` | Report the current state without rebuilding. | — |

## `mage-obsidian:frontend:config` { data-toc-label="frontend:config" }

Manage configuration of active modules and themes compatible with the modern frontend.

```bash
bin/magento mage-obsidian:frontend:config [options]
```

| Option | Description | Default |
|---|---|---|
| `--generate` | Generate or update the configuration file for active compatible modules and themes. | — |
| `--show` | Display the current configuration of compatible modules and themes. | — |
| `--modules` | Display only the modules configuration (requires `--show`). | — |
| `--themes` | Display only the themes configuration (requires `--show`). | — |

## `mage-obsidian:frontend:critical-css` { data-toc-label="frontend:critical-css" }

Extract above-the-fold critical CSS for a layout handle into the theme's `web/critical` dir.

```bash
bin/magento mage-obsidian:frontend:critical-css [options]
```

| Option | Description | Default |
|---|---|---|
| `--handle=HANDLE` | Layout handle the critical CSS is for. | `cms_index_index` |
| `--url=URL` | URL to render; repeat it once per page shape the handle serves (default: store secure base URL). Can be repeated. | — |
| `--min-coverage=MIN-COVERAGE` | Fail when the critical CSS covers less than this share (0..1) of the styled classes. | `0` |
| `--store=STORE` | Store code/id to emulate (default: default store view). | — |
| `--insecure` | Skip TLS verification (self-signed dev certs). | — |
| `--resolve=RESOLVE` | curl `--resolve` entry `host:port:ip` (dev). | — |
| `--cookie=COOKIE` | Cookie header for handles that need a session (a checkout needs a cart with items). | — |
| `--bin=BIN` | Path to the node critical-css bin. | — |
| `--node=NODE` | node binary. | `node` |

## `mage-obsidian:frontend:dev` { data-toc-label="frontend:dev" }

Manage the MageObsidian dev workflow (one-shot `--up`/`--down`, Vite `.env`, dev server).

```bash
bin/magento mage-obsidian:frontend:dev [options]
```

| Option | Description | Default |
|---|---|---|
| `--up` | One shot: developer mode + HMR on + sync `.env` + flush + start the dev server (probe-first). | — |
| `--down` | One shot: stop the dev server + HMR off + flush + rebuild assets to disk. | — |
| `--no-start` | With `--up`: set state only, do not start the dev server (the environment runs it). | — |
| `--production` | With `--down`: also switch Magento to production mode (`di:compile` + static deploy). | — |
| `--sync-env` | Write the Vite harness `.env` (`vite/.env`) from the current Magento config. | — |
| `--show` | Print the env vars derived from Magento config without writing any file. | — |
| `--start` | Start the local Vite dev server. Picks a theme interactively if `--theme` is omitted. | — |
| `--stop` | Stop the local Vite dev server started by `--start`. | — |
| `--status` | Report whether the local dev server process is running and reachable. | — |
| `--print-nginx` | Print the nginx proxy snippet (derived from config) to paste into your server block. | — |
| `--theme=THEME` | Theme to serve/build (e.g. `Vendor/theme`). Prompted when omitted on a terminal. | — |
| `--watch` | With `--start`: run the HMR dev server. | Default for `--start` |
| `--no-watch` | With `--start`: build the theme once to disk instead of running the dev server. | — |

## `mage-obsidian:frontend:doctor` { data-toc-label="frontend:doctor" }

Diagnose the MageObsidian dev environment (HMR, Vite dev server, contract, config).

```bash
bin/magento mage-obsidian:frontend:doctor
```

No options.

## `mage-obsidian:frontend:hmr` { data-toc-label="frontend:hmr" }

Manage Hot Module Replacement (HMR) configuration for modules and themes compatible with the modern frontend.

```bash
bin/magento mage-obsidian:frontend:hmr [options]
```

| Option | Description | Default |
|---|---|---|
| `--show` | Show the current status of HMR. | — |
| `--enable` | Enable HMR. | — |
| `--disable` | Disable HMR. | — |

## `mage-obsidian:generate:component` { data-toc-label="generate:component" }

Generate a Vue component wired for the MageObsidian frontend.

```bash
bin/magento mage-obsidian:generate:component [options] [--] <name>
```

| Argument | Description |
|---|---|
| `name` | Component name or path under `components/` (for example `Button` or `elements/Button`). |

| Option | Description | Default |
|---|---|---|
| `--module=MODULE` | Target module (`Vendor_Module`). | — |
| `--theme=THEME` | Target theme (`Vendor/theme`). | — |
| `--wire` | Also generate a phtml stub that renders the component. | — |
| `-f, --force` | Overwrite files if they already exist. | — |

## `mage-obsidian:generate:module` { data-toc-label="generate:module" }

Generate a new module under `app/code` pre-wired for the MageObsidian frontend.

```bash
bin/magento mage-obsidian:generate:module [options] [--] <name>
```

| Argument | Description |
|---|---|
| `name` | Module name in `Vendor_Module` form. |

| Option | Description | Default |
|---|---|---|
| `-f, --force` | Overwrite files if they already exist. | — |

## `mage-obsidian:generate:theme` { data-toc-label="generate:theme" }

Generate a new frontend theme under `app/design` pre-wired for MageObsidian.

```bash
bin/magento mage-obsidian:generate:theme [options] [--] <path>
```

| Argument | Description |
|---|---|
| `path` | Theme code in `Vendor/theme` form (for example `Acme/aurora`). |

| Option | Description | Default |
|---|---|---|
| `--parent=PARENT` | Parent theme (for example `Magento/blank`). | — |
| `--title=TITLE` | Human-readable theme title. | — |
| `-f, --force` | Overwrite files if they already exist. | — |

## `mage-obsidian:i18n:collect` { data-toc-label="i18n:collect" }

Collect translatable phrases from `.vue`/`.ts`/`.js` and `.twig` into each component i18n CSV.

```bash
bin/magento mage-obsidian:i18n:collect [options]
```

| Option | Description | Default |
|---|---|---|
| `--locale=LOCALE` | Locale of the CSV dictionary to write (for example `en_US`). | `en_US` |

## `mage-obsidian:twig:namespaces` { data-toc-label="twig:namespaces" }

Show the Twig template namespaces (`@alias/path.twig`) and their modules.

```bash
bin/magento mage-obsidian:twig:namespaces [options]
```

| Option | Description | Default |
|---|---|---|
| `-f, --filter=FILTER` | Only show aliases or modules containing this string. | — |
