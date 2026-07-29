# Storefront Events

**{{ config.extra.components_name }}** ports both of Magento's extension points to the browser. They answer different questions, and the difference is the same one it is in PHP:

| | Wraps | Can change what happens | Wired |
|---|---|---|---|
| **Interceptors** | a specific function | yes | at build time, by module |
| **Events** | nothing — something already happened | only through the data it carries | at runtime, by anyone |

Extending a flow from another module should not require knowing which function to wrap. So the flow announces what it did, and anyone can listen.

---

## The convention

Every mutation in the storefront announces itself three times, under a name built from three parts:

```
<domain>_<operation>_<phase>
```

`snake_case`, like Magento's own events. The phases:

| Phase | Meaning | Payload |
|---|---|---|
| `_before` | it is about to happen; an observer may amend or cancel it | `{ …, cancelled: boolean, message?: string }` |
| `_after` | it happened | `{ …, result }` |
| `_failed` | additionally, it did not succeed | `{ …, result }` |

A failed mutation dispatches **both** `_after` and `_failed`: `_after` means "the flow is over", not "the flow worked". Observers that only care about success check `result`.

That convention is not cosmetic — it is the mechanism [loading state is derived from](#the-activity-tracker). A flow that follows it gets synchronised spinners across the whole page without writing a line for them.

Build names with the helper rather than by hand, so a typo is a compile error instead of an event nobody receives:

```ts
import { MutationPhase, mutationEvent } from 'mage-obsidian/runtime/mutationEvent.ts';

mutationEvent('cart', 'add', MutationPhase.Before); // 'cart_add_before'
```

---

## Observing

```js
import events from 'MageObsidian_ModernFrontend::js/events';

events.observe('cart_add_after', (data) => {
    if (data.result.ok) {
        analytics.track('add_to_cart', { product: data.body.get('product') });
    }
});
```

Observers run in `sortOrder` (default `10`, lowest first) and are awaited, so an async one finishes before the next runs. `observe` returns a function that removes it; `observeOnce` removes itself after the first call.

An observer that throws is reported and skipped — a failing analytics hook must never take down an add-to-cart.

```js
events.observe('cart_add_before', (data) => { … }, { name: 'my_module', sortOrder: 5 });
```

### Amending and cancelling

A `_before` observer receives the request that is about to be sent, and the request is whatever it leaves behind:

```js
events.observe('cart_add_before', (data) => {
    data.body.set('qty', String(Number(data.body.get('qty')) * 2));
});
```

Setting `cancelled` stops it entirely. Nothing is sent, and no `_after` or `_failed` follows:

```js
events.observe('cart_add_before', (data) => {
    if (isRestricted(data.body.get('product'))) {
        data.cancelled = true;
        data.message = 'Not available in your region';
    }
});
```

The caller sees `{ ok: false, message }`, so the toast says what happened.

### Sticky events

An event that happens once per page — `page_ready` above all — is remembered. An observer registered *after* it was dispatched is invoked immediately with the payload it missed:

```js
events.observe('page_ready', (data) => {
    console.log(`${data.islands} islands on ${data.url}`);
});
```

This is what makes a deferred tag-manager snippet workable: it cannot control whether it loads before or after the bootstrap, and with sticky events it does not have to. `events.sticky(name)` reads the remembered payload directly.

Only mark one-per-page events as sticky. A sticky `cart_add_after` would fire on every future observer with a stale add.

---

## From outside the bundle

Every dispatch is mirrored as a `CustomEvent` on `window`, named `obsidian:<event>`, so a tag manager or an inline snippet needs no import:

```html
<script>
    window.addEventListener('obsidian:cart_add_after', (event) => {
        dataLayer.push({ event: 'add_to_cart', ok: event.detail.result.ok });
    });
</script>
```

A DOM listener **cannot amend the data** — it runs after the observers, on the result. A module that wants to change what happens registers a real observer.

The mirror is skippable per dispatch for high-frequency events, where allocating a `CustomEvent` per keystroke buys nothing:

```ts
events.dispatch(SEARCH_QUERY_CHANGE_EVENT, { query }, { mirror: false });
```

The DOM mirror is also **not sticky**: a `window` listener registered after a sticky dispatch does not receive it. Out-of-bundle code that needs the replay reads `window.__MAGE_OBSIDIAN_EVENTS__.sticky('page_ready')`.

---

## Runtime lifecycle

The runtime itself announces what it is doing, so profiling and third-party integration need no patched internals.

| Event | Payload | When |
|---|---|---|
| `island_mount_before` | `{ component, strategy, element }` | before an island's module is imported |
| `island_mount_after` | `+ durationMs` | after it mounted |
| `island_mount_failed` | `+ error` | its import or mount threw |
| `page_ready` *(sticky)* | `{ url, islands }` | the bootstrap finished discovering markers |
| `page_hidden` / `page_visible` | `{ url }` | `visibilitychange` — the cue to pause polling and timers |
| `page_leave` | `{ url, persisted }` | `pagehide`; `persisted` means it went into the back/forward cache |
| `section_reload_before` | `{ names }` | before hitting `/customer/section/load/` |
| `section_reload_after` | `{ names, changed }` | after the merge; `changed` is what actually differed |
| `section_reload_failed` | `{ names }` | the request failed; the previous data is kept |

`durationMs` is the cheapest island profiler there is — no build flag, no extension:

```js
events.observe('island_mount_after', ({ component, durationMs }) => {
    if (durationMs > 50) console.warn(component, durationMs);
});
```

---

## The catalogue

Every domain funnels its mutations through a single function, so events are announced there rather than at each call site.

### Cart — `MageObsidian_Storefront::js/useCart`

| Operation | Events | Emitted by |
|---|---|---|
| `add` | `cart_add_before` / `_after` / `_failed` | `addFromForm`, `addProduct`, `addRaw` |
| `update_qty` | `cart_update_qty_*` | `updateItemQty` |
| `remove_item` | `cart_remove_item_*` | `removeItem` |
| `coupon` | `cart_coupon_*` | the bag page's coupon form |

```ts
interface CartEvent {
    operation: 'add' | 'update_qty' | 'remove_item';
    action: string;      // the endpoint about to be posted to
    body: FormData;      // the request body, form key included
    cancelled: boolean;
    message?: string;
    result?: CartResult; // on _after / _failed only
}
```

`_after` fires once the response **and** the `cart`/`messages` section reload have landed, so an observer reading `section('cart')` sees the new state.

### Wishlist and compare

`wishlist_add_*`, `wishlist_remove_*`, `compare_add_*`, `compare_remove_*` — same `MutationEvent` shape, with `result: boolean`.

### Search — `MageObsidian_Storefront::js/search-events`

| Event | Payload |
|---|---|
| `search_query_change` | `{ query }` — every keystroke, **not mirrored to the DOM** |
| `search_suggest_before` / `_after` / `_failed` | `{ query, url, cancelled, result?: Suggestion[] }` |

### Catalog — `MageObsidian_Catalog::js/catalog-events`

These describe a selection changing, not a request, so they have no phases.

| Event | Payload |
|---|---|
| `product_variant_change` | `{ productId }` — `null` when the selection is incomplete |
| `bundle_selection_change` | `{ selections }` |
| `product_gallery_change` | `{ reset?, large?, label?, tiles? }` |

### Checkout — `MageObsidian_Checkout::js/checkout-events`

| Event | Payload |
|---|---|
| `checkout_step_change` | `{ from, to }` — only on a real move |
| `checkout_estimate_shipping_*` | `CheckoutEvent` |
| `checkout_save_shipping_*` | `CheckoutEvent` |
| `checkout_apply_coupon_*` / `checkout_remove_coupon_*` | `CheckoutEvent` |
| `checkout_place_order_*` | `CheckoutEvent` |

```ts
interface CheckoutEvent {
    operation: CheckoutOperation;
    payload?: Record<string, unknown>;
    cancelled: boolean;
    message?: string;
    result?: unknown;
}
```

### UI

| Event | Payload | Notes |
|---|---|---|
| `notification_add` | `{ message, tone }` | `tone` is `success`, `error` or `warning`; the toast host observes it |
| `navigation_start` | `{ from, to, kind, trigger }` | a cross-document view transition is starting |

`navigation_start` is announced, not negotiated: the browser's `pageswap` cannot await, so setting `cancelled` on it does nothing.

Two legacy `CustomEvent` names are still dispatched alongside their bus events — `obsidian:toast` and `obsidian:variant-image` — so snippets written against them keep working.

---

## The activity tracker

A loading state should not be a local `ref` in the component that started the request. The button that submits and the badge that reflects the result are separate islands that never import each other, and both need to know the same thing.

They ask the bus. The tracker attaches to every dispatch and reads the phase off the name: a `_before` opens the `cart` and `cart_add` scopes, an `_after` or `_failed` closes them.

```vue
<script setup>
import { computed } from 'vue';
import { useActivity } from 'MageObsidian_ModernFrontend::js/activity';

const activity = useActivity();
const syncing = computed(() => activity.isBusy('cart'));
</script>
```

| Member | Purpose |
|---|---|
| `isBusy(scope)` | is anything pending in that scope |
| `pending(scope)` | how many |
| `busy(scope)` | the same as a `ComputedRef`, for a template |

Scopes nest by convention. `cart` is busy for any cart mutation; `cart_remove_item` only for removals — enough to spin the bag icon for everything while a single row shows its own state.

The counter is derived, so it takes care of the cases a hand-written flag gets wrong: a cancelled `_before` closes its scope immediately (no `_after` is coming), concurrent mutations of the same domain nest instead of clearing each other, and a scope opened for more than 15 seconds is released with a warning rather than leaving a spinner turning forever.

**A new domain inherits all of it for free.** Follow the naming convention and the spinners work, with no import and no registration.

---

## Typing your own events

The catalogue is a TypeScript interface the engine declares empty and each module augments, so `observe` and `dispatch` know every event on the page and their payloads:

```ts
import {
    MutationPhase,
    mutationEvent,
    type MutationEvent,
    type MutationEventName,
} from 'mage-obsidian/runtime/mutationEvent.ts';

export const RETURNS_DOMAIN = 'returns';

export const ReturnsOperation = { Request: 'request' } as const;
export type ReturnsOperation = (typeof ReturnsOperation)[keyof typeof ReturnsOperation];

export type ReturnsEvent = MutationEvent<ReturnsOperation, boolean>;
export type ReturnsEventName = MutationEventName<typeof RETURNS_DOMAIN, ReturnsOperation>;

declare module 'mage-obsidian/runtime/eventManager.ts' {
    interface StorefrontEventMap extends Record<ReturnsEventName, ReturnsEvent> {}
}

export const returnsEvent = <Phase extends MutationPhase>(phase: Phase) =>
    mutationEvent(RETURNS_DOMAIN, ReturnsOperation.Request, phase);
```

That declares `returns_request_before`, `_after` and `_failed` at once, each with its payload. Observing one with the wrong shape now fails the type check, and the editor completes the event names.

Importing the module is what activates the augmentation. A module that only observes another's events imports its event file for the types.

An event whose name is not in the map still works — it falls back to `Record<string, unknown>`. Nothing existing breaks; it just gets no help.

---

## Debugging and performance

In a development build the manager traces itself. Every dispatch is logged with its payload, and an observer that takes more than 16 ms — a dropped frame — is named:

```
[MageObsidian] Observer "gtm_add_to_cart" of "cart_add_after" took 41.3ms
and delayed the interaction that dispatched it.
```

`events.debug()` turns the same tracing on in a production build from the console, and `events.observersOf('cart_add_before')` lists who is registered. Both are on `window.__MAGE_OBSIDIAN_EVENTS__`, so the console needs no import.

The cost of an event nobody observes is the hook loop and the mirrored `CustomEvent`. The mirror is what you turn off (`{ mirror: false }`) for anything dispatched per keystroke or per frame.

Observers are awaited in sequence: a slow one delays the flow that dispatched it, and on `cart_add_before` that delay is in front of the request. Analytics belongs in `_after`.

---

## Key Notes

- The manager is published as `window.__MAGE_OBSIDIAN_EVENTS__`, which is what the `CustomEvent` bridge and out-of-bundle code use. Inside the bundle, import it.
- Event names are `snake_case`, matching Magento's convention, and always `<domain>_<operation>_<phase>` for a mutation.
- `_after` means the flow ended, not that it worked. Check `result`.
- The dispatch logic, the activity tracker and the lifecycle definitions live in the engine (`mage-obsidian/runtime/`) with no DOM or framework dependency, so they are unit-tested in Node; the singletons, the reactive wrapper and the `CustomEvent` bridge are the module's `web/js/`.

---

## Next Steps

- [Optimistic UI & Motion](0158-optimistic-ui-motion.md) — what the storefront does with these events on screen.
- [Vue Islands](0105-vue-islands.md) — how the components dispatching these events are mounted.
- [State Management](0150-state-management.md) — the reactive cart state these events run alongside.
