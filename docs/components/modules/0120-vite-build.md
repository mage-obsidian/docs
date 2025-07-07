# Building Static Assets

**MageObsidian** uses Vite to process and bundle frontend assets (CSS, JavaScript, Vue components). This page covers building those assets to disk — for local inspection without HMR, for CI, and for production deployment.

---

## Build a Theme to Disk (no HMR)

To build a single theme once to disk — the same artifacts a browser would get, but written to `web/generated` instead of served by the dev server — use the dev command with `--no-watch`:

```bash
bin/magento mage-obsidian:frontend:dev --start --no-watch --theme=Vendor/theme
```

This is the inverse of `--start` (HMR): no daemon, no watching — it runs one build and exits. Useful to inspect the real output or to reproduce a CI build locally.

### The underlying engine bin

`frontend:dev` wraps the build engine's own bin, which you can also run directly from the `vite/` harness (this is what CI uses):

```bash
# from the component's vite/ directory
mage-obsidian:build-themes                  # build every compatible theme
mage-obsidian:build-themes --theme Vendor/theme   # build one
```

`frontend:dev` is the Magento-side entry point (it derives the Vite `.env` from your config first); `build-themes` is the lower-level engine command. Either produces the same output.

---

## Production Deployment

For production you do **not** run a separate build step. MageObsidian hooks into Magento's standard static-content deploy: its deploy plugins exclude modern themes from the legacy Less/RequireJS pipeline and produce/inject the Vite output as part of the normal command:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

The Vite-generated assets land in the deployed static content alongside everything else. Vite handles minification, tree-shaking, and asset hashing for cache-busting automatically.

> **Compatible themes only.** Only themes that ship `etc/mage_obsidian_compatibility.xml` (and have been picked up by `mage-obsidian:frontend:config --generate`) go through the Vite pipeline. Themes without it follow Magento's native deploy untouched.

---

## Benefits

- **Optimized output** — minified, tree-shaken, hashed assets ready for production.
- **Native integration** — production builds happen inside `setup:static-content:deploy`; no extra step in your deploy pipeline.
- **Coexistence** — legacy themes keep using Magento's native static deploy; only modern themes use Vite.

---

See [Development Workflow](../../getting-started/development.md) for the HMR dev server and the full command set, and [HMR](0110-hmr-configuration.md) for live reloading during development.
