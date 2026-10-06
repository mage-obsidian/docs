# Building Static Assets

**MageObsidian** uses Vite to process and bundle frontend assets (CSS, JavaScript, Vue components). This page covers building those assets to disk — for local inspection without HMR, for CI, and for production deployment.

---

## Build a Theme to Disk (no HMR)

To build a single theme once to disk — the same artifacts a browser would get, but written to `web/generated` instead of served by the dev server — use the dev command with `--no-watch`:

```bash
bin/magento mage-obsidian:frontend:dev --start --no-watch --theme=Vendor/theme
```

This is the inverse of `--start` (HMR): no daemon, no watching — it runs one build and exits. Useful to inspect the real output or to reproduce a CI build locally.

> Leaving the dev loop with `bin/magento mage-obsidian:frontend:dev --down` runs this same build for you (HMR off + rebuild to disk). Reach for `--no-watch` directly when you only want a one-off build without touching HMR.

### The underlying engine bin

`frontend:dev` wraps the build engine's own bin, which you can also run directly from the `vite/` harness (this is what CI uses):

```bash
# from the component's vite/ directory
mage-obsidian:build-themes                  # build every compatible theme
mage-obsidian:build-themes --theme Vendor/theme   # build one
```

`frontend:dev` is the Magento-side entry point (it derives the Vite `.env` from your config first); `build-themes` is the lower-level engine command. Either produces the same output.

!!! tip "Run the CMS export first"
    ```bash
    bin/magento mage-obsidian:cms:export
    ```
    Tailwind scans files, and CMS content lives in a database. The export writes it out so the build
    covers the classes written in pages and blocks; without it, those classes fall to the runtime
    delta instead. See [CMS Content](cms.md).

---

## Production Deployment

Production builds run inside Magento's static-content deploy. See [Deploy to production](../../getting-started/deploy.md).

---

## Benefits

- **Optimized output** — minified, tree-shaken, hashed assets ready for production.
- **Native integration** — production builds happen inside `setup:static-content:deploy`; no extra step in your deploy pipeline.
- **Coexistence** — legacy themes keep using Magento's native static deploy; only modern themes use Vite.

---

See [Development Workflow](../../getting-started/development.md) for the HMR dev server and the full command set, and [HMR](hmr.md) for live reloading during development.
