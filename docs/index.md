---
template: home.html
title: MageObsidian — the modern frontend for Magento
description: Vite, Tailwind CSS 4 and Vue islands on top of Magento's native layouts, blocks and templates. 4.0 is stable.
hero:
  pill: "Stable release · two release trains"
  title: "The modern frontend for Magento,"
  accent: "built on Magento."
  lead: "Vite, Tailwind CSS 4 and Vue islands on top of native layouts, blocks and templates — with a stable contract for all of 4.x."
  ctas:
    - {label: "Get started", href: "getting-started/", primary: true}
    - {label: "Upgrade from 3.x", href: "upgrade/3-to-4/"}
    - {label: "Live demo", href: "https://mage-obsidian-demo.jeanmarcos.dev/", external: true}
install:
  - {tab: composer, lines: ["composer require mage-obsidian/theme-default:^4.0", "bin/magento setup:upgrade"]}
  - {tab: pnpm, lines: ["cd vite && pnpm install --frozen-lockfile", "pnpm build:theme MageObsidian/default"]}
tiles:
  - {eyebrow: "Lighthouse", number: "100", text: "on the demo store, mobile", source: "demo · 2026-09"}
  - {eyebrow: "Verified", number: "317", text: "Luma behaviours", source: "register · 2026-09-22"}
  - {eyebrow: "Compatibility", wide: true, title: "Magento Open Source & Mage-OS", text: "Installed from Packagist on every release.", href: "getting-started/compatibility/"}
paths:
  - {eyebrow: "01 · Evaluate", wide: true, title: "Why MageObsidian", text: "How it compares with Hyvä and Luma, and what is — and is not — verified yet.", href: "why/"}
  - {eyebrow: "02 · Build", title: "Your first theme", text: "A child of OBSIDIAN.", href: "getting-started/first-theme/"}
  - {eyebrow: "03 · Upgrade", title: "From 3.x", text: "Raise the constraints, run one command.", href: "upgrade/3-to-4/"}
---
