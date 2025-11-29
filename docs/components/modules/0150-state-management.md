{% raw %}
# Shared State (Pinia)

Each Vue island is its own app, but they can share reactive state through a single page-wide [Pinia](https://pinia.vuejs.org) instance. This is **opt-in by design**: a component that needs no global state pulls in nothing — Pinia is never installed by the island bootstrap, so pages and components without a store ship no Pinia at all.

A store module activates the shared instance on import (via `ensureSharedPinia()`), and because every store resolves against the same active Pinia, any islands that import it share state. Native ESM, pay-per-use.

> **Requirement:** stores import `pinia`, so the theme must expose it in `exposeNpmPackages` (see [JS Configuration](0060-js-configuration.md)). If a store is imported without Pinia exposed, the build fails loudly.

---

## Authoring a shared store

Call `ensureSharedPinia()` at the top of your store module, then define stores as usual:

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

Two different islands — say a header cart button and a cart drawer — that both `import { useUiStore }` now read and write the same state.

## The customer-data bridge

`useCustomerData` is a ready-made store that mirrors Magento's private content (the `customer-data` sections: `cart`, `customer`, `wishlist`, `compare-products`, …) into reactive state:

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

It is **read-mostly**: Magento's native `customer-data.js` stays the owner of the canonical store (`localStorage['mage-cache-storage']`) and the `/customer/section/load/` endpoint. The bridge reads that cache, re-syncs when Magento broadcasts an update, and exposes `reload()` for an explicit refresh — so it never breaks Full Page Cache.

| Member | Purpose |
|---|---|
| `sections` | Reactive map of all sections. |
| `section(name)` | A single section, or `null`. |
| `sync()` | Re-read the canonical store (called automatically on Magento updates). |
| `reload(names = [], { force })` | Fetch sections from `/customer/section/load/` and merge. |

## How it stays FPC-safe

Magento serves cached pages and loads private content client-side after render (via `/customer/section/load/`, a never-cached endpoint), so per-user data is never baked into the cached HTML. The bridge observes that flow instead of fighting it: it reads `mage-cache-storage`, subscribes to Magento's update broadcasts, and only the explicit `reload()` ever hits the network.

## Next Steps

- [JS Configuration](0060-js-configuration.md) — exposing npm packages like `pinia` to the bundle.
- [Vue Islands](0105-vue-islands.md) — the per-island app model this state layer spans.
{% endraw %}
