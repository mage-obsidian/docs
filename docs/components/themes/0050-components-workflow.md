# Creating Scripts and Components

In **{{ config.extra.components_name }}**, themes carry their own JavaScript and Vue components, under the theme directory:

```
app/design/frontend/Vendor/Theme/web/js          # plain scripts (.ts / .js)
app/design/frontend/Vendor/Theme/web/components  # Vue single-file components
```

Files under a module use `view/frontend/web/` instead. Everything below works the same either way — the only difference is the namespace you refer to them by: `Theme::` for the theme's own files, `Vendor_Module::` for a module's.

---

## Workflow

### 1. Scripts in `web/js`

A script is a module, not a bundle entry. It is loaded once, does its work and exports whatever the rest needs.

```ts
// app/design/frontend/Vendor/Theme/web/js/greeting.ts
export function greetUser(name: string): void {
    console.log(`Hello, ${name}!`);
}
```

Load it from a template with the `script()` helper, which emits a `<script type="module">` pointing at the built file:

{% raw %}
```twig
{{ script('Theme::js/greeting') }}
```
{% endraw %}

Import it from other JS with the framework's specifier — **never a relative path**:

```ts
import { greetUser } from "Theme::js/greeting";
```

The specifier is what makes theme inheritance work: a child theme that ships `web/js/greeting.ts` transparently replaces the parent's for everyone who imports it. A relative path resolves to one specific file on disk and skips that entirely. A typo fails the build with suggestions rather than shipping broken.

### 2. Vue components in `web/components`

Components are single-file components using **`<script setup>`**. TypeScript is the default (`lang="ts"`).

{% raw %}
```vue
<!-- app/design/frontend/Vendor/Theme/web/components/CartSummary.vue -->
<script setup lang="ts">
import { computed } from "vue";

interface Item {
    price: number;
}

const props = defineProps<{ items: Item[] }>();

const total = computed(() => props.items.reduce((sum, item) => sum + item.price, 0));
</script>

<template>
    <div>
        <h2>Total: {{ total }}</h2>
    </div>
</template>
```
{% endraw %}

Mount it from a template as an **island** — a marker the runtime hydrates, not a page-wide app:

{% raw %}
```twig
{{ render_vue('Theme::components/CartSummary', { items: items }) }}
```
{% endraw %}

`render_vue(name, props, eager, serverHtml, hydrate)`:

| Argument | Meaning |
|---|---|
| `name` | `Theme::components/X` or `Vendor_Module::components/X` |
| `props` | Passed to the component as its props |
| `eager` | `true` mounts immediately; the default waits until the island scrolls into view |
| `serverHtml` | Markup for the component's initial state, so the island has something to show before Vue arrives |
| `hydrate` | With `serverHtml`, adopt that markup instead of replacing it — no layout shift |

Generate `serverHtml` with the `mage-obsidian:island-ssr` bin (see [Vue islands](../modules/0105-vue-islands.md)). An eager island that replaces its container shifts the page on mount; `bin/magento mage-obsidian:frontend:doctor` reports every one that does.

---

## Templates: Twig or phtml

With the optional Twig module installed, templates are `.twig` and the helpers above are Twig functions. They are declared `is_safe => html`, so **they never need `|raw`**.

Without it, the same capabilities are ViewModel calls from `.phtml`:

```php
<?= $block->renderVueComponent('Theme::components/CartSummary', ['items' => $items]) ?>
<script type="module" src="<?= $escaper->escapeUrl($block->getViteFileUrl('Theme::js/greeting')) ?>"></script>
```

New themes are expected to be written in Twig; `.phtml` remains supported for compatibility and for the rare block whose PHP the theme has to keep.

---

## Guidelines

1. **Location.** Scripts in `web/js`, components in `web/components`. Under a module, the same two directories inside `view/frontend/web/`.
2. **Naming.** kebab-case for `web/js`, PascalCase for components.
3. **Imports.** Always `Theme::` / `Vendor_Module::`. Relative paths across a module or theme boundary break inheritance.
4. **Composition API only.** `<script setup>`; the Options API is not used anywhere in the shipped storefront.
5. **Dynamic imports** work with the same specifiers, and are how an island's code stays out of the critical path:
   ```ts
   const { greetUser } = await import("Theme::js/greeting");
   ```
6. **Vite processes both directories** — bundled, tree-shaken, and fingerprinted into `web/generated`.

---

## Adding to an existing page

A component that has to appear inside a block someone else owns does not need that block edited. Declare a child block in layout XML and render it where the parent template calls `child_html`:

```xml
<referenceBlock name="product.info.main">
    <block class="MageObsidian\ModernFrontend\Block\Template"
           name="vendor.cart.summary" as="cart_summary"
           template="Vendor_Module::cart/summary.twig"/>
</referenceBlock>
```

If the parent template has no hook for it, an **interceptor** can wrap the JS instead, without editing the module that owns it.
