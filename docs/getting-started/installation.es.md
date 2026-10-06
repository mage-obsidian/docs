---
description: "Instala el tema MageObsidian desde Packagist, genera el contrato, compila los assets y comprueba el storefront."
---
# Instalación

{{ verified('install') }}

Los pasos 1 a 6 son la receta que la matriz de versiones ejecuta en cada plataforma listada en [Compatibilidad](compatibility.md): los paquetes publicados, instalados desde Packagist en una tienda limpia y construidos, seguidos de una verificación rápida del storefront. El paso 7 es el paso de producción y no forma parte de la corrida de la matriz. Con `^4.0`, Composer instala los módulos del storefront 4.0.1 y el framework y `theme-default` 4.0.0. Revisa primero los [requisitos](requirements.md). En Adobe Commerce, lee también [Instalar en Adobe Commerce](adobe-commerce.md).

## 1. Requerir el tema

`mage-obsidian/theme-default` trae `theme-base`, el framework, el harness de Vite y toda la pila de módulos del storefront:

```bash
composer require mage-obsidian/theme-default:^4.0
```

## 2. Registrar los módulos

```bash
bin/magento setup:upgrade
```

## 3. Activar el tema

En el Admin, ve a **Content › Design › Configuration**, edita el scope que quieras y elige **MageObsidian — Default (Obsidian)** como tema aplicado.

## 4. Generar el contrato PHP ↔ JS

```bash
bin/magento mage-obsidian:frontend:config --generate
```

## 5. Preparar el harness de Vite

El harness `vite/` debe estar en la raíz de Magento. Si falta `vite/package.json`, cópialo desde el paquete instalado:

```bash
[ -f vite/package.json ] || { rm -rf vite && cp -r vendor/mage-obsidian/component-modern-frontend/vite vite; }
```

Crea `vite/.env` a partir de `vite/.env.sample` con los valores de tu host y luego instala las dependencias de Node tal como están bloqueadas:

```bash
cd vite
pnpm install --frozen-lockfile
```

El `.env` lleva `VITE_SERVER_HOST`, `VITE_SERVER_PORT`, `VITE_SERVER_SECURE`, `VITE_HMR_PATH`, `MAGENTO_HOST` y `VITE_SERVER_ALLOWED_HOSTS`. Sin él, el build se detiene en una shell no interactiva.

## 6. Construir el tema

Desde el directorio `vite/`:

```bash
pnpm build:theme MageObsidian/default
```

## 7. Desplegar el contenido estático y vaciar la caché

De vuelta en la raíz de Magento:

```bash
bin/magento setup:static-content:deploy
bin/magento cache:flush
```

Abre el storefront: la home se renderiza con sus islas de Vue. Para producción, consulta [Despliegue a producción](deploy.md).

> **Nota:** La instalación incluye por defecto el [motor Twig](../guides/twig.md) opcional (un motor `.twig` junto a `.phtml`). No cambia nada de tus plantillas `.phtml` existentes; si no lo quieres, [desactívalo](../guides/twig.md#deshabilitar-twig) con `bin/magento module:disable MageObsidian_ModernFrontendTwig`.

## Siguientes pasos

- [Tu primer tema hijo](first-theme.md) para personalizar el tema.
- [Flujo de desarrollo](development.md) para recarga en vivo con HMR.
- [Por qué MageObsidian](../why/index.md) y la [guía del tema](../guides/themes/obsidian.md).
