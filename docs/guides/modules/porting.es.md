# Portar una extensión de Luma

{{ verified('porting') }}

Una extensión de Luma tiene tres partes que el nuevo frontend no lee: una plantilla `.phtml`, un script de RequireJS/KnockoutJS y LESS. Portarla consiste en sustituir cada una por su equivalente y avisar al framework de que el módulo participa. Esta guía lo hace con un módulo ficticio, `Acme_Badge`, que muestra una insignia descartable "Novedad" en la página de inicio.

Los pasos salen de un port real: un módulo de tienda que además necesitó el archivo de compatibilidad (incluye recursos estáticos y, sin la declaración, no se despliegan bajo un tema Obsidian) y un plugin sobre un ViewModel de `MageObsidian\Catalog`. `Acme_Badge` reproduce los mismos movimientos con código escrito para esta página.

## El módulo de Luma

```
app/code/Acme/Badge/
├── registration.php
├── etc/module.xml
└── view/frontend/
    ├── layout/cms_index_index.xml
    ├── requirejs-config.js
    ├── templates/badge.phtml
    └── web/
        ├── js/badge.js
        └── css/source/_module.less
```

`badge.phtml` montaba un widget de jQuery mediante `data-mage-init`:

```php
<p class="acme-badge" data-mage-init='{"Acme_Badge/js/badge": {"label": "<?= $block->escapeHtmlAttr(__('New arrival')) ?>"}}'></p>
```

`requirejs-config.js` mapeaba el widget y `badge.js` lo definía con `define(['jquery'], …)`. Nada de eso se ejecuta bajo {{ config.extra.components_name }}: no hay RequireJS ni Knockout.

## Paso 1: declarar la compatibilidad

Un módulo que no se declara se ignora: su layout, sus bloques y su configuración de frontend nunca llegan a la página. Añade `etc/mage_obsidian_compatibility.xml`:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
    <features>
        <compatibility>true</compatibility>
    </features>
</config>
```

Añade `MageObsidian_ModernFrontend` al `<sequence>` de `etc/module.xml`. El archivo y su indicador opcional `universal` se explican en [Hacer un módulo compatible](compatibility.md). Hazlo incluso en un módulo sin JavaScript: también decide si se despliegan los recursos estáticos del módulo.

## Paso 2: sustituir el `.phtml`

El layout sigue funcionando, pero apunta el bloque a una plantilla que renderice el motor de tu tema y usa la clase de bloque del framework, que aporta los ayudantes de islas. Con el módulo Twig instalado:

{% raw %}
```xml
<block class="MageObsidian\ModernFrontend\Block\Template" name="acme.badge"
       template="Acme_Badge::badge.twig"/>
```

```twig
{{ render_vue('Acme_Badge::Badge', { label: __('New arrival'), dismissLabel: __('Dismiss') }) }}
```
{% endraw %}

Sin Twig, conserva un `.phtml` y llama a `$block->renderVueComponent('Acme_Badge::Badge', $props)`; consulta [Plantillas (.phtml)](phtml.md). Las props son datos simples: pasa cadenas ya traducidas, no un JSON de `data-mage-init`.

## Paso 3: llevar el script a una isla de Vue

El comportamiento del widget pasa a ser un componente en `view/frontend/web/components/Badge.vue`:

```vue
<script setup>
import { ref } from "vue";

defineProps({
    label: { type: String, required: true },
    dismissLabel: { type: String, required: true },
});

const visible = ref(true);
</script>

<template>
    <p v-if="visible" class="acme-badge">
        <span>{{ label }}</span>
        <button type="button" :aria-label="dismissLabel" @click="visible = false">×</button>
    </p>
</template>
```

Usa una isla cuando el script gobierna marcado. Si es lógica simple sin marcado, escribe un módulo ESM en `view/frontend/web/js/` y úsalo con un especificador `Vendor_Module::`; consulta [JavaScript e importaciones](javascript.md). Nunca importes entre módulos con una ruta relativa: se salta la herencia de temas.

Elimina `requirejs-config.js` y el archivo del widget. Las plantillas de Knockout con `data-bind` no tienen equivalente: reconstrúyelas como plantillas de componente.

Los plugins sobre un bloque o ViewModel del core solo se trasladan si el destino existe en el nuevo storefront. Apunta el `<plugin>` al ViewModel `MageObsidian\*` equivalente, en `etc/frontend/di.xml`.

## Paso 4: estilos con Tailwind

Sustituye el LESS por `view/frontend/web/css/module.extend.css`. Tailwind 4 es CSS-first, así que las utilidades se aplican con `@apply`:

```css
.acme-badge {
    @apply inline-flex items-center gap-2 rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-900;
}

.acme-badge button {
    @apply cursor-pointer leading-none;
}
```

El CSS del módulo se importa antes que el del tema, de modo que un tema todavía puede sobrescribir tus tokens. Más en [Configuración](configuration.md).

## Paso 5: generar el contrato y compilar

```bash
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
```

Después recarga PHP-FPM. El contrato se carga con `require` y, cuando `opcache.validate_timestamps` está desactivado (lo habitual en producción y el valor por defecto en el stack local), los workers web siguen sirviendo la copia que tienen en caché. El síntoma es un tema o módulo que la CLI ve y la página no: faltan los layouts de los módulos `MageObsidian_*`. Reinicia el servicio PHP con el que habla tu servidor web (`zento compose restart php php-noxdebug` en el stack local), compila y vacía la caché:

```bash
pnpm build:theme MageObsidian/default
bin/magento cache:flush
```

Ejecuta `pnpm` desde el directorio `vite/`. El layout del contrato también queda en la caché de layout, por eso el vaciado importa.

## Paso 6: comprobarlo

Pide la página y busca el marcador de isla:

```bash
curl -s https://your-store.test/ | grep -c 'data-mage-island'
```

En la ejecución de verificación la home pasó de 9 a 10 islas, y el nuevo marcador apuntaba a `generated/Acme_Badge/components/Badge.js`, que respondió 200. La hoja de estilos compilada contenía las reglas de `.acme-badge`.

Lista de comprobación final:

- [ ] `etc/mage_obsidian_compatibility.xml` existe y `MageObsidian_ModernFrontend` está en la secuencia del módulo.
- [ ] `setup:upgrade` se ejecutó y `module:status` muestra el módulo como habilitado.
- [ ] `mage-obsidian:frontend:config --generate` se ejecutó y PHP-FPM se recargó después.
- [ ] El tema se recompiló y se ejecutó `cache:flush`.
- [ ] La página contiene un marcador `data-mage-island` para tu componente y su JavaScript devuelve 200.
- [ ] No queda ningún `requirejs-config.js`, `data-mage-init`, `x-magento-init` ni `.less` en el módulo.

Si un paso no se comporta como se espera, la [referencia del contrato](../../reference/contract.md) describe lo que escribe `--generate` y lo que valida el build. Las islas, sus estrategias y la hidratación están en [Islas de Vue](../vue/islands.md).
