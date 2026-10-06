---
description: Crea un tema hijo de OBSIDIAN, cambia un token de color, sobrescribe un componente Vue y comprueba ambos cambios en la tienda.
---

# Tu primer tema hijo

{{ verified('storefront') }}

Vas a crear `Acme/child`, un tema que hereda de `MageObsidian/default` (OBSIDIAN), cambiar su color de acento, sobrescribir un componente Vue, compilarlo y ver ambos cambios en la home. Cada comando y cada salida de abajo proviene de ejecutar este tutorial de principio a fin en una tienda, y la tienda quedó como estaba después.

Los comandos se muestran como `bin/magento …` desde la raíz de Magento. En un proyecto zento, antepón `zento magento` y ejecútalos desde la raíz del proyecto.

## 1. Genera el tema

```bash
bin/magento mage-obsidian:generate:theme Acme/child --parent=MageObsidian/default --title="Child"
```

```text
 [!] Theme Acme/child created at /var/www/html/app/design/frontend/Acme/child

  Files generated
  registration.php
  theme.xml
  etc/mage_obsidian_compatibility.xml
  web/theme.config.js
  web/css/theme.source.css
  .gitignore

 Next steps:
     Activate the theme in Content > Design > Configuration (or via config),
     then: bin/magento mage-obsidian:frontend:config --generate
```

`theme.xml` declara ahora `<parent>MageObsidian/default</parent>` y `etc/mage_obsidian_compatibility.xml` incorpora el tema al build del frontend. Las opciones están en [Scaffolding](scaffolding.md#generar-un-tema).

## 2. Actívalo

Magento registra un tema nuevo durante `setup:upgrade`:

```bash
bin/magento setup:upgrade --keep-generated
```

```text
Upgrade completed successfully.
```

Luego abre **Content → Design → Configuration**, edita la fila de tu vista de tienda o la global y elige **Child** como tema aplicado. El mismo ajuste por línea de comandos es `design/theme/theme_id`, con el id que la tabla `theme` le dio a `Acme/child` (7 en la tienda usada aquí):

```bash
bin/magento config:set design/theme/theme_id 7
```

```text
Value was saved.
```

## 3. Cambia un token de color

OBSIDIAN define sus colores como tokens de Tailwind 4 en su propio `theme.source.css`, entre ellos `--color-accent: #2f6e66`. El source del hijo se carga después del padre, así que redefinir el token en el hijo gana. Edita `app/design/frontend/Acme/child/web/css/theme.source.css`:

```css
@import "tailwindcss";

@theme {
  --color-accent: #b4232a;
}
```

## 4. Sobrescribe un componente Vue

Un tema sobrescribe un archivo de un módulo recreando su ruta bajo una carpeta con el nombre del módulo. El indicador del carrito en el encabezado es `MageObsidian_Storefront::cart/CartCount`; para reemplazarlo, crea:

```text
app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart/CartCount.vue
```

{% raw %}
```vue
<script setup lang="ts">
import { computed } from "vue";
import Icon from "MageObsidian_ModernFrontend::elements/Icon";
import { useCustomerData } from "MageObsidian_ModernFrontend::js/customer-data";

withDefaults(defineProps<{ label?: string }>(), { label: "in your bag" });

const customerData = useCustomerData();
const count = computed(() => Number(customerData.section("cart")?.summary_count ?? 0));
</script>

<template>
    <span class="cart-count relative inline-flex items-center" data-allow-mismatch="children">
        <Icon name="shopping-cart" set="outline" class="h-5 w-5" />
        <span class="cart-count__badge mo-badge" aria-hidden="true">{{ count }}</span>
        <span class="sr-only" role="status" aria-live="polite">{{ `${count} ${label}` }}</span>
    </span>
</template>
```
{% endraw %}

Esta copia muestra un icono de carrito en lugar de la bolsa. Las importaciones entre módulos usan `Vendor_Module::path`, nunca una ruta relativa, para que la sobrescritura siga siendo alcanzable por los hijos de tu tema.

## 5. Regenera el contrato y compila

```bash
bin/magento mage-obsidian:frontend:config --generate
```

```text
 ===========================================================
  /var/www/html/app/etc/mage_obsidian_frontend_modules.php
  /var/www/html/app/etc/mage_obsidian_frontend_modules.json
 ===========================================================
```

Comprueba que el contrato lista el tema:

```bash
bin/magento mage-obsidian:frontend:config --show --themes
```

```text
  Acme/child                /var/www/html/app/design/frontend/Acme/child
```

Luego compílalo, desde la carpeta `vite/` de la raíz de Magento:

```bash
pnpm build:theme Acme/child
```

```text
✓ built in 799ms
✓ Acme/child built
```

Vacía la caché para que la tienda tome el tema nuevo:

```bash
bin/magento cache:flush
```

## 6. Míralo en la home

```bash
curl -sk -o home.html -w "%{http_code}\n" https://your-store.test/
```

```text
200
```

La página ahora carga sus assets desde el hijo:

```bash
grep -o 'frontend/[A-Za-z]*/[a-z]*' home.html | sort | uniq -c
```

```text
     20 frontend/Acme/child
```

Descarga los archivos compilados y busca ambos cambios:

```bash
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/css/style.css | grep -o -- '--color-accent:[^;]*' | head -1
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/MageObsidian_Storefront/components/cart/CartCount.js | grep -o 'shopping-[a-z]*' | sort -u
```

```text
--color-accent:#b4232a
shopping-cart
```

`<version>` es el número que aparece en las URL de assets de `home.html`. En un navegador ves el nuevo color de acento y el icono de carrito en el encabezado.

## 7. Deshaz el tutorial

Omite este paso si te quedas con el tema. Para devolver la tienda a su estado, reactiva OBSIDIAN, elimina el tema y regenera el contrato:

```bash
bin/magento config:set design/theme/theme_id 6
rm -rf app/design/frontend/Acme/child
bin/magento mage-obsidian:frontend:config --generate
bin/magento cache:flush
```

Antes de cualquier `rm` en un proyecto que monta carpetas en un contenedor, confirma que la ruta no es un montaje. En zento, `zento cli cat /proc/self/mountinfo | grep /var/www/html` los lista. `app/design/frontend/Acme` no debe aparecer.

`theme:uninstall` no elimina un tema que no se instaló con Composer, así que su fila queda en la tabla `theme`. Cuando nada la referencie (revisa `design_config_grid_flat` y `core_config_data`), elimínala:

```sql
DELETE FROM theme WHERE theme_path = 'Acme/child';
```

La home responde `200` y las islas de OBSIDIAN vuelven.

## Siguientes pasos

- [Configuración del tema](../guides/themes/configuration.md) y [CSS](../guides/themes/css.md): los archivos que puede incluir un tema.
- [Componentes](../guides/themes/components.md): scripts y componentes Vue en un tema.
