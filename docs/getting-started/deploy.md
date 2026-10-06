# Deploy to production

There is **no separate build step**. MageObsidian hooks into Magento's standard static-content deploy: its deploy plugins exclude modern themes from the legacy Less/RequireJS pipeline and produce and inject the Vite output (minified, tree-shaken, hashed) as part of the normal command:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

The Vite-generated assets land in the deployed static content alongside everything else. Vite handles minification, tree-shaking and asset hashing for cache-busting automatically.

> **Compatible themes only.** Only themes that ship `etc/mage_obsidian_compatibility.xml` (and have been picked up by `mage-obsidian:frontend:config --generate`) go through the Vite pipeline. Themes without it follow Magento's native deploy untouched.

If you have not installed the theme yet, start with [Installation](installation.md). To build a theme to disk without deploying, see [Building Static Assets](../guides/features/vite-build.md).

## How fast is it?

Legacy static deploys are infamous for taking minutes. Because the Vite build replaces the whole Less/RequireJS pipeline, a MageObsidian theme deploys in seconds, not minutes. Absolute times vary with hardware and theme size, but the Vite build is fast and file materialization dominates.

## Server requirements

Because the Vite build runs *inside* `setup:static-content:deploy`, whatever machine runs that command needs the JS toolchain from [Requirements](requirements.md) — Node ≥ 22 and pnpm ≥ 11 — in addition to PHP. This applies to your deploy box, CI image or build server, not just developer machines. If your pipeline builds static content on a separate build host, only that host needs Node and pnpm.

> **Corepack version mismatch.** `vite/package.json` pins the exact pnpm version via the `packageManager` field. If the server has corepack enabled with a different pnpm active, the build aborts with a version-mismatch error before doing any work. Fix it by activating the pinned version:
>
> ```bash
> corepack prepare pnpm@11.7.0 --activate
> ```
>
> (Match the version to the current `packageManager` pin in `vite/package.json`.)

## Benefits

- **Optimized output** — minified, tree-shaken, hashed assets ready for production.
- **Native integration** — production builds happen inside `setup:static-content:deploy`; no extra step in your deploy pipeline.
- **Coexistence** — legacy themes keep using Magento's native static deploy; only modern themes use Vite.
