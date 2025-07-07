## Requisitos previos

Antes de comenzar con **{{ config.extra.components_name }}**, asegúrate de cumplir con los siguientes requisitos:

- **Magento:** Versión 2.4.7 o superior instalada y configurada.
- **PHP:** Version 8.3.
- **Node.js:** Versión 22 o superior instalada en tu entorno.
- **pnpm:** Versión 11 o superior. pnpm es el gestor de paquetes para el que está configurado el harness de Vite (`packageManager` está fijado en `vite/package.json`).
- **Acceso a la terminal:** Permisos para ejecutar comandos en el servidor donde esté alojado Magento.

> El engine de build (`mage-obsidian`) es **ESM-only y está escrito en TypeScript**, se ejecuta sobre Node ≥ 22 con type-stripping nativo —no hay un paso de compilación aparte. Por debajo orquesta **Vite** mediante el harness `vite/` de los componentes.
