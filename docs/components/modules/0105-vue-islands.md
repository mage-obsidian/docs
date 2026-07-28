# Vue Islands

In **{{ config.extra.components_name }}**, every Vue component rendered from a `.phtml` (or `.twig`) template is mounted as an **island**: a self-contained Vue app attached to a single marker in the page, hydrated independently from the rest of the document.

The `.phtml` bridge method [`renderVueComponent`](0090-phtml-configuration.md#2-rendering-vue-components) does not emit an inline mount script. It emits a marker that a single page-level bootstrap discovers and mounts — by default only when the marker scrolls into view.

Here it is on a real product page over a throttled connection: the server-rendered HTML paints first — readable before a single byte of Vue executes — then the islands hydrate as their chunks arrive:

<video autoplay loop muted playsinline style="max-width:100%;border-radius:8px" src="/assets/islands-hydration.mp4"></video>

---

## Why Islands

- **One bootstrap per page, not one per component.** The Vue runtime and the i18n plugin are imported **once** and shared by every island, instead of each `renderVueComponent` call re-importing them.
- **Zero cost when there are no islands.** The bootstrap checks the page for markers first; if there are none, it returns before importing Vue or the dictionary. A page without islands ships no Vue at all.
- **Lazy by default.** Below-the-fold components do not hydrate — and their component module is not even fetched — until they enter the viewport.
- **Isolation is preserved.** Each island is still its own Vue app, so one component crashing or re-rendering never touches another.

---

## The Two Modes

An island can either **own** its markup or **adopt** markup the server rendered. Which one you pick decides whether the component appears out of nowhere or is simply there from the first paint.

| Mode | Who owns the markup | Use it for |
|---|---|---|
| **mount** (default) | the component | UI that does not exist without JS: modals, drawers, toasts, autocomplete. Keep it lazy, or outside the document flow. |
| **hydrate** | the template, adopted by the component | anything above the fold and in the flow: buy boxes, navigation, forms. |

### mount

The marker is empty (or carries a placeholder), and Vue renders the component into it, replacing whatever was there:

```php
<?= $block->renderVueComponent('Vendor_Module::Toast', $props, true) ?>
```

This is right when the component has no meaningful server-side state — a toast host has nothing to show until something happens. It is wrong for anything occupying space in the page: the container is empty when the document paints and grows when the chunk arrives, pushing everything below it down.

### hydrate

The template renders the component's initial state, and Vue attaches to that DOM instead of recreating it:

```php
<?= $block->renderVueComponent('Vendor_Module::BuyBox', $props, true, $serverHtml, true) ?>
```

Nothing moves, because nothing is inserted — the markup was already on screen, and it stays readable if the chunk is slow or never arrives.

That is not the same as the page *working* without JavaScript. Whether it does depends on the markup: the product card's add-to-cart is a real `<form>` that posts to `checkout/cart/add`, so it works either way; the configurable island's form has no action and its swatches are buttons, so it still ships a `<noscript>`. Hydration preserves whatever the server rendered — it does not make it functional.

Hydration is **opt-in** through that fifth argument, and deliberately so. Vue adopts server markup only if it matches what the component would render; markup that merely approximates it fails to match and gets re-rendered, which is the exact reflow this mechanism exists to avoid. Passing markup without `$hydrate` keeps it a placeholder that Vue clears on mount — safe, and no worse than an empty container.

---

## Writing the Server Markup

The initial state has to match what the component renders. Structure is what counts: **element sequence, fragment anchors and text**. Classes, styles and attributes are compared semantically, so class order and style formatting are free.

### Generating it

Vue's SSR output marks a `v-for` with `<!--[-->` / `<!--]-->` and a falsy `v-if` with `<!---->`, because a fragment owns no element of its own and hydration needs to know where it starts and ends. Nobody should transcribe that by hand, so the engine renders the component for you:

```bash
mage-obsidian:island-ssr --component path/to/BuyBox.vue --state ./state.mjs
```

- `--state` is a `.mjs` (or `.json`) with the values the template reads. A `.mjs` can carry the methods the template calls and a `components` map for child components; run it from the Vite harness so its imports resolve.
- `--props` passes the island's props as JSON.

Only the component's `<template>` is used — its `<script setup>` never runs — so this needs no bundler and no browser. Nothing about it ships to a storefront.

### The anchors

Paste the generated markup, replace the values with template variables, and express the anchors with the helpers instead of hardcoding HTML comments:

{% raw %}
```twig
{% apply island_list %}
    {% for option in group.options %}<button …>{{ option.label }}</button>{% endfor %}
{% endapply %}

{% apply island_if(oldPrice) %}<span class="regular">{{ oldPrice }}</span>{% endapply %}
```
{% endraw %}

| Helper | Mirrors | Emits |
|---|---|---|
| `island_list` | `v-for` | `<!--[-->` … `<!--]-->` |
| `island_if(cond)` | `v-if` with no `v-else` | the markup, or `<!---->` |

A `v-if`/`v-else` needs no helper: Vue renders the taken branch with no anchor at all, so a plain {% raw %}`{% if %}`{% endraw %} matches. In `.phtml`, the equivalents are `$block->islandList()` and `$block->islandIf()`.

Indentation is handled for you — `renderVueComponent` strips the whitespace between tags, which Vue's compiler does not expect and which would otherwise fail to hydrate on every island.

---

## How It Works

### 1. The marker (server side)

```html
<div data-mage-island
     data-component="/static/.../generated/Vendor_Module/components/NavBar.js"
     data-props="{&quot;title&quot;:&quot;Welcome&quot;}"
     data-strategy="visible"
     data-hydrate>…server markup…</div>
```

| Attribute | Meaning |
|---|---|
| `data-mage-island` | Marks the element so the bootstrap can discover it. |
| `data-component` | URL of the compiled component module to import. |
| `data-props` | Attribute-safe JSON of the props. The browser decodes the entities back to JSON before `JSON.parse`. |
| `data-strategy` | `visible` (lazy) or `eager`. |
| `data-hydrate` | Present when the contents are the component's initial state, not a placeholder. |

Props are encoded by the `PropsEncoder` service: it `json_encode`s them and entity-escapes `<`, `>`, `&`, `"` and `'` so the value cannot break out of the attribute. An un-encodable value (malformed UTF-8, a resource, `NAN`/`INF`) throws instead of emitting a broken marker.

### 2. The page bootstrap (browser side)

A single module script is injected once per page, just before `</body>`, by the `IslandsRuntime` block. On load it:

1. Queries the document for `[data-mage-island]`. **If there are none, it stops here** — Vue is never imported.
2. Otherwise it lazily imports the Vue runtime and the i18n plugin (once).
3. Hands the markers to the framework's hydration runtime, providing the concrete browser behavior: dynamic component import, app creation, i18n wiring, and an `IntersectionObserver` for the `visible` strategy.

Apps are created with `createSSRApp`, so a marker with `data-hydrate` is adopted and one without it is cleared and mounted. Vue picks the path from the container itself, which is why nothing here needs a flag.

### 3. Hydration strategies

The strategy comes from the `$eager` argument:

- **`visible` (default)** — the marker is registered with an `IntersectionObserver`; the component module is fetched and the island is mounted the first time it enters the viewport.
- **`eager`** — the island mounts immediately on page load. Use it for above-the-fold components, and give it server markup to hydrate.

Hydration is **idempotent**: the first mount claims the element, so a second observer callback for the same marker is a no-op.

---

## Verifying It

### The drift detector

The server markup restates what the component's `<template>` renders, and nothing stops the two from diverging — worse, a class that only exists on the client is reported by Vue and then dropped, so it fails invisibly. That is what the runtime check is for.

A hydration that matched leaves the DOM untouched: Vue compares `class` as a set and `style` as a map, and a difference there only logs. Anything it cannot adopt goes through `handleMismatch`, which removes the server node and patches the right one in. So the markup having changed **is** the mismatch, exactly, with no fixtures to keep up to date. In a development build the bootstrap snapshots each hydration target, mounts, compares, and reports the first differing byte:

```
[MageObsidian] Island "MageObsidian_Catalog::catalog/ProductForm" hydrated with a mismatch — Vue replaced the server markup.
server: <button class="pdp__swatch pdp__swatch--text">
client: <button class="pdp__swatch">
                       ^ first difference at offset 412
```

A subtree marked with Vue's `data-allow-mismatch` is cut from both sides, so a value the server cannot predict is exempted rather than reported on every page load.

The same pass reports an **eager island that changed size on mount**, which is the shift this whole mechanism exists to prevent. Size is the honest test: an empty container that occupies no space — a drawer, a toast host — moves nothing and is not a defect.

Both are development-only. They are gated on `__MAGE_OBSIDIAN_DEV__`, which the Vite config defines from `NODE_ENV` — **not** `import.meta.env.DEV`, which is false in any `vite build` because Vite always builds in production mode.

### At the command line

**`bin/magento mage-obsidian:frontend:doctor`** reports eager islands that still replace their container, across module templates and theme overrides.

### Do not gate on CLS

A buy box appearing 200 ms after the page paints can score 0.02 — comfortably "good" — while showing a visibly broken page, because the metric weighs the fraction of the viewport that moved. Measure what actually matters: whether any island changes size after the first paint.

---

## Sharing Logic Across the Engine

The discovery/hydration logic lives in the JS build engine (`mage-obsidian/runtime/islands.ts`) and is fully dependency-injected — no direct reference to the DOM, a bundler, or Vue — so it is unit-tested in Node. The concrete wiring (the actual dynamic `import`, `createSSRApp`, `app.use(i18n)`, and the observer) lives in the module's `web/js/islands.ts`.

---

## Key Notes

- A page with no islands loads no Vue — keep that property in mind when deciding between an island and the [inline Vue pattern](0100-phtml-vue-integration.md).
- Default to `visible`; reserve `eager` for above-the-fold components, and hydrate those.
- Props must be JSON-encodable. Pass plain data (scalars, arrays, maps), not objects with resources or non-UTF-8 strings.
- The i18n dictionary is Magento's native per-locale `js-translation.json`, so islands share the same translations as the rest of the storefront.
- A value the server cannot predict (a generated id, a locale-formatted number) can be exempted with Vue's `data-allow-mismatch` rather than chased.
- **Icons must come from the same source on both sides.** `hero_icon()` emits `<svg><use href>`; a component importing `@heroicons/vue` emits an inline `<path>`. They can never match, so a hydrating component uses the engine's `Icon` component instead, which emits the same `<use>`. Pass the classes to `hero_icon`'s fourth argument as well — a class only the client would have set is reported and then dropped, so it would silently never land.

---

## Next Steps

- See [Using JavaScript and Vue Components in `.phtml` Templates](0090-phtml-configuration.md) for the full `renderVueComponent` reference.
- The same island can be mounted from a `.twig` template via the `render_vue` helper — see the [Twig Engine](../../twig/index.md).
