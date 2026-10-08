---
description: "What MageObsidian does not cover and why, with the Luma parity register read on 2026-10-07."
---
# Known scope

What MageObsidian does not cover, and why. Each item here is a decision or a measured limit, not something left out of sight.

## Luma parity

The parity register was read on 2026-10-07 against **Magento Open Source 2.4.9**. It lists 529 entries: 265 covered, 53 partial, 7 uncovered, 59 resolved, 142 out of scope and 3 blocked. A covered entry has a test that observed the behaviour, and every block the core contributes to that screen is accounted for. A partial entry has the test, but one or more of those blocks has no counterpart; the four groups below are the ones that are not covered.

Until 2026-10-06 the register compared screens only, so a screen MageObsidian re-declared counted as covered even when a block another core module added to it was gone. It now also compares the 832 blocks the core declares on those screens. The 71 partial entries it first found came from that comparison, and they were all counted as covered before; 53 remain.

### Partial

79 blocks on 53 screens have no counterpart. Each one is listed in the register with what the shopper loses. By area:

| Area | What is missing |
|---|---|
| Account and session | There is no account offer on the success page for a guest who just paid. |
| Catalog and search | The category image, swatches on listing cards, the compare sidebar, recently viewed products, and search suggestions and related terms. Product views and search terms are no longer recorded for the admin reports. |
| Orders and emails | Bundle selections and downloadable link titles in the order, invoice and credit memo emails, and Fixed Product Tax in their totals. Comments on orders, invoices, shipments and credit memos. Reorder and Print Order on the document pages, the Track your order link, the Recently Ordered sidebar, the order status on printed documents, and the print and downloadable-products links on the success page. Item options in the multi-address steps. |
| Wish list | Updating quantities, item comments, editing a saved item's options, showing which variant was saved, review summaries, and the sidebar. |
| Marketing and feeds | Google Ads conversion tracking, both the gtag and the legacy tag (Google Analytics 4 is ported). RSS links in the head, the footer, category pages, the wish list and order pages. |
| Platform | Subresource Integrity hashes on the checkout scripts (PCI DSS 4.0 requirement 6.4.3). A switcher between store groups. The back-in-stock unsubscribe page. |

### Found by the functional audit

The screen and block comparison cannot see a store setting that Magento honours inside a block that exists, or a script behaviour with no counterpart. A functional audit of those cases gave the register an origin of its own: each entry names the core setting, template or script that defines the behaviour and the value that triggers it, and it can only be resolved by a test that sets that value. It added 36 entries, and the inventory of the reCAPTCHA forms and the session work added 7 more: 32 resolved, 7 open and 4 out of scope.

Resolved: the minimum order amount, a reduced quantity, a price change and a line out of stock are announced in the cart and make Proceed to checkout inert; a cart holding a minimum advertised price item says the total comes later; the cross-sell cards add to the bag, the wish list and the comparison like a listing card; an add follows the redirect to the cart when the store asks for it; the side bag honours its display switch, its line limit with an "N of M" link and the edit link; the cart paginates its lines; the "All" page-size limiter no longer breaks the category page; the postal code is optional in the countries the store declares, and the telephone follows its setting; the prefix, middle name, suffix, birth date, gender, tax id, company, fax and VAT number follow their settings in the account forms and the checkout, as does the number of street lines; the configured password length and character classes are announced, enforced and measured; cheque, bank transfer and cash on delivery show the merchant's instructions; a purchase order asks for its number and records it; the bag lines, the totals and the checkout summary state prices, subtotal and shipping with tax, without it or both as the store configures, with the full tax summary and a zero tax hidden when asked; the shipping rates, the estimator's totals and a configurable's price keep both amounts after a variant is chosen; and Fixed Product Tax is included in the price, named by label or stated as one row as configured; a signed-in customer can bill a saved address; the comparison states prices as the listing does, so a minimum advertised price stays hidden, sends a configurable to its page instead of failing to add it, can be emptied in one step and saves to the wish list; a guest is asked to sign in when the store does not allow guest reviews, the reviews of a product are paged, and the cards in category and search listings show their rating; layered navigation drops the product count when the store turns it off, send to a friend offers the configured number of recipients and the advanced search caps its fields at the configured length; and no link points at the newsletter, wish list, reviews or contact page once the store turns the feature off; and the image captcha that waits for failed attempts now appears in the background sign-in once the third one fails; the sign-in sends the reCAPTCHA token, so it works with the challenge on; the browser's cookie settings (domain, path, Secure, website) are published and applied to every cookie the storefront writes; a browser that refuses cookies is told so instead of a mutation failing; Remember Me and the checkout context travel with the background sign-in and registration, so the persistent bag survives them; a recognised visitor is greeted by name with Not you?; and the menu on a phone offers Sign In, Create an Account, My Account and Sign Out; and the product page announces whether the product is in stock and how many are left under the store's threshold, and a downloadable sold link by link prices the links the buyer chooses, with a select-all control.

