# Roadmap

Where the project stands and where it is going. This roadmap is intentionally high-level and may change — follow [GitHub Discussions](https://github.com/mage-obsidian/module-modern-frontend/discussions) for updates.

## ✅ Available today

- **Core engine** — Vite build with HMR inside Magento, Tailwind CSS 4, native ESM, theme inheritance resolution, JS interceptors and per-theme precompilation.
- **Vue 3 islands** — interactive components mounted lazily over server-rendered pages, with automatic `modulepreload` of the eager island graph.
- **Twig engine (optional)** — write `.twig` templates alongside `.phtml`.
- **CLI** — config contract generation, HMR management, module/theme inspection.
- **Performance features** — opt-in critical CSS generation, JSON-LD structured data (Organization, WebSite, BreadcrumbList, Product).
- **Storefront foundation** — `module-storefront` plus compatibility modules for catalog, search, checkout (cart), customer, sales, wishlist, reviews and more, paired with the OBSIDIAN theme. See it running on the [live demo]({{ config.extra.demo_url }}).

## 🚧 In progress

- **Full Luma parity for the default theme** — completing the remaining storefront domains and end-to-end QA so a store can switch to MageObsidian without losing any stock functionality.

## 🔜 Planned

- **Stable release** once parity is reached, with curated release notes and an upgrade guide.
- **Showcase** of stores running MageObsidian in production — [tell us about yours](https://github.com/mage-obsidian/module-modern-frontend/discussions)!

!!! note "A note on pace"
    MageObsidian is developed in the maintainer's free time. If it saves you time, consider [supporting the project](support/project.md) — it directly accelerates this roadmap.
