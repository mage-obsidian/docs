# Development Workflow

**{{ config.site_name }}** drives the whole frontend dev loop from `bin/magento`. You never hand-edit the Vite `.env`: it is **derived from your Magento configuration** (Stores → Configuration → MageObsidian), which is the single source of truth for the dev server host, port, and HMR settings. The commands below sync it for you.

---

## The Loop at a Glance

```bash
# once: put Magento in developer mode and turn on HMR
bin/magento deploy:mode:set developer
bin/magento mage-obsidian:frontend:hmr --enable

# once: wire nginx to the Vite dev server (paste the snippet into your server block)
bin/magento mage-obsidian:frontend:dev --print-nginx

# day to day: start the dev server for the theme you're working on
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme

# ...edit .vue / css / templates with live HMR...

bin/magento mage-obsidian:frontend:dev --status   # is it running and reachable?
bin/magento mage-obsidian:frontend:dev --stop     # stop when done
```

---

## Commands

### `mage-obsidian:frontend:dev`

Manages the Vite `.env` and the local dev server.

| Option | What it does |
|---|---|
| `--sync-env` | Write `vite/.env` from the current Magento config. |
| `--show` | Print the env vars derived from config without writing the file. |
| `--start --theme=Vendor/theme` | Sync the env, then start the Vite dev server (HMR). |
| `--start --no-watch --theme=Vendor/theme` | Build the theme once to disk instead of running the server (no HMR, no daemon). |
| `--stop` | Stop the dev server started by `--start`. |
| `--status` | Report whether the dev server process is running and reachable. |
| `--print-nginx` | Print the nginx proxy snippet (host/port from config) to paste into your server block. |

`--start` requires `--theme`. Starting always syncs the `.env` first, so you rarely call `--sync-env` directly — it's there for inspection or scripting. The command runs the dev server **where `bin/magento` runs**; running it in a different container than the CLI is your environment's concern.

### `mage-obsidian:frontend:hmr`

HMR is a Magento config flag, ignored in production mode.

```bash
bin/magento mage-obsidian:frontend:hmr --enable
bin/magento mage-obsidian:frontend:hmr --disable
bin/magento mage-obsidian:frontend:hmr --show
```

See [HMR](../components/modules/0110-hmr-configuration.md) for details and the nginx proxy.

### `mage-obsidian:frontend:doctor`

One-shot diagnosis of the dev environment — app mode, the contract (and drift), the HMR flag, dev-server reachability, and the required env vars. Each check is reported ok / warn / error with a hint.

```bash
bin/magento mage-obsidian:frontend:doctor
```

Run it first whenever something doesn't behave: it usually pinpoints the cause (wrong mode, HMR off, unreachable dev server, missing env var, stale contract).

---

## Building to Disk

To produce the real built assets without the dev server (local inspection or CI), use `--no-watch`, or the lower-level engine bin. See [Building Static Assets](../components/modules/0120-vite-build.md).

```bash
bin/magento mage-obsidian:frontend:dev --start --no-watch --theme=Vendor/theme
```

---

## Next Steps

- [Scaffolding](scaffolding.md) — generate modules, themes, and components.
- [HMR](../components/modules/0110-hmr-configuration.md) — the live-reload details and nginx.
- [Building Static Assets](../components/modules/0120-vite-build.md) — production deploy.
