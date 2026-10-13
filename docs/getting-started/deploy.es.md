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

## Subresource Integrity en las páginas de pago

El build de Vite escribe un hash `sha384` por cada chunk en el manifiesto de la compilación. En las páginas que Magento lista en `SriEnabledActions` (el checkout, la confirmación del pedido y el paso de facturación del checkout multidirección), `ViteResolver` añade `integrity` y `crossorigin` a los scripts de módulo y a los `modulepreload`. Los chunks que se cargan con un `import()` dinámico no pueden llevar el atributo, así que se declaran en la sección `integrity` del import map. Un comerciante sujeto al requisito 6.4.3 de PCI DSS 4.0 puede demostrar que cada script que el navegador ejecuta en esas páginas es el que se desplegó, y un archivo modificado después del deploy es rechazado por el navegador.

El deploy también lo comprueba: tras `setup:static-content:deploy`, el verificador de la salida de Vite compara los hashes del manifiesto con los archivos desplegados y avisa si alguno difiere; con `MAGE_OBSIDIAN_STRICT_DEPLOY=1` hace fallar el deploy. Las demás páginas se sirven sin los atributos y no dependen de ellos.

Requiere el framework 4.1.1, cuyo harness instala el motor 4.1.0: un motor anterior no escribe los hashes, y entonces las páginas se sirven sin los atributos.

## Beneficios

- **Salida optimizada** — assets minificados, con tree-shaking y hash, listos para producción.
- **Integración nativa** — los builds de producción ocurren dentro de `setup:static-content:deploy`; sin paso extra en tu pipeline de deploy.
- **Coexistencia** — los temas legacy siguen usando el deploy estático nativo de Magento; solo los temas modernos usan Vite.
