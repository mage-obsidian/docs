---
description: Create a child theme of OBSIDIAN, change a color token, override a Vue component and see both on the storefront.
---

# Your first child theme

{{ verified('storefront') }}

You will create `Acme/child`, a theme that inherits from `MageObsidian/default` (OBSIDIAN), change its accent color, override one Vue component, build it and see both changes on the home page. Every command and output below comes from running this tutorial end to end on a store, and the store was put back as it was afterwards.

Commands are shown as `bin/magento …` from the Magento root. On a zento project, prefix them with `zento magento` and run them from the project root.

## 1. Generate the theme

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

`theme.xml` now declares `<parent>MageObsidian/default</parent>`, and `etc/mage_obsidian_compatibility.xml` opts the theme into the frontend build. The options are in [Scaffolding](scaffolding.md#generate-a-theme).

## 2. Activate it

Magento registers a new theme during `setup:upgrade`:

```bash
bin/magento setup:upgrade --keep-generated
```

```text
Upgrade completed successfully.
```

Then open **Content → Design → Configuration**, edit the row for your store view or the global row, and pick **Child** as the applied theme. The same setting from the command line is `design/theme/theme_id`, set to the id the `theme` table gave `Acme/child` (7 on the store used here):

```bash
bin/magento config:set design/theme/theme_id 7
```

```text
Value was saved.
```

## 3. Change a color token

OBSIDIAN defines its colors as Tailwind 4 tokens in its own `theme.source.css`, among them `--color-accent: #2f6e66`. The child's source is loaded after the parent's, so redefining the token in the child wins. Edit `app/design/frontend/Acme/child/web/css/theme.source.css`:

```css
@import "tailwindcss";

@theme {
  --color-accent: #b4232a;
}
```

## 4. Override a Vue component

A theme overrides a module's file by recreating its path under a folder named after the module. The header cart badge is `MageObsidian_Storefront::cart/CartCount`; to replace it, create:

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

This copy shows a cart icon instead of the shopping bag. Cross-module imports use `Vendor_Module::path`, never a relative path, so the override stays reachable for children of your theme.

## 5. Regenerate the contract and build

```bash
bin/magento mage-obsidian:frontend:config --generate
```

```text
 ===========================================================
  /var/www/html/app/etc/mage_obsidian_frontend_modules.php
  /var/www/html/app/etc/mage_obsidian_frontend_modules.json
 ===========================================================
```

Check that the contract lists the theme:

```bash
bin/magento mage-obsidian:frontend:config --show --themes
```

```text
  Acme/child                /var/www/html/app/design/frontend/Acme/child
```

Then build it, from the `vite/` folder of the Magento root:

```bash
pnpm build:theme Acme/child
```

```text
✓ built in 799ms
✓ Acme/child built
```

Flush the cache so the store picks up the new theme:

```bash
bin/magento cache:flush
```

## 6. See it on the home page

```bash
curl -sk -o home.html -w "%{http_code}\n" https://your-store.test/
```

```text
200
```

The page now loads its assets from the child:

```bash
grep -o 'frontend/[A-Za-z]*/[a-z]*' home.html | sort | uniq -c
```

```text
     20 frontend/Acme/child
```

Fetch the built files and look for both changes:

```bash
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/css/style.css | grep -o -- '--color-accent:[^;]*' | head -1
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/MageObsidian_Storefront/components/cart/CartCount.js | grep -o 'shopping-[a-z]*' | sort -u
```

```text
--color-accent:#b4232a
shopping-cart
```

`<version>` is the number in the asset URLs of `home.html`. In a browser you see the new accent color and the cart icon in the header.

## 7. Undo the tutorial

Skip this if you are keeping the theme. To put the store back, reactivate OBSIDIAN, remove the theme and regenerate the contract:

```bash
bin/magento config:set design/theme/theme_id 6
rm -rf app/design/frontend/Acme/child
bin/magento mage-obsidian:frontend:config --generate
bin/magento cache:flush
```

Before any `rm` on a project that mounts folders into a container, confirm the path is not a mount. On zento, `zento cli cat /proc/self/mountinfo | grep /var/www/html` lists them. `app/design/frontend/Acme` must not appear.

`theme:uninstall` does not remove a theme that was not installed with Composer, so its row stays in the `theme` table. When nothing references it (check `design_config_grid_flat` and `core_config_data`), delete it:

```sql
DELETE FROM theme WHERE theme_path = 'Acme/child';
```

The home page returns `200` and OBSIDIAN's islands are back.

## Where to go next

- [Theme configuration](../guides/themes/configuration.md) and [CSS](../guides/themes/css.md): the files a theme can ship.
- [Components](../guides/themes/components.md): scripts and Vue components in a theme.
