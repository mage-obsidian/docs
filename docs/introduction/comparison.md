# Choosing a frontend: MageObsidian vs Hyvä vs Luma

Magento 2 has more than one answer to "how should my store's frontend be built?". This page is an honest comparison to help you decide — including when **not** to choose MageObsidian.

## At a glance

| | **MageObsidian** | **Hyvä** | **Luma / Blank** |
|---|---|---|---|
| License | MIT (free, open source) | Theme open source (OSL 3.0 / AFL 3.0, free since Nov 2025); Checkout, Enterprise & UI remain paid | Included with Magento |
| CSS | Tailwind CSS 4 | Tailwind CSS | LESS |
| JavaScript | Vue 3 islands + native ESM | Alpine.js | RequireJS + jQuery + Knockout |
| Build tooling | Vite (dev server + HMR) | Custom build | Grunt / static deploy |
| Templates | `.phtml` + optional Twig engine | `.phtml` (own theme system) | `.phtml` |
| Magento layout XML | Native — layouts, blocks and theme inheritance keep working | Replaced by its own simplified approach | Native |
| Extension ecosystem | Young — compatibility modules for core domains | Large — broad third-party coverage | Universal |
| Maturity | Pre-1.0, under active development | Production-proven since 2021 | Legacy default |
| Performance | Lighthouse 100/100/100/100 on the [live demo]({{ config.extra.demo_url }}) | Excellent | Poor without heavy tuning |

## What makes MageObsidian different

The core design decision: **modernize the toolchain without replacing Magento's frontend architecture.**

- Your **layout XML, blocks, ViewModels and theme inheritance** work exactly as core Magento defines them. A developer who knows Magento theming already knows how MageObsidian themes are organized.
- Modules extend each other's JavaScript through **interceptors** — the same `before`/`around`/`after` plugin pattern Magento uses in PHP, ported to the JS build.
- The dev loop is **Vite with HMR**: edit a template, a Tailwind class or a Vue component and see it instantly, inside a real Magento instance.
- Everything is **MIT-licensed**, from the build engine to the storefront theme.

## When to choose what

**Choose Hyvä** if you need a production-proven stack today — the theme is now free and open source — with paid premium products (Checkout, Enterprise) and a large ecosystem of compatible extensions. It is an excellent product and the safest choice for many agencies right now.

**Choose MageObsidian** if you want a fully open-source stack, prefer Vue over Alpine, value keeping Magento's native layout system, and are comfortable adopting a project that is still completing full Luma parity (see the [roadmap](../roadmap.md)).

**Stay on Luma** only if you maintain an existing store with heavy investment in Luma-based customizations and no budget to migrate yet.

!!! tip "Try it in minutes"
    The fastest way to form an opinion is the [live demo]({{ config.extra.demo_url }}) and the [installation guide](../getting-started/installation.md) on a test instance.
