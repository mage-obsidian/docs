---
description: "The Magento, PHP, Node.js and pnpm versions and the terminal access you need before installing MageObsidian."
---
# Requirements

Before starting with **{{ config.extra.components_name }}**, make sure you meet the following requirements:

- **Magento:** Magento Open Source or Mage-OS 2.4.7 or higher, installed and configured. See [Compatibility](compatibility.md) for the versions each release was tested on.
- **Adobe Commerce:** 2.4.7 or higher, with its own Composer keys. See [Install on Adobe Commerce](adobe-commerce.md).
- **PHP:** Version 8.3 or higher.
- **Node.js:** Version 22 or higher installed in your environment.
- **pnpm:** Version 11 or higher. pnpm is the package manager the Vite harness is set up for (`packageManager` is pinned in `vite/package.json`).
- **Terminal access:** Permissions to run commands on the server where Magento is hosted.

> The build engine (`mage-obsidian`) is **ESM-only and written in TypeScript**, run on Node ≥ 22 with native type-stripping — there is no separate compile step. It drives **Vite** under the hood via the components' `vite/` harness.
