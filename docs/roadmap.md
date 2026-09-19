# Roadmap

Where the project stands and where it is going. This roadmap is intentionally high-level and may change — follow [GitHub Discussions](https://github.com/mage-obsidian/module-modern-frontend/discussions) for updates.

## ✅ Available today

- **Core engine** — Vite build with HMR inside Magento, Tailwind CSS 4, native ESM, theme inheritance resolution, JS interceptors and per-theme precompilation.
- **Vue 3 islands** — interactive components mounted lazily over server-rendered pages, with automatic `modulepreload` of the eager island graph.
- **Twig engine (optional)** — write `.twig` templates alongside `.phtml`.
- **CLI** — config contract generation, HMR management, module/theme inspection.
- **Performance features** — opt-in critical CSS generation, JSON-LD structured data (Organization, WebSite, BreadcrumbList, Product).
- **Storefront** — `module-storefront` plus compatibility modules for catalog, search, customer, sales, wishlist, reviews and more, paired with the OBSIDIAN theme. See it running on the [live demo]({{ config.extra.demo_url }}).
- **Checkout, end to end** — a one-page checkout that carries a cart to a placed order: guest and signed-in, addresses, shipping method selection, totals, coupons, gift messages, multishipping, instant purchase and stored cards.
- **Payment method extension point** — a payment method can render its own interface inside the checkout island, ask for its own fields, and hand the shopper over to a gateway and back. What is verified is the mechanism, exercised by a purpose-built probe method; no commercial gateway has been verified (see below).
- **Translations** — `bin/magento mage-obsidian:i18n:collect` collects phrases from `.vue`, `.ts`, `.js` and `.twig` into each component's `i18n/<locale>.csv`; the default theme ships `en_US` and `es_ES`.

## 📊 What has been verified

Measured on 2026-09-22 against **Magento Open Source 2.4.9** with the
[verification harness](https://github.com/mage-obsidian/storefront-verification), on the
`theme-default` / `theme-base` pair:

| Register | Figure |
|---|---|
| Parity entries | 485 — 317 covered, 138 out of scope, 27 resolved, 3 blocked |
| Page layouts | 15 entries, 13 covered by an executed test, 2 out of scope |
| Build engine unit tests | 321 |
| Harness unit tests | 268 |

A "covered" entry means a test ran and observed the behaviour on that platform; a
declaration in a theme never counts as coverage on its own.

**What these figures do not say:**

- **No commercial payment gateway has been verified.** The payment extension point is exercised
  with a simulated method built for the harness. A real gateway needs its own verification.
- **One platform, one version.** Everything above was observed on Magento Open Source 2.4.9.
  Nothing here claims Adobe Commerce or another 2.4.x minor.
- **Entries still open.** 3 blocked and 138 out-of-scope entries carry their reason in the
  register; they are not silently counted as working.

## 🚧 In progress

- **Full Luma parity for the default theme** — closing the entries the register still lists as
  blocked or uncovered, so a store can switch to MageObsidian without losing any stock
  functionality.

## 🔜 Planned

- **Stable release** once parity is reached, with curated release notes and an upgrade guide.
- **Showcase** of stores running MageObsidian in production — [tell us about yours](https://github.com/mage-obsidian/module-modern-frontend/discussions)!

!!! note "A note on pace"
    MageObsidian is developed in the maintainer's free time. If it saves you time, consider [supporting the project](support/project.md) — it directly accelerates this roadmap.
