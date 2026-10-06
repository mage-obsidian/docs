---
description: "Cómo versiona MageObsidian sus dos trenes de versiones, qué cubre el contrato de 4.x, la política de deprecación y qué versiones tienen soporte."
---

# Versiones y soporte

## Versionado semántico

Cada paquete sigue el [versionado semántico](https://semver.org/lang/es/): `MAJOR.MINOR.PATCH`.

- **MAJOR** puede romper el contrato. Es la única versión que elimina algo.
- **MINOR** añade funcionalidades y deprecaciones sin romper el contrato.
- **PATCH** corrige errores y no cambia nada más.

## Dos trenes de versiones { #two-release-trains }

MageObsidian publica dos trenes de versiones independientes. Cada uno versiona todos sus paquetes juntos, así que todos los paquetes de un tren llevan siempre la misma versión.

| Tren | Paquetes | Repositorio |
|---|---|---|
| Framework | `module-modern-frontend`, `module-modern-frontend-cli`, `module-modern-frontend-twig`, `component-modern-frontend`, npm `mage-obsidian` | [`mage-obsidian/framework`]({{ config.extra.gh_framework_url }}) |
| Storefront | los módulos del storefront y `theme-base` | [`mage-obsidian/storefront`]({{ config.extra.gh_storefront_monorepo_url }}) |

El storefront depende del framework y declara la línea de framework que necesita, de modo que los dos trenes se relacionan por ese requisito y no por un número de versión compartido. Storefront 4.0.1 requiere framework 4.x; una versión de parche del storefront no obliga a publicar el framework, ni al revés.

`theme-default` se versiona por su cuenta y vive en [su repositorio]({{ config.extra.gh_theme_default_url }}).

## Qué cubre el contrato de 4.x

El contrato es la superficie que lista la [Referencia](../reference/index.md):

- Los comandos de la CLI y sus opciones.
- Las rutas de configuración.
- Las variables de entorno.
- Las claves de `theme.config.js` y `module.config.ts`.
- El XML de compatibilidad y la versión de esquema del contrato.
- Las funciones y filtros de Twig.
- Los nombres de paquetes.
- Los especificadores `Vendor_Module::path`.
- La API de interceptores JS.

Lo que no está en la Referencia no forma parte del contrato y puede cambiar en cualquier versión.

## Política de deprecación { #deprecation-policy }

Nada del contrato se elimina en una minor ni en un parche. Una deprecación se marca en una versión minor, se anuncia en las [Notas de actualización](../upgrade/index.md) y se elimina en la siguiente major.

## Versiones con soporte

| Línea | Soporte |
|---|---|
| Última minor de 4.x | Recibe correcciones. |
| 3.x | Congelada. Solo hotfixes de emergencia, publicados desde una rama `3.x` del repositorio afectado. |

4.x requiere PHP 8.3+, Node 22+, pnpm 11+ y Magento Open Source o Mage-OS 2.4.7+, según la [tabla de compatibilidad](../getting-started/compatibility.md).

Las preguntas y los reportes van a las Discussions de los monorepos de [framework]({{ config.extra.gh_discussions_framework }}) y [storefront]({{ config.extra.gh_discussions_storefront }}).

## Restricciones en tu composer.json

Usa `^4.0` para todos los paquetes de MageObsidian:

```json
{
    "require": {
        "mage-obsidian/module-modern-frontend": "^4.0"
    }
}
```

No hace falta un techo. `^4.0` acepta todas las versiones 4.x y se detiene en 5.0, y el contrato garantiza que nada de 4.x te rompe. Las versiones de Magento y Mage-OS también son un piso, así que un Magento más nuevo no exige una restricción nueva.
