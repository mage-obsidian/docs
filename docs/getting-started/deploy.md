---
description: "Deploy MageObsidian to production with Magento's standard static-content deploy, with no separate build step."
---
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

## Subresource Integrity on payment pages

The Vite build writes a `sha384` hash for every chunk into the build manifest. On the pages Magento lists in `SriEnabledActions` (the checkout, the order confirmation and the billing step of multi-address checkout), `ViteResolver` adds `integrity` and `crossorigin` to the module scripts and `modulepreload` links. Chunks that load through a dynamic `import()` cannot carry the attribute, so they are declared in the import map's `integrity` section. A merchant bound by PCI DSS 4.0 requirement 6.4.3 can show that every script the browser runs on those pages is the one that was deployed, and a file changed after the deploy is refused by the browser.

The deploy checks it too: after `setup:static-content:deploy`, the Vite output verifier compares the hashes in the manifest with the deployed files and warns when one differs; with `MAGE_OBSIDIAN_STRICT_DEPLOY=1` it fails the deploy instead. Other pages are served without the attributes and do not depend on them.

This needs framework 4.1.1, whose harness installs engine 4.1.0: an older engine writes no hashes, and the pages are then served without the attributes.

## Benefits

- **Optimized output** — minified, tree-shaken, hashed assets ready for production.
- **Native integration** — production builds happen inside `setup:static-content:deploy`; no extra step in your deploy pipeline.
- **Coexistence** — legacy themes keep using Magento's native static deploy; only modern themes use Vite.