The forms the reCAPTCHA modules protect were inventoried against 2.4.9. The coupon in the cart, the wish list share, the review, send to a friend, registration, password reset, account information, contact, the newsletter and placing an order each render the challenge and accept the answer, with the multi-address review now showing the terms and conditions as well. Two settings have no storefront form to protect and are out of scope: PayPal Payflow Pro, which the checkout does not offer, and resending the confirmation, which core guards only on its REST and GraphQL operation.

Open, by area:

| Area | What the store configures and the storefront ignores |
|---|---|
| Checkout | In-store pickup from MSI has no interface although its modules are enabled. |
| Page chrome | The logo, welcome message and copyright configured in the admin are not shown, and the fixed texts of the footer are not translatable. |
| Widgets | Only the product list widget is ported, and the containers that receive widgets from the admin do not exist. |

### Blocked

Three entries are blocked. None is a missing feature nobody has looked at; each waits on a decision.

| Entry | Why it is blocked |
|---|---|
| Page Builder video background from YouTube or Vimeo | A self-hosted video background plays. A provider-hosted one needs the provider's player in a frame, which is a third-party request during page load and a privacy decision. Provider URLs are refused rather than loaded silently. It unblocks when the storefront settles how provider embeds are fetched. |
| Page Builder row at full-bleed width | Contained and full-width rows are fixed. True edge-to-edge needs a viewport-relative width that overflows horizontally by the scrollbar unless an ancestor clips, so it waits on a decision about where clipping belongs in the theme shell. |
| Server-rendered initial state of the map and banner content types | They save an island marker with no initial state inside it, so what they show appears when the island hydrates. Neither moves the page, but neither is readable with no script. It needs a per-request island renderer. |

### Out of scope

142 entries are out of scope, each with its reason in the register. By family:

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
| 2 | Declined behaviours | The catalog list view, which the theme drops on purpose, and inline translation, a development tool. |
| 2 | Settings with no storefront form | reCAPTCHA for PayPal Payflow Pro, which the checkout does not offer, and for resending the confirmation, which core guards only through its API. |
| 7 | Single replacements | Product gallery route, the core checkout page layout, a cart handle the platform does not route, a handle no core controller loads, a Page Builder category description template, the review list endpoint, and the first uncacheable search, which is core behaviour. |

## Payment gateways

No commercial payment gateway has been verified. The extension point is: a payment method can render its own interface inside the checkout, ask for its own fields and hand the shopper over to a gateway and back, and that mechanism is exercised by a purpose-built probe method. A real gateway needs its own verification.

## Adobe Commerce

Adobe Commerce is detected and inventoried by `mage-obsidian:frontend:doctor`, which reports which Commerce-only storefront families a store has enabled. It is not in the compatibility matrix. The storefront was walked once on Adobe Commerce 2.4.9 on 2026-10-06; Adobe Commerce Cloud, payment gateways and Commerce-only features are unverified. See [Adobe Commerce](../getting-started/adobe-commerce.md).
