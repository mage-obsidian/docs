# Storefront Events

**{{ config.extra.components_name }}** ports both of Magento's extension points to the browser. They answer different questions, and the difference is the same one it is in PHP:

| | Wraps | Can change what happens | Wired |
|---|---|---|---|
| **Interceptors** | a specific function | yes | at build time, by module |
| **Events** | nothing — something already happened | only through the data it carries | at runtime, by anyone |

Extending a flow from another module should not require knowing which function to wrap. So the flow announces what it did, and anyone can listen.

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

Observers run in `sortOrder` (default `10`, lowest first) and are awaited, so an async one finishes before the next runs. `observe` returns a function that removes it.

An observer that throws is reported and skipped — a failing analytics hook must never take down an add-to-cart.

```js
events.observe('cart_add_before', (data) => { … }, { name: 'my_module', sortOrder: 5 });
```

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

---

## The cart flow

Every cart mutation funnels through one function, so the events are announced there rather than at each call site — `addFromForm`, `addProduct`, `addRaw`, `updateItemQty` and `removeItem` all emit them.

| Event | When |
|---|---|
| `cart_add_before` | after the form key is backfilled, before anything is sent |
| `cart_add_after` | after the response and the `cart`/`messages` section reload |
| `cart_add_failed` | additionally, when the mutation did not succeed |

`update_qty` and `remove_item` have the same three.

The payload:

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

A `_before` observer may rewrite `action` or `body` — the request is what it leaves behind:

```js
events.observe('cart_add_before', (data) => {
    data.body.set('qty', String(Number(data.body.get('qty')) * 2));
});
```

…or stop it entirely, in which case nothing is sent and no `_after` or `_failed` follows:

```js
events.observe('cart_add_before', (data) => {
    if (isRestricted(data.body.get('product'))) {
        data.cancelled = true;
        data.message = 'Not available in your region';
    }
});
```

The caller sees `{ ok: false, message }`, so the toast says what happened.

---

## Key Notes

- The manager is published as `window.__MAGE_OBSIDIAN_EVENTS__`, which is what the `CustomEvent` bridge and out-of-bundle code use. Inside the bundle, import it.
- Event names are `snake_case`, matching Magento's convention.
- The dispatch logic lives in the engine (`mage-obsidian/runtime/eventManager.ts`) with no DOM or framework dependency, so it is unit-tested in Node; the singleton and the `CustomEvent` bridge are the module's `web/js/events.ts`.

---

## Next Steps

- [Vue Islands](0105-vue-islands.md) — how the components dispatching these events are mounted.
- [State Management](0150-state-management.md) — the reactive cart state these events run alongside.
