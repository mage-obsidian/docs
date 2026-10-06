---
description: "An honest comparison of MageObsidian, Hyvä and Luma, including when not to choose MageObsidian."
---
# Choosing a frontend: MageObsidian vs Hyvä vs Luma

Magento 2 has more than one answer to "how should my store's frontend be built?". This page is an honest comparison to help you decide — including when **not** to choose MageObsidian.

## At a glance

<div class="mo-table-scroll" tabindex="0" role="region" aria-label="Comparison" markdown>

<table markdown>
<thead markdown>
<tr markdown>
<th scope="col" markdown>Feature</th>
<th scope="col" markdown>**MageObsidian**</th>
<th scope="col" markdown>**Hyvä**</th>
<th scope="col" markdown>**Luma / Blank**</th>
</tr>
</thead>
<tbody markdown>
<tr markdown>
<th scope="row" markdown>License</th>
<td markdown>MIT (free, open source)</td>
<td markdown>Theme open source (OSL 3.0 / AFL 3.0, free since Nov 2025); Checkout, Enterprise & UI remain paid</td>
<td markdown>Included with Magento</td>
</tr>
<tr markdown>
<th scope="row" markdown>CSS</th>
<td markdown>Tailwind CSS 4</td>
<td markdown>Tailwind CSS</td>
<td markdown>LESS</td>
</tr>
<tr markdown>
<th scope="row" markdown>JavaScript</th>
<td markdown>Vue 3 islands + native ESM</td>
<td markdown>Alpine.js</td>
<td markdown>RequireJS + jQuery + Knockout</td>
</tr>
<tr markdown>
<th scope="row" markdown>Build tooling</th>
<td markdown>Vite (dev server + HMR)</td>
<td markdown>Custom build</td>
<td markdown>Grunt / static deploy</td>
</tr>
<tr markdown>
<th scope="row" markdown>Templates</th>
<td markdown>`.phtml` + optional Twig engine</td>
<td markdown>`.phtml` (own theme system)</td>
<td markdown>`.phtml`</td>
</tr>
<tr markdown>
<th scope="row" markdown>Magento layout XML</th>
<td markdown>Native — layouts, blocks and theme inheritance keep working</td>
<td markdown>Replaced by its own simplified approach</td>
<td markdown>Native</td>
</tr>
<tr markdown>
<th scope="row" markdown>Extension ecosystem</th>
<td markdown>Young — compatibility modules for core domains</td>
<td markdown>Large — broad third-party coverage</td>
<td markdown>Universal</td>
</tr>
<tr markdown>
<th scope="row" markdown>Maturity</th>
<td markdown>Stable (4.0, October 2026)</td>
<td markdown>Production-proven since 2021</td>
<td markdown>Legacy default</td>
</tr>
<tr markdown>
<th scope="row" markdown>Performance</th>
<td markdown>Lighthouse 100/100/100/100 on the [live demo]({{ config.extra.demo_url }})</td>
<td markdown>Excellent</td>
<td markdown>Poor without heavy tuning</td>
</tr>
</tbody>
</table>

</div>

## What makes MageObsidian different

The core design decision: **modernize the toolchain without replacing Magento's frontend architecture.**

- Your **layout XML, blocks, ViewModels and theme inheritance** work exactly as core Magento defines them. A developer who knows Magento theming already knows how MageObsidian themes are organized.
- Modules extend each other's JavaScript through **interceptors** — the same `before`/`around`/`after` plugin pattern Magento uses in PHP, ported to the JS build.
- The dev loop is **Vite with HMR**: edit a template, a Tailwind class or a Vue component and see it instantly, inside a real Magento instance.
- Everything is **MIT-licensed**, from the build engine to the storefront theme.

## When to choose what

**Choose Hyvä** if you need a production-proven stack today — the theme is now free and open source — with paid premium products (Checkout, Enterprise) and a large ecosystem of compatible extensions. It is an excellent product and the safest choice for many agencies right now.

**Choose MageObsidian** if you want a fully open-source stack, prefer Vue over Alpine, value keeping Magento's native layout system, and are comfortable adopting a project that is still completing full Luma parity (see the [roadmap](../project/roadmap.md)).

**Stay on Luma** only if you maintain an existing store with heavy investment in Luma-based customizations and no budget to migrate yet.

!!! tip "Try it in minutes"
    The fastest way to form an opinion is the [live demo]({{ config.extra.demo_url }}) and the [installation guide](../getting-started/installation.md) on a test instance.
