---
description: En qué versiones de Magento y Mage-OS se instaló y probó cada versión de MageObsidian.
---

# Compatibilidad

{{ verified('matrix') }}


Cada versión de MageObsidian se instala desde Packagist en una tienda limpia para cada plataforma
de abajo, y debe renderizar el storefront con sus islas Vue.

<ul class="mo-legend">
  <li><strong>✅ Pasa</strong> se instaló y renderizó el storefront con sus islas</li>
  <li><strong>❌ Falla</strong> se probó y no lo hizo</li>
  <li><strong>⏳ Sin ejecutar</strong> aún no se ha ejecutado para esta versión</li>
</ul>

## {{ compatibility.release_label }}

{{ compat_table() }}

El storefront 4.0.0 falló en PHP 8.3 y 8.4 y en Magento 2.4.7. El storefront 4.0.1 lo corrigió, por
lo que la versión mínima del storefront es 4.0.1; Composer la elige con `^4.0`.

Los paquetes declaran un piso (`magento/framework >=103.0.7`, Magento 2.4.7) y ningún techo, así que
Composer no te detendrá en un Magento más nuevo: consulta esta tabla antes de actualizar Magento.

## Por qué una versión no se instala

    composer why-not mage-obsidian/theme-default 4.0.0

## Trenes de versiones

El framework y el storefront publican cada uno todos sus paquetes bajo una misma versión; consulta
[Versiones y soporte](../project/versioning.md#two-release-trains).
