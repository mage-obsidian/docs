# Optimistic UI & Motion

A storefront feels slow long before it *is* slow. Clicking `+` on a cart row and watching the number sit still for 400 ms while a request travels is the difference between an interface that responds and one that waits — and no amount of server tuning removes the round trip.

**{{ config.extra.components_name }}** answers it the other way round: apply the change on screen immediately, send the request, and reconcile when the server answers. The state layer and the [event bus](0155-storefront-events.md) already provide everything this needs — a reactive local copy, a snapshot to go back to, and a phase to hang the spinner on.

---

## The flag

```
Stores → Configuration → MageObsidian → Storefront → Optimistic UI
```

`mage_obsidian/storefront/optimistic_ui`, default **Yes**, scoped per website and store view. Turned off, quantity and removal wait for the server before touching the screen — the animations still play, just when the response lands.

The flag reaches the browser as `window.__MAGE_OBSIDIAN_UX__`, emitted inline through `SecureHtmlRenderer` so it carries the CSP nonce, and is read with:

```ts
import { readUxRuntimeConfig } from 'mage-obsidian/runtime/uxConfig.ts';

const ux = readUxRuntimeConfig(); // { optimistic, summaryCountsQty }
```

**Adding to cart is optimistic regardless of the flag.** The badge going up is the acknowledgement of the click, and there is no state to corrupt: the count is projected forward and the mandatory section reload replaces it with the server's number a moment later.

---

## How reconciliation works

Three pieces of the section store, all on `useCustomerData`:

| Member | Purpose |
|---|---|
| `patch(name, partial)` | merge a partial section into the reactive map |
| `snapshot()` | the current map, to go back to |
| `restore(snapshot)` | put it back |

`patch` is **memory-only** — it never writes to `mage-cache-storage`. Magento's `customer-data.js` stays the owner of the canonical cache, so a projection that turns out to be wrong dies with the page instead of outliving it in local storage.

Two flows come out of that:

**Add** needs no rollback. `post()` already reloads the `cart` and `messages` sections on completion, and that reload *is* the reconciliation — it overwrites the projection with the truth whether the add succeeded or not.

```ts
customerData.patch('cart', {
    summary_count: count.value + (ux.summaryCountsQty ? qty : 1),
});
```

**Quantity and removal** in the mini-cart take a snapshot first, project, and put it back if the server refuses:

```ts
const rollback = customerData.snapshot();
if (ux.optimistic) {
    project();
}

const { ok, message } = await mutate();
if (!ok) {
    customerData.restore(rollback);
    notify(message ?? 'Could not update your bag', NotificationTone.Warning);
}
```

The removed row re-enters through the same transition it left by, and the warning says why.

### Counting units or lines

Magento decides what the bag badge means: `checkout/cart_link/use_qty` makes `summary_count` the number of **units**, off it counts **lines**. The projection has to agree, or adding two of something moves the badge by the wrong amount and the reload visibly corrects it.

That setting travels in the same global as `summaryCountsQty`, which is why the projection reads it instead of assuming.

---

## Loading state

No component owns a loading flag. Both the button and the badge derive theirs from the bus:

```ts
const activity = useActivity();
const syncing = computed(() => activity.isBusy('cart'));
```

**The bag badge** grows a thin rotating ring around the icon and fades the number to 45% while anything cart-related is in flight. Since the add is optimistic, the number is *already* the new one — the ring says "syncing", not "I don't know yet".

**The button** keeps its label in the box and hides it with `visibility`, then centres the spinner absolutely on top:

```html
<button :class="{ 'is-loading': adding }">
    <span class="obsidian-button__label">Add to cart</span>
    <span v-if="adding" class="obsidian-button__spinner"></span>
</button>
```

Swapping the label out for a spinner is the obvious implementation and the wrong one: the spinner is shorter and narrower than the text, so the button shrinks the moment it is clicked and everything around it moves. Keeping the label reserves the exact box it already had. Nothing shifts, and no `min-width` needs guessing.

The spinner is `1em`, so it scales with whatever button it lands in.

---

## Motion

### Removing a row

