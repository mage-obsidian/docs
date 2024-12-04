# Guía de Instalación

Sigue estos pasos para instalar **{{ config.extra.components_name }}** y configurar tu proyecto para el desarrollo.

> **Importante:** Todos los comandos deben ejecutarse desde el directorio raíz de tu proyecto Magento.

Antes de comenzar, asegúrate de que tu entorno cumpla con los [Requisitos Mínimos](../../getting-started/requirements).

---

## Paso 1: Instalar con Composer

Primero, agrega los componentes a tu proyecto Magento utilizando Composer:

```bash
composer require mage-obsidian/component-modern-frontend
```

> **Consejo:** Si tienes problemas con Composer, consulta la [Guía de Solución de Problemas de Composer](https://getcomposer.org/doc/articles/troubleshooting.md).

---

## Paso 2: Instalar dependencias de Node

Asegúrate de que todas las dependencias necesarias de Node estén instaladas:

### pnpm
```bash
pnpm --prefix vite install
```

### npm
```bash
npm --prefix vite install
```

> **Nota:** La carpeta `vite` se genera automáticamente mediante el paquete de Composer e incluye toda la configuración necesaria de Vite para el proyecto.

---

## Paso 3: Habilitar nuevos módulos

Registra los nuevos componentes actualizando la configuración de Magento:

```bash
bin/magento setup:upgrade
```

---

## Paso 4: Generar la configuración inicial

Genera la configuración inicial para los componentes del frontend:

```bash
bin/magento mage-obsidian:frontend:config --generate
```

> **Consejo:** Usa `--help` con el comando para ver opciones adicionales:

```bash
bin/magento mage-obsidian:frontend:config --help
```

---

## Paso 5: Listo para desarrollar

¡Felicidades! Los componentes están configurados y listos para ser utilizados en tu proyecto Magento. Comienza a construir tu tema moderno y aprovecha las herramientas proporcionadas por **{{ config.extra.components_name }}**.

---

## Solución de Problemas

Si tienes problemas durante la instalación, revisa estas soluciones comunes:

- **Problema de permisos:** Asegúrate de que los archivos de tu proyecto tengan la propiedad y permisos correctos.
- **Error de configuración:** Verifica que tu archivo `composer.json` y la configuración de Magento no tengan errores tipográficos ni dependencias faltantes.
- **Problemas con Node Modules:** Ejecuta `npm cache clean --force` y reinstala las dependencias si encuentras errores durante la instalación.
