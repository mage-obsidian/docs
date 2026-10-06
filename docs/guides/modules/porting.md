# Port a Luma extension

{{ verified('porting') }}

A Luma extension has three parts the new frontend does not read: a `.phtml` template, a RequireJS/KnockoutJS script and LESS. Porting it means replacing each with its counterpart and telling the framework the module takes part. This guide does it for a fictional module, `Acme_Badge`, that shows a dismissible "New arrival" badge on the home page.

The steps come from a real port: a store module that also needed the compatibility file (it ships static assets, and without the declaration they are not deployed under an Obsidian theme) and a plugin on a `MageObsidian\Catalog` ViewModel. `Acme_Badge` reproduces the same moves with code written for this page.

## The Luma module

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

`badge.phtml` mounted a jQuery widget through `data-mage-init`:

```php
<p class="acme-badge" data-mage-init='{"Acme_Badge/js/badge": {"label": "<?= $block->escapeHtmlAttr(__('New arrival')) ?>"}}'></p>
```

`requirejs-config.js` mapped the widget and `badge.js` defined it with `define(['jquery'], …)`. None of that runs under {{ config.extra.components_name }}: there is no RequireJS and no Knockout.

## Step 1: declare the compatibility

A module that does not declare itself is ignored: its layout, blocks and frontend configuration never reach the page. Add `etc/mage_obsidian_compatibility.xml`:

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
    <features>
        <compatibility>true</compatibility>
    </features>
</config>
```

Add `MageObsidian_ModernFrontend` to the `<sequence>` of `etc/module.xml`. The file and its optional `universal` flag are covered in [Make a module compatible](compatibility.md). Do this even for a module with no JavaScript: it also decides whether the module's static assets are deployed.

## Step 2: replace the `.phtml`

The layout keeps working, but point the block at a template your theme engine renders and use the framework block class, which provides the island helpers. With the Twig module installed:

{% raw %}
```xml
<block class="MageObsidian\ModernFrontend\Block\Template" name="acme.badge"
       template="Acme_Badge::badge.twig"/>
```

```twig
{{ render_vue('Acme_Badge::Badge', { label: __('New arrival'), dismissLabel: __('Dismiss') }) }}
```
{% endraw %}

Without Twig, keep a `.phtml` and call `$block->renderVueComponent('Acme_Badge::Badge', $props)`; see [Templates (.phtml)](phtml.md). Props are plain data: pass already translated strings, not a `data-mage-init` JSON blob.

## Step 3: move the script to a Vue island

The widget's behavior becomes a component in `view/frontend/web/components/Badge.vue`:

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

Use an island when the script drives markup. When it is plain logic with no markup, write an ESM module under `view/frontend/web/js/` instead and import it by `Vendor_Module::` specifier; see [JavaScript & imports](javascript.md). Never import across modules with a relative path: it bypasses theme inheritance.

Delete `requirejs-config.js` and the widget file. Knockout `data-bind` templates have no counterpart: rebuild them as component templates.

Plugins on a core block or ViewModel carry over only when the target exists in the new storefront. Re-point the `<plugin>` at the matching `MageObsidian\*` ViewModel, in `etc/frontend/di.xml`.

## Step 4: styles with Tailwind

Replace the LESS with `view/frontend/web/css/module.extend.css`. Tailwind 4 is CSS-first, so utilities are applied with `@apply`:

```css
.acme-badge {
    @apply inline-flex items-center gap-2 rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-900;
}

.acme-badge button {
    @apply cursor-pointer leading-none;
}
```

The module's CSS is imported before the theme's, so a theme can still override your tokens. More in [Configuration](configuration.md).

## Step 5: generate the contract and build

```bash
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
```

Then reload PHP-FPM. The contract is loaded with `require`, and when `opcache.validate_timestamps` is off (the usual production setting, and the default in the local stack) the web workers keep serving the copy they cached. The symptom is a theme or module that the CLI sees and the page does not: layout from `MageObsidian_*` modules goes missing. Restart the PHP service your web server talks to (`zento compose restart php php-noxdebug` in the local stack), then build and flush:

```bash
pnpm build:theme MageObsidian/default
bin/magento cache:flush
```

Run `pnpm` from the `vite/` directory. The contract's layout is also kept in the layout cache, so the flush matters.

## Step 6: check it

Fetch the page and look for the island marker:

```bash
curl -s https://your-store.test/ | grep -c 'data-mage-island'
```

On the verification run the home went from 9 to 10 islands, and the new marker pointed at `generated/Acme_Badge/components/Badge.js`, which answered 200. The compiled stylesheet held the `.acme-badge` rules.

Final checklist:

- [ ] `etc/mage_obsidian_compatibility.xml` exists and `MageObsidian_ModernFrontend` is in the module sequence.
- [ ] `setup:upgrade` ran and `module:status` lists the module as enabled.
- [ ] `mage-obsidian:frontend:config --generate` ran, and PHP-FPM was reloaded afterwards.
- [ ] The theme was rebuilt and `cache:flush` ran.
- [ ] The page contains a `data-mage-island` marker for your component and its JavaScript returns 200.
- [ ] No `requirejs-config.js`, `data-mage-init`, `x-magento-init` or `.less` is left in the module.

If a step does not behave, the [contract reference](../../reference/contract.md) describes what `--generate` writes and what the build validates. Islands, their strategies and hydration are in [Vue Islands](../vue/islands.md).
