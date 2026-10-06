---
description: "Despliega MageObsidian a producción con el static-content deploy estándar de Magento, sin un paso de build aparte."
---
# Despliegue a producción

**No hay un paso de build aparte**. MageObsidian se engancha al deploy de contenido estático estándar de Magento: sus plugins de deploy excluyen los temas modernos del pipeline legacy de Less/RequireJS y producen e inyectan la salida de Vite (minificada, con tree-shaking y hash) como parte del comando normal:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

Los assets generados por Vite quedan en el contenido estático desplegado junto a todo lo demás. Vite se encarga de la minificación, el tree-shaking y el hashing de assets para cache-busting automáticamente.

> **Solo temas compatibles.** Solo los temas que entregan `etc/mage_obsidian_compatibility.xml` (y han sido detectados por `mage-obsidian:frontend:config --generate`) pasan por el pipeline de Vite. Los temas sin él siguen el deploy nativo de Magento intacto.

Si aún no has instalado el tema, empieza por [Instalación](installation.md). Para construir un tema a disco sin desplegar, consulta [Compilar Assets Estáticos](../guides/features/vite-build.md).

## ¿Qué tan rápido es?

Los deploys estáticos legacy son famosos por tardar minutos. Como el build de Vite reemplaza todo el pipeline de Less/RequireJS, un tema MageObsidian se despliega en segundos, no en minutos. Los tiempos absolutos varían con el hardware y el tamaño del tema, pero el build de Vite es rápido y domina la materialización de archivos.

## Requisitos del servidor

Como el build de Vite corre *dentro* de `setup:static-content:deploy`, la máquina que ejecute ese comando necesita el toolchain JS de [Requisitos](requirements.md) —Node ≥ 22 y pnpm ≥ 11— además de PHP. Esto aplica a tu servidor de deploy, imagen de CI o build server, no solo a las máquinas de desarrollo. Si tu pipeline construye el contenido estático en un build host separado, solo ese host necesita Node y pnpm.

> **Mismatch de versión con corepack.** `vite/package.json` fija la versión exacta de pnpm vía el campo `packageManager`. Si el servidor tiene corepack habilitado con otro pnpm activo, el build aborta con un error de version-mismatch antes de hacer nada. Se arregla activando la versión fijada:
>
> ```bash
> corepack prepare pnpm@11.7.0 --activate
> ```
>
> (Ajusta la versión al pin `packageManager` vigente en `vite/package.json`.)

## Beneficios

- **Salida optimizada** — assets minificados, con tree-shaking y hash, listos para producción.
- **Integración nativa** — los builds de producción ocurren dentro de `setup:static-content:deploy`; sin paso extra en tu pipeline de deploy.
- **Coexistencia** — los temas legacy siguen usando el deploy estático nativo de Magento; solo los temas modernos usan Vite.
