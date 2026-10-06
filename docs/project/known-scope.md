---
description: "What MageObsidian does not cover and why, with the Luma parity register read on 2026-09-29."
---
# Known scope

What MageObsidian does not cover, and why. Each item here is a decision or a measured limit, not something left out of sight.

## Luma parity

The parity register was read on 2026-09-29 against **Magento Open Source 2.4.9**. It lists 486 entries: 318 covered, 27 resolved, 138 out of scope and 3 blocked. A covered entry has a test that observed the behaviour; the two groups below are the ones that are not.

### Blocked

Three entries are blocked. None is a missing feature nobody has looked at; each waits on a decision.

| Entry | Why it is blocked |
|---|---|
| Page Builder video background from YouTube or Vimeo | A self-hosted video background plays. A provider-hosted one needs the provider's player in a frame, which is a third-party request during page load and a privacy decision. Provider URLs are refused rather than loaded silently. It unblocks when the storefront settles how provider embeds are fetched. |
| Page Builder row at full-bleed width | Contained and full-width rows are fixed. True edge-to-edge needs a viewport-relative width that overflows horizontally by the scrollbar unless an ancestor clips, so it waits on a decision about where clipping belongs in the theme shell. |
| Server-rendered initial state of the map and banner content types | They save an island marker with no initial state inside it, so what they show appears when the island hydrates. Neither moves the page, but neither is readable with no script. It needs a per-request island renderer. |

### Out of scope

138 entries are out of scope, each with its reason in the register. By family:

| Entries | Family | Reason |
|---|---|---|
| 53 | Renderer declarations | Not a screen: they contribute item renderers to another handle. |
| 24 | Consolidated screens | Equivalent by another route: MageObsidian consolidates what the core splits per product type. |
| 17 | PayPal and Payment Services | Decided on 2026-08-27 not to build those screens in this project. |
| 15 | Fragments and base handles | Not a storefront screen: a fragment, a base handle that every concrete one re-declares, or a Knockout endpoint the stack replaced. |
| 7 | Wish list items with options | Deliberately not used: the item links to the product page instead. |
| 4 | Handles with no route | The handle has no route on this platform version. |
| 4 | Re-expressed behaviour | MAP as a native disclosure with no JavaScript, remember-me handled centrally. |
| 3 | Swagger tools | Development tools served only outside production mode, with their own legacy JavaScript. |
| 2 | Off-site payment flows | Reaching them needs a payment method that places the order and sends the shopper off-site. |
| 2 | Declined products | A separately sold checkout and a copy-and-paste component library: decisions taken, not gaps left open. |
| 7 | Single replacements | Product gallery route, the core checkout page layout, a cart handle the platform does not route, a handle no core controller loads, a Page Builder category description template, the review list endpoint, and the first uncacheable search, which is core behaviour. |

## Payment gateways

No commercial payment gateway has been verified. The extension point is: a payment method can render its own interface inside the checkout, ask for its own fields and hand the shopper over to a gateway and back, and that mechanism is exercised by a purpose-built probe method. A real gateway needs its own verification.

## Adobe Commerce

Adobe Commerce is detected and inventoried by `mage-obsidian:frontend:doctor`, which reports which Commerce-only storefront families a store has enabled. It is not in the compatibility matrix. The storefront was walked once on Adobe Commerce 2.4.9 on 2026-10-06; Adobe Commerce Cloud, payment gateways and Commerce-only features are unverified. See [Adobe Commerce](../getting-started/adobe-commerce.md).
