# Navigation continuity

Moving from one page of the storefront to the next should feel like one application, not a
sequence of pages being torn down and rebuilt. On a slow phone that is not what a browser does by
default, and MageObsidian closes the gap with two small pieces from `mage-obsidian/module-storefront`.

## What the browser does on its own

When the shopper follows a link, Chrome keeps the old page on screen until the new document paints
something ("paint holding"). The first thing a storefront paints is its header, so on a slow CPU the
shopper sees the old page, then a header over an empty body, then the page assembling itself piece
by piece. Measured on the demo with the CPU throttled 6×, seven navigations out of nine showed at
least one entirely blank frame, even though the documents had already been prefetched.

## Holding the previous page

The storefront keeps the previous page on screen until the next one has parsed its main content:

- A tiny inline script in the `<head>` adds `<link rel="expect" href="#obsidian-main-end"
  blocking="render">`. The browser does not render the new document until that element exists.
- The element is an empty, hidden `<div id="obsidian-main-end">`: the last child of the
  `main.content` container, so it arrives after the breadcrumb, the title and the listing, and
  before the footer.
- The script only does this when the shopper **arrives from another page of the same store**
  (`navigation.activation.from` is set). A first visit, an arrival from a search engine and a reload
  paint progressively as before, so first-load metrics and Lighthouse are unchanged.
- Images still arrive after the swap, into the space already reserved for them.

The link is emitted through Magento's `SecureHtmlRenderer`, so it carries the CSP nonce and works
under a strict policy.

=== "CLI"

    ```bash
    bin/magento config:set mage_obsidian/navigation/retain 0   # 1 to turn it back on
    bin/magento cache:flush
    ```

=== "Admin"

    **Stores → Configuration → MageObsidian → Frontend → Speculative Loading → Hold the Previous
    Page Until the Next Is Ready**

It ships **on**. Turning it off brings back progressive rendering between pages; nothing else
depends on it.

!!! note "A layout without `main.content`"

    The marker lives in the `main.content` container. A page layout that removes that container has
    no marker, and the browser releases rendering when it has parsed the whole document: the page
    still appears, only later. Browsers without `rel="expect"` or without the Navigation API ignore
    the hold and render progressively.

## Immediate feedback on the click

While the previous page is held, a click must still visibly register. A thin bar at the top of the
viewport starts at once when the shopper follows a link or submits a form to another page of the
store, and a polite `role="status"` region announces "Loading the page" to assistive technology
without taking focus.

- It is driven by the Navigation API's `navigate` event, so it ignores new tabs, downloads, anchors
  on the same page and links to other sites.
- It disappears when the navigation fails or is stopped, and when the page comes back from the
  back/forward cache.
- With `prefers-reduced-motion: reduce` the bar stays still instead of animating.
- It never takes pointer events or moves the layout; its colour is `--color-accent`.

## Prerender: viable, with conditions

The Speculative Loading group already offers `prerender` as a mode. It was measured on 2026-09-29
against a development store, with a Chrome that had no automation client attached. With one
attached — Playwright, DevTools — Chrome refuses to prerender and reports
`PrerenderingDisabledByDevTools`, so no automated suite can observe it.

| Question | Finding |
|---|---|
| Does it activate? | Yes. The prepared page was shown with `activationStart` at 5 s, already painted. |
| Private data prepared early | The prerendered page loads the customer sections while it is being prepared. When the cart changed in between, it reloaded them on activation and showed the right count about **130 ms** later. The stale value is on screen for that time. |
| Analytics | Safe as shipped. The gtag queue is filled, but the library waits for the shopper's first interaction, which can only happen after activation. |
| Server load | One extra uncacheable `customer/section/load` (PHP) per prepared page, on top of the document a prefetch already costs, plus the images in its viewport. With `moderate` eagerness that is every link hovered for 200 ms. |
| With the held page | No conflict. A prerendered page is already painted when it is activated, so there is nothing to hold. |

**Decision:** keep `prefetch` as the default. Prerender becomes worth turning on once three things
hold, and they belong to a change of their own:

1. The customer-section store waits for `prerenderingchange` before rendering private data, so an
   activated page never shows a stale value.
2. Prerender is limited to the links most likely to be followed (product cards) or runs with
   `conservative` eagerness, so hovering a listing does not cost a PHP request per card.
3. Its verification runs outside the automated suite, since a Chrome under automation never
   prerenders.

## How it is verified

`storefront-verification` walks the storefront by clicking — home, a listing from the menu, a
product card, another listing, the logo, a search, the cart — on desktop and on a Pixel 7 profile
with the CPU throttled 6×, and records the screen while doing it
(`specs/navigation-continuity.paint.spec.ts`). Every frame between a click and the finished page is
classified; the test fails on a blank frame or on a page half built (a header over an empty body)
and attaches the offending frame. Loading pages directly with `page.goto` does not count as coverage
of this behaviour.