The row slides right and fades while the rows below glide up to close the gap:

```css
.minicart-item-move,
.minicart-item-enter-active,
.minicart-item-leave-active {
    transition:
        transform 0.32s var(--ease-obsidian),
        opacity 0.24s var(--ease-obsidian);
}

.minicart-item-enter-from,
.minicart-item-leave-to {
    opacity: 0;
    transform: translateX(1.5rem);
}

.minicart-item-leave-active {
    position: absolute;
    left: 0;
    right: 0;
}
```

`position: absolute` on the leaving row is the whole trick. Vue's `TransitionGroup` computes the FLIP offsets for `-move` from where the remaining elements land; while the leaving row still occupies its space, they land nowhere. Taking it out of flow lets them move up immediately, and the transition animates the difference.

Only `transform` and `opacity` are animated — both composited, neither triggering layout. Animating `height` to collapse the row would do the same thing visually at the cost of a layout pass per frame.

!!! warning "The scroll container needs `overflow-x: hidden`"
    The leaving row translates 24 px past the right edge of a list that is `overflow-y: auto`. CSS resolves the other axis of a scroll container to `auto` too, so the drawer grows a horizontal scrollbar for the length of every removal. Pinning `overflow-x: hidden` on the list is the fix.

### Changing quantity

Three things happen at once, each saying something different:

- **The number changes immediately.** The controls are never disabled, so clicking `+` three times fast works; the requests queue and the last one wins.
- **The stepper bumps** (`scale(1.08)`, 250 ms) — the acknowledgement that the click registered.
- **The line price dims and pulses** while its request is in flight, and **the subtotal flashes** `--color-accent-soft` when its value actually changes.

The flash is a composable, so the bag page and checkout get it the same way:

```ts
import { useValueFlash } from 'MageObsidian_Storefront::js/useValueFlash';

const subtotalFlashing = useValueFlash(() => subtotal.value);
```

The shimmer is on the **price only**, not the row. Dimming the whole row to say "one number is updating" reads as "this item is disabled".

### Emptying

When the last row leaves, the list cross-fades into the empty panel instead of collapsing to it — `<Transition mode="out-in">` around the two states.

### Destructive actions

Remove controls use `--color-danger` (`#a4322b`, a muted mineral red that sits inside the OBSIDIAN palette), at 72% opacity, reaching full opacity and `scale(1.1)` on hover. It is a theme token, not a mini-cart constant, so anything destructive across the storefront uses the same red.

The icon comes from the shared sprite through the `Icon` component, never inline SVG — the same source `hero_icon()` uses, so a hydrating component matches its server markup.

---

## Reduced motion

Every transition and animation in this document is switched off under `prefers-reduced-motion: reduce`, including the spinners:

```css
@media (prefers-reduced-motion: reduce) {
    .minicart-item-move,
    .minicart-item-enter-active,
    .minicart-item-leave-active,
    .minicart-value,
    .minicart-qty {
        transition: none;
    }

    .cart-count__ring,
    .obsidian-button__spinner {
        animation: none;
    }
}
```

The result is still fully functional: rows disappear, numbers change, states are still legible — they simply arrive instantly. Optimistic UI is *why* that works, since without the animation there is nothing to wait for.

---

## Key Notes

- Motion class names are written as plain CSS selectors in `module.extend.css`, not Tailwind utilities. Nothing references them statically, so the tree-shaker would drop them.
- That file lives in `view/frontend/web/css/`, not `view/frontend/web/` — anywhere else and the theme does not build it.
- `patch` never persists. The canonical customer-data cache stays Magento's.
- Only project what the server can confirm. The mini-cart projects `items` and `summary_count`; it does not recompute the subtotal, because tax, discounts and totals rules are the server's answer to give.
- Optimistic does not mean silent. A refused mutation always reverts *and* says so.

---

## Next Steps

- [Storefront Events](0155-storefront-events.md) — the convention the loading state is derived from.
- [State Management](0150-state-management.md) — `patch`, `snapshot` and `restore` in context.
- [Performance](0160-performance.md) — the budget this motion has to live inside.
