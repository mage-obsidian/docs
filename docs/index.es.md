---
template: home.html
hide:
  - navigation
  - toc
title: MageObsidian — el frontend moderno para Magento
description: Vite, Tailwind CSS 4 e islas Vue sobre los layouts, bloques y plantillas nativos de Magento. La 4.0 es estable.
hero:
  pill: "Versión estable · dos trenes de versiones"
  title: "El frontend moderno para Magento,"
  accent: "construido sobre Magento."
  lead: "Vite, Tailwind CSS 4 e islas Vue sobre layouts, bloques y plantillas nativos — con un contrato estable para toda la 4.x."
  ctas:
    - {label: "Primeros pasos", href: "getting-started/", primary: true}
    - {label: "Actualizar desde 3.x", href: "upgrade/3-to-4/"}
    - {label: "Demo en vivo", href: "https://mage-obsidian-demo.jeanmarcos.dev/", external: true}
install:
  - {tab: composer, lines: ["composer require mage-obsidian/theme-default:^4.0", "bin/magento setup:upgrade"]}
  - {tab: pnpm, lines: ["cd vite && pnpm install --frozen-lockfile", "pnpm build:theme MageObsidian/default"]}
tiles:
  - {eyebrow: "Lighthouse", number: "100", text: "en la tienda demo, móvil", source: "Lighthouse 13.5.0 · 2026-10-06", href: "why/showcase/"}
  - {eyebrow: "Verificadas", number: "247", text: "pantallas de Luma, completas", source: "registro · 2026-10-06", href: "project/known-scope/"}
  - {eyebrow: "Compatibilidad", wide: true, title: "Magento Open Source y Mage-OS", text: "Se instala desde Packagist en cada versión.", href: "getting-started/compatibility/"}
paths:
  - {eyebrow: "01 · Evaluar", wide: true, title: "Por qué MageObsidian", text: "Cómo se compara con Hyvä y Luma, y qué está —y qué no— verificado todavía.", href: "why/"}
  - {eyebrow: "02 · Construir", title: "Tu primer tema", text: "Un hijo de OBSIDIAN.", href: "getting-started/first-theme/"}
  - {eyebrow: "03 · Actualizar", title: "Desde 3.x", text: "Sube las restricciones, ejecuta un comando.", href: "upgrade/3-to-4/"}
---
