## Prerequisites

Before starting with **{{ config.extra.components_name }}**, make sure you meet the following requirements:

- **Magento:** Magento Open Source 2.4.7 or higher installed and configured.
- **PHP:** Version 8.3.
- **Node.js:** Version 22 or higher installed in your environment.
- **pnpm:** Version 11 or higher. pnpm is the package manager the Vite harness is set up for (`packageManager` is pinned in `vite/package.json`).
- **Terminal access:** Permissions to run commands on the server where Magento is hosted.

> The build engine (`mage-obsidian`) is **ESM-only and written in TypeScript**, run on Node ≥ 22 with native type-stripping — there is no separate compile step. It drives **Vite** under the hood via the components' `vite/` harness.