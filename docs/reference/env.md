---
description: "The environment variables the Vite harness and build engine read, with their purpose and default."
---
# Environment variables

The build engine reads these variables from the environment or from `vite/.env` (see `vite/.env.sample`). `bin/magento mage-obsidian:frontend:dev --sync-env` writes `vite/.env` from the Magento configuration.

| Variable | Used by | Purpose | Default |
|---|---|---|---|
| `CURRENT_THEME` | `mage-obsidian:build-themes`, `vite.config.js` | Theme the Vite build or dev server works on (`Vendor/theme`). `mage-obsidian:build-themes` sets it for each theme it builds, so you do not set it by hand. | Set per theme by `build-themes` |
| `MAGENTO_HOST` | `vite.config.js` | Fixed public host for the HMR websocket. Leave it empty on multi-website setups with a shared theme so the Vite client derives the host from `window.location`. Written by `frontend:dev --sync-env` from `mage_obsidian/dev_server/public_host`. | `magento.test` (`.env.sample`) |
| `MAGE_OBSIDIAN_BUILD_CONCURRENCY` | `mage-obsidian:build-themes` | Maximum number of themes built in parallel. Must be an integer of 1 or more; any other value falls back to the default. The result is capped at the number of themes. | CPU cores minus 1 |
| `MAGE_OBSIDIAN_MAGENTO_ROOT` | `js-package-utils` (`config/default.ts`) | Explicit Magento root, used to locate `app/etc/mage_obsidian_frontend_modules.json`. Set it when the engine does not run from the `vite/` directory one level below the Magento root. | Parent of the working directory |
| `MAGE_OBSIDIAN_TYPES_PATH_MAP` | `js-package-utils` (`core/generateJsconfig.ts`) | Optional. Rewrites the absolute paths in the generated theme `jsconfig.json` so go-to-definition and autocomplete land where your editor opens the files. Only needed when the build runs on a different filesystem or mount than your editor (for example a container). Format: `from=>to`, comma-separated for several mounts; the longest matching `from` wins. | Unset |
| `VITE_HMR_PATH` | `vite.config.js` | Path of the HMR websocket. Also reported by `frontend:dev --show` and checked by `frontend:doctor`. Maps from `mage_obsidian/dev_server/hmr_path`. | `/__vite_ping` |
| `VITE_SERVER_ALLOWED_HOSTS` | `vite.config.js` | Comma-separated list of the hosts allowed to reach the dev server. Every storefront host that serves the theme in development must be listed, or Vite answers its asset requests with 403. Maps from `mage_obsidian/dev_server/allowed_hosts`. | `magento.test,localhost` (`.env.sample`) |
| `VITE_SERVER_HOST` | `mage-obsidian:build-themes --dev-server`, `vite.config.js` | Host the dev server binds to. Required for the dev server; it is also added to the allowed hosts. Maps from `mage_obsidian/dev_server/host`. | `phpfpm` (`.env.sample`) |
| `VITE_SERVER_PORT` | `mage-obsidian:build-themes --dev-server`, `vite.config.js` | Port the dev server listens on. Required for the dev server. Maps from `mage_obsidian/dev_server/port`. | `5173` |
| `VITE_SERVER_SECURE` | `vite.config.js` | Use `wss` instead of `ws` for the HMR socket. Accepts `true`, `1`, `yes` or `on` (case-insensitive); anything else means `ws`. Maps from `mage_obsidian/dev_server/secure`. | `true` (`.env.sample`) |
