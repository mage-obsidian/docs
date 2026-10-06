---
description: "What MageObsidian does not cover and why, with the Luma parity register read on 2026-10-06."
---
# Known scope

What MageObsidian does not cover, and why. Each item here is a decision or a measured limit, not something left out of sight.

## Luma parity

The parity register was read on 2026-10-06 against **Magento Open Source 2.4.9**. It lists 486 entries: 247 covered, 71 partial, 27 resolved, 138 out of scope and 3 blocked. A covered entry has a test that observed the behaviour, and every block the core contributes to that screen is accounted for. A partial entry has the test, but one or more of those blocks has no counterpart; the three groups below are the ones that are not covered.

Until 2026-10-06 the register compared screens only, so a screen MageObsidian re-declared counted as covered even when a block another core module added to it was gone. It now also compares the 832 blocks the core declares on those screens. The 71 partial entries come from that comparison, and they were all counted as covered before.

### Partial

108 blocks on 71 screens have no counterpart. Each one is listed in the register with what the shopper loses. By area:

| Area | What is missing |
|---|---|
| Blocks an action when a store setting is on | With reCAPTCHA enabled for coupons, a coupon cannot be applied from the cart. With reCAPTCHA enabled for the wish list, a wish list cannot be shared. With terms and conditions enabled, the multi-address review shows no agreements to accept. The core still validates all three on the server. |
| Cart | Minimum order amount, reduced-quantity and price-change notices are not shown, and checkout is not disabled by them. A cart with a minimum-advertised-price item shows its total. Cross-sell cards have no add to wish list or compare. |
| Account and session | On a phone there is no Sign In or My Account link in the header or the menu drawer. Remember Me is lost on the default sign-in. A sign-in or registration started from checkout loses the checkout context. There is no Create an Account link in the header and no account offer on the success page. A shopper with cookies disabled is not told so. The cookie domain and Secure setting are not published to the browser, so the `form_key` cookie ignores them. |
| Catalog and search | Product videos, tier-price messages, quantity-increment hints, the category image, swatches on listing cards, the compare sidebar, recently viewed products, search suggestions and related terms, and skip links around the gallery. Product views and search terms are no longer recorded for the admin reports. |
| Orders and emails | Bundle selections and downloadable link titles in the order, invoice and credit memo emails, and Fixed Product Tax in their totals. Comments on orders, invoices, shipments and credit memos. Reorder and Print Order on the document pages, the Track your order link, the Recently Ordered sidebar, the order status on printed documents, and the print and downloadable-products links on the success page. Item options in the multi-address steps. |
| Wish list | Updating quantities, item comments, editing a saved item's options, showing which variant was saved, review summaries, and the sidebar. |
| Marketing and feeds | Google Ads conversion tracking, both the gtag and the legacy tag (Google Analytics 4 is ported). RSS links in the head, the footer, category pages, the wish list and order pages. |
| Platform | Subresource Integrity hashes on the checkout scripts (PCI DSS 4.0 requirement 6.4.3). A switcher between store groups. The back-in-stock unsubscribe page. Customer data invalidation across websites that share an origin. |

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
