# Vue Islands

In **{{ config.extra.components_name }}**, every Vue component rendered from a `.phtml` (or `.twig`) template is mounted as an **island**: a self-contained Vue app attached to a single marker in the page, hydrated independently from the rest of the document.

The `.phtml` bridge method [`renderVueComponent`](0090-phtml-configuration.md#2-rendering-vue-components) does not emit an inline mount script anymore. It emits an inert marker that a single page-level bootstrap discovers and mounts — by default only when the marker scrolls into view.

Here it is on a real product page over a throttled connection: the server-rendered HTML paints first — readable before a single byte of Vue executes — then the islands hydrate as their chunks arrive:

<video autoplay loop muted playsinline style="max-width:100%;border-radius:8px" src="/assets/islands-hydration.mp4"></video>

---

## Why Islands

- **One bootstrap per page, not one per component.** The Vue runtime and the i18n plugin are imported **once** and shared by every island, instead of each `renderVueComponent` call re-importing them.
- **Zero cost when there are no islands.** The bootstrap checks the page for markers first; if there are none, it returns before importing Vue or the dictionary. A page without islands ships no Vue at all.
- **Lazy by default.** Below-the-fold components do not hydrate — and their component module is not even fetched — until they enter the viewport.
- **Isolation is preserved.** Each island is still its own Vue app, so one component crashing or re-rendering never touches another.

---

## How It Works

### 1. The marker (server side)

`renderVueComponent` emits a single `<div>` carrying everything the browser needs as data attributes:

```html
<div data-mage-island
     data-component="/static/.../generated/Vendor_Module/components/NavBar.js"
     data-props="{&quot;title&quot;:&quot;Welcome&quot;}"
     data-strategy="visible"></div>
```

| Attribute | Meaning |
|---|---|
| `data-mage-island` | Marks the element so the bootstrap can discover it. |
| `data-component` | URL of the compiled component module to import. |
| `data-props` | Attribute-safe JSON of the props. The browser decodes the entities back to JSON before `JSON.parse`. |
| `data-strategy` | `visible` (lazy) or `eager`. |

Props are encoded for the attribute by the `PropsEncoder` service: it `json_encode`s the props and entity-escapes `<`, `>`, `&`, `"` and `'` so the value cannot break out of the attribute. An un-encodable value (malformed UTF-8, a resource, `NAN`/`INF`) throws instead of emitting a broken marker.

### 2. The page bootstrap (browser side)

A single module script is injected once per page, just before `</body>`, by the `IslandsRuntime` block (wired in the module's `default.xml` layout). On load it:

1. Queries the document for `[data-mage-island]`. **If there are none, it stops here** — Vue is never imported.
2. Otherwise it lazily imports the Vue runtime and the i18n plugin (once).
3. Hands the markers to the framework's hydration runtime, providing the concrete browser behavior: dynamic component import, app creation, i18n wiring, and an `IntersectionObserver` for the `visible` strategy.

### 3. Hydration strategies

The strategy comes straight from the `$eager` argument of `renderVueComponent`:

- **`visible` (default)** — the marker is registered with an `IntersectionObserver`; the component module is fetched and the island is mounted the first time it enters the viewport. Ideal for below-the-fold content.
- **`eager`** — the island mounts immediately on page load, without waiting for the viewport. Use it for above-the-fold components where any delay would be visible.

```php
<?= $block->renderVueComponent('Vendor_Module::Hero', $props, true) ?>  // eager
<?= $block->renderVueComponent('Vendor_Module::Reviews', $props) ?>     // visible (default)
```

Hydration is **idempotent**: the first mount claims the element, so a second observer callback for the same marker is a no-op and never double-mounts.

---

## Sharing Logic Across the Engine

The discovery/hydration logic lives in the JS build engine (`mage-obsidian/runtime/islands.ts`) and is fully dependency-injected — no direct reference to the DOM, a bundler, or Vue — so it is unit-tested in Node. The concrete wiring (the actual dynamic `import`, `createApp`, `app.use(i18n)`, and the observer) lives in the module's `web/js/islands.js`. You normally never touch either: you call `renderVueComponent` and the island machinery does the rest.

---

## Key Notes

- A page with no islands loads no Vue — keep that property in mind when deciding between an island and the [inline Vue pattern](0100-phtml-vue-integration.md).
- Default to `visible`; reserve `eager` for above-the-fold components.
- Props must be JSON-encodable. Pass plain data (scalars, arrays, maps), not objects with resources or non-UTF-8 strings.
- The i18n dictionary is Magento's native per-locale `js-translation.json`, so islands share the same translations as the rest of the storefront.

---

## Next Steps

- See [Using JavaScript and Vue Components in `.phtml` Templates](0090-phtml-configuration.md) for the full `renderVueComponent` reference.
- The same island can be mounted from a `.twig` template via the `render_vue` helper — see the [Twig Engine](../../twig/index.md).
