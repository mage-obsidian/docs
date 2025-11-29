{% raw %}
# Estado compartido (Pinia)

Cada isla Vue es su propia app, pero pueden compartir estado reactivo a través de una única instancia de [Pinia](https://pinia.vuejs.org) a nivel de página. Esto es **opt-in por diseño**: un componente que no necesita estado global no carga nada —el bootstrap de islas nunca instala Pinia, así que las páginas y los componentes sin store no envían Pinia en absoluto.

Un módulo de store activa la instancia compartida al importarse (vía `ensureSharedPinia()`), y como todos los stores resuelven contra la misma Pinia activa, cualquier isla que lo importe comparte el estado. ESM nativo, pago por uso.

> **Requisito:** los stores importan `pinia`, así que el tema debe exponerla en `exposeNpmPackages` (ver [Configuración de JS](0060-js-configuration.md)). Si se importa un store sin Pinia expuesta, el build falla de forma ruidosa.

---

## Crear un store compartido

Llama a `ensureSharedPinia()` al inicio de tu módulo de store y define stores como siempre:

```js
import { defineStore } from 'pinia';
import { ensureSharedPinia } from 'MageObsidian_ModernFrontend::js/store';

ensureSharedPinia();

export const useUiStore = defineStore('ui', {
    state: () => ({ cartDrawerOpen: false }),
    actions: {
        toggleCartDrawer() {
            this.cartDrawerOpen = !this.cartDrawerOpen;
        },
    },
});
```

Dos islas distintas —por ejemplo un botón de carrito en el header y un cajón de carrito— que ambas hagan `import { useUiStore }` leen y escriben ahora el mismo estado.

## El puente customer-data

`useCustomerData` es un store listo que espeja el contenido privado de Magento (las secciones `customer-data`: `cart`, `customer`, `wishlist`, `compare-products`, …) en estado reactivo:

```vue
<script setup>
import { computed } from 'vue';
import { useCustomerData } from 'MageObsidian_ModernFrontend::js/customer-data';

const customerData = useCustomerData();
const cartCount = computed(() => customerData.section('cart')?.summary_count ?? 0);
</script>

<template>
    <span class="cart-count">{{ cartCount }}</span>
</template>
```

Es **read-mostly**: el `customer-data.js` nativo de Magento sigue siendo el dueño del store canónico (`localStorage['mage-cache-storage']`) y del endpoint `/customer/section/load/`. El puente lee esa caché, se re-sincroniza cuando Magento emite una actualización, y expone `reload()` para un refresco explícito —así nunca rompe el Full Page Cache.

| Miembro | Propósito |
|---|---|
| `sections` | Mapa reactivo de todas las secciones. |
| `section(name)` | Una sección, o `null`. |
| `sync()` | Re-lee el store canónico (se llama solo ante actualizaciones de Magento). |
| `reload(names = [], { force })` | Trae secciones de `/customer/section/load/` y las fusiona. |

## Por qué respeta el FPC

Magento sirve páginas cacheadas y carga el contenido privado en el cliente tras el render (vía `/customer/section/load/`, un endpoint no cacheado), así que los datos por usuario nunca quedan horneados en el HTML cacheado. El puente observa ese flujo en lugar de pelearse con él: lee `mage-cache-storage`, se suscribe a las emisiones de Magento, y solo el `reload()` explícito toca la red.

## Próximos pasos

- [Configuración de JS](0060-js-configuration.md) — exponer paquetes npm como `pinia` al bundle.
- [Islas Vue](0105-vue-islands.md) — el modelo de app por isla que abarca esta capa de estado.
{% endraw %}
