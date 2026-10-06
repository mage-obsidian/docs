---
description: "MageObsidian 4.0 es la primera versión estable: un contrato estable para toda la serie 4.x, dos trenes de versiones y una tabla de compatibilidad probada."
---

# Novedades de 4.0

## 4.0 es estable

MageObsidian 4.0 es la primera versión estable. A partir de ahora, la superficie que lista la [Referencia](../reference/index.md) no cambia de forma incompatible hasta la 5.0. Lo que cubre y cuánto tiempo se mantiene cada línea está en [Versiones y soporte](../project/versioning.md).

## Mismos paquetes, mismo código

Ningún paquete fue renombrado. Los nombres de Packagist y npm son los mismos que ya usas.

4.0.0 publicó el último código de 2.x y 3.x más las cabeceras de licencia SPDX. Esas cabeceras causaron una regresión, corregida el mismo día en storefront 4.0.1: las plantillas fallaban en PHP 8.3 y 8.4, y faltaba una variable de plantilla en Magento 2.4.7.

## Dos trenes de versiones

El framework y el storefront se versionan por separado. Cada tren versiona todos sus paquetes juntos.

- **Framework:** `module-modern-frontend`, `module-modern-frontend-cli`, `module-modern-frontend-twig`, `component-modern-frontend` y el paquete npm `mage-obsidian`.
- **Storefront:** los módulos del storefront y `theme-base`.

El storefront declara la línea de framework que necesita, de modo que una versión del storefront nunca se instala sobre un framework para el que no fue construida. Consulta [Dos trenes de versiones](../project/versioning.md#two-release-trains).

## Dónde vive el código

El framework vive en el monorepo [`mage-obsidian/framework`]({{ config.extra.gh_framework_url }}) y el storefront en [`mage-obsidian/storefront`]({{ config.extra.gh_storefront_monorepo_url }}). Los repositorios por paquete son espejos de solo lectura: abre issues y pull requests en los monorepos. `theme-default` sigue en [su propio repositorio]({{ config.extra.gh_theme_default_url }}).

## Compatibilidad

Las seis combinaciones de Magento Open Source y Mage-OS 2.4.7, 2.4.8 y 2.4.9 pasaron el 2026-10-06, con framework 4.0.0 y storefront 4.0.1. Magento y Mage-OS 2.4.7 es el piso y no hay techo: se espera que las versiones más nuevas funcionen y se añaden a la tabla cuando se prueban. Consulta la [tabla de compatibilidad](../getting-started/compatibility.md).

## Actualizar desde 3.x

La actualización cambia tus restricciones de versión y nada más. Sigue [Actualizar de 3.x a 4.0](../upgrade/3-to-4.md).

## Lo que aún no está verificado

Hay áreas que no se han probado con la misma profundidad que el resto. Están listadas, con su estado, en [Alcance conocido](../project/known-scope.md).
