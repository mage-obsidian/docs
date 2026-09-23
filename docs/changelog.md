# Changelog

MageObsidian ships as a set of independently versioned packages, but its features rarely live in
just one of them: a cacheable checkout is a core flag, a compatibility module and a theme template
landing together. This page follows the **stack**, so you can read what changed without having to
recompose it from a dozen release feeds.

Each entry names the packages and versions that carry it. For the commit-level history of a single
package, see its releases on [GitHub](https://github.com/mage-obsidian).

!!! note "Where this starts"
    The whole stack was cut to `2.0.0` together on **22 June 2026**, and that is where this log
    begins. Anything older predates the current line.

---

## September 2026

### Guest checkout that asks to sign in, and messages that repeat

With a downloadable product in the bag, Magento refuses guest checkout by default. Natively the
checkout buttons ask the guest to sign in; ours navigated to `/checkout`, which bounced back to the
cart, and the "Guest checkout is disabled." message showed only on the first try. The buttons now
send the guest to sign in with a `referer` back to checkout, the sign-in page returns there, and a
session message the server sends again always shows.

- **module-checkout** 3.12.1 — the cart page and mini-cart checkout buttons lead a guest to sign in
  when the cart refuses guest checkout
- **module-customer** 2.4.1 — a sign-in that carries a `referer` returns to it
- **module-storefront** 3.22.1 — show a repeated session message when its cookie was cleared
- **theme-default** 3.21.2 — pass the sign-in URL to the checkout buttons

### Installs that hold up outside our environment

Fixes found installing the stack on a store it was not built on: defaults that only worked in our
own environment, checks that failed a healthy deploy, and a policy that blocked payment pages.

**A fresh install serves built assets.** `module-modern-frontend` shipped HMR switched on, and
Magento only overrides that flag in production mode, so a new store in the default mode asked a
Vite dev server that was not running for every asset: all of them returned 404 and no island
mounted. HMR is now **off by default** and opt-in. `mage-obsidian:frontend:hmr --enable` and
`mage-obsidian:frontend:dev --up` still turn it on. If you use the dev server and never saved the
flag yourself, run `bin/magento mage-obsidian:frontend:hmr --enable` once after upgrading; the
doctor reports "HMR disabled" until you do.

**The doctor reports Adobe Commerce coverage.** On an Adobe Commerce install,
`mage-obsidian:frontend:doctor` adds a section listing the Commerce-only storefront families, the
Commerce modules behind each one and whether a MageObsidian module covers it.

**A production build no longer asks for dev server settings.** `mage-obsidian` 3.1.0 validates the
dev server variables only with `--dev-server`, and only `VITE_SERVER_HOST` and `VITE_SERVER_PORT`
are required. Without a terminal it never prompts. Before, a build without `vite/.env` opened a
prompt, exited 1 and aborted `setup:static-content:deploy` in any CI.

**PHP 8.3 is required.** Every MageObsidian Magento module now declares `"php": ">=8.3"`, and
`module-modern-frontend` requires Magento 2.4.7 or later. The code uses typed class constants, so
on PHP 8.2 Composer installed the packages and `setup:di:compile` then failed with a parse error.
**PHP 8.2 is no longer supported.**

**A failed compile keeps the CMS delta you had.** When the Tailwind binary was missing, timed out
or failed, `module-modern-frontend` wrote an empty delta over the last good one, and the classes
the build did not cover lost their styles until the next successful save. The previous stylesheet
now stays in place. A compile that fails with the binary installed is logged; a missing binary is left
to the doctor, which already reports it.

**The frontend contract is regenerated only when the module list is written.** Every write to
`config.php` or `env.php` regenerated it, so a failure there broke `deploy:mode:set` and
`setup:config:set`. It now runs only when the `modules` section is written, and a failure is logged
with the command to run instead of failing the write. A contract that fails its schema no longer
leaves the `.php` file rewritten either: both files are written only after validation passes.

**Payment pages allow inline styles again, and the pre-paint survives a strict policy.** Magento
enforces the policy on `checkout_index_index` and `multishipping_checkout_billing`, and our
storefront-wide `styles/inline=0` blocked the inline styles payment extensions inject there. Both
pages are back to Magento's default. The pre-paint now applies its rules through a constructable
stylesheet, which `style-src` does not govern, and falls back to a `<style>` element only in
browsers without them.

**Static deploy reports themes with no Vite build.** A theme whose build output was missing or
empty passed the deploy in silence. It is now named in a warning. Set `MAGE_OBSIDIAN_STRICT_DEPLOY=1`
to turn that warning, and a failure to publish the build, into a failed deploy.

**Source-writing commands refuse production mode.** `mage-obsidian:generate:module`, `:theme`,
`:component` and `mage-obsidian:i18n:collect` exit with an error in production mode instead of
failing halfway through a write. `mage-obsidian:frontend:dev` is unchanged.

**Page Builder classes stay out of the CMS delta.** `pagebuilder-*` classes never resolve to a
Tailwind rule and filled the delta's unresolved list. They are skipped by default; the prefix list
is an `ignoredClassPrefixes` argument of `ContentExporter` in `di.xml`.

**The Vite harness installs outside our own environment.** `component-modern-frontend` shipped
`vite/pnpm-workspace.yaml` with a pnpm store under `/home/www` and the supply-chain release-age
check switched off, both settings of our local environment. On any machine where `/home/www` is not
writable, `pnpm install` failed. Both are gone; if you relied on that store path, set
`pnpm_config_store_dir` in your environment. The harness now declares `engines.node >=22.13`, the
floor of the pnpm version it pins. Upgrading an install whose `vite/node_modules` was created with the old store path: delete
`vite/node_modules` once, or pnpm aborts without a terminal with
`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`.

- **module-modern-frontend** 2.20.0 — HMR off by default; contract validated before writing and
  regenerated only on module-list writes; CMS delta kept on a failed compile and Page Builder classes
  skipped; inline styles back on the payment pages and a CSSOM pre-paint; deploy warning for themes
  with no Vite build; Adobe Commerce storefront inventory; PHP 8.3 and Magento 2.4.7
- **module-modern-frontend-cli** 2.8.0 — Adobe Commerce section in the doctor; source-writing
  commands refuse production mode; requires core ^2.20
- **component-modern-frontend** 2.6.0 — drop our environment's pnpm settings from the harness;
  require engine ^3.1.0 and Node 22.13
- **mage-obsidian** 3.1.0 — validate dev server settings only with `--dev-server`
- **module-catalog** 3.12.0 — place the filter column where the page layout declares it
- **module-storefront** 3.22.0, **module-showcase** 1.5.0 — ship the collected `en_US` dictionary
- PHP 8.3 floor: **module-catalog-search** 2.2.0, **module-checkout** 3.12.0, **module-customer**
  2.4.0, **module-downloadable** 2.2.0, **module-gift-message** 2.2.0, **module-instant-purchase**
  2.2.0, **module-inventory-stock-visualizer** 1.2.0, **module-modern-frontend-twig** 2.7.0,
  **module-multishipping** 2.1.0, **module-persistent** 2.1.0, **module-product-alert** 2.1.0,
  **module-review** 2.3.0, **module-sales** 2.4.0, **module-search** 1.3.0, **module-send-friend**
  2.2.0, **module-vault** 2.3.0, **module-wishlist** 2.3.0

---

## August 2026

### Checkout served from the full-page cache

The checkout is now a cacheable public shell with the private half delivered through customer-data,
instead of an uncacheable page. The shell can be toggled per store.

- **module-checkout** 3.3.0 — serve the checkout page from the full-page cache; seed the island from
  the customer-data section; fill the shipping form from the customer address book; show selected
  options under each summary line
- **module-modern-frontend** 2.14.0 — cacheable checkout shell flag
- **module-modern-frontend** 2.15.0 — the section store reports whether its cached snapshot is unsynced
- **theme-default** 3.8.0 — inline only the cacheable half of the checkout config; label the saved
  address picker

### Cacheable listing fragments

Layered navigation, sorting and paging are served as cacheable fragments, so a filtered listing no
longer costs a full uncached page render.

- **module-search** 1.0.0 — new module: filters, sorting and paging as cacheable fragments
- **module-storefront** 3.7.0 — announce listing navigation so enhancers rebind after a swap

### Feature switchboard for demo stores

- **module-showcase** 1.0.0 – 1.2.0 — new module: switch MageObsidian features per visitor, offer the
  cacheable checkout as a visitor switch, and report the active feature set as New Relic attributes

### Static deploy verification

**Static deploy verification no longer cries wolf.** The check added in `module-modern-frontend`
2.15.0 read `--language`'s default value, `all`, as if it were a locale, so it looked under a
`pub/static/<area>/<theme>/all/` that Magento never writes and reported a flawless deploy as
entirely missing. It now resolves the sentinel through Magento's own `LocaleResolver`, honours
`--theme`, `--exclude-theme` and `--exclude-language`, and **warns instead of aborting** the deploy.

- **module-modern-frontend** 2.15.1 — resolve `--language all` through `LocaleResolver`; warn
  instead of aborting

---

## July 2026

The month the storefront line moved to `3.x` (21 July) and then grew a reactive layer on top of it.

### Optimistic UI and a typed storefront event bus

Every cart, wishlist, compare, catalog and checkout mutation now dispatches `before` / `after` /
`failed` events on a typed bus. The UI projects the change before the server confirms it and settles
when it does — counters flash, toasts fire, and in-flight operations are tracked centrally.

- **js-package-utils** 2.5.0 — observer-style event manager
- **js-package-utils** 2.6.0 — typed storefront events with sticky dispatch and a DOM mirror;
  `patchSection` for projecting a change ahead of the server; in-flight operation tracking;
  optimistic-UI runtime config
- **module-modern-frontend** 2.11.0 — storefront event manager singleton
- **module-modern-frontend** 2.12.0 — island lifecycle events and section patching wired into the
  runtime; optimistic-UI storefront flag
- **module-storefront** 3.2.0 – 3.4.0 — events around every cart mutation; cart, wishlist and compare
  mutation events; search mutation events from the autocomplete; toasts driven by the notification
  event; the optimistic feedback layer for buttons, notices and value flashes
- **module-checkout** 3.1.0 — cart page driven by the event bus; checkout mutation and step-change
  events; mini-cart items removed optimistically
- **module-catalog** 3.1.0, 3.3.0 — variant, bundle, gallery and product-option events

### Islands that hydrate over server-rendered markup

Islands no longer pop in over an empty container: the server renders the markup the island adopts,
and development builds report hydration drift when the two disagree.

- **module-modern-frontend** 2.9.0 — server-side placeholder inside island markers
- **module-modern-frontend** 2.11.0 — islands rendered with hydratable server markup; hydration drift
  reported in development builds; doctor flags eager islands that render an empty container
- **js-package-utils** 2.5.0 — mount islands from server markup and diff for drift; `island-ssr` CLI
  to render an island's initial markup
- **js-package-utils** 2.6.1 — flag a marker once its island has finished rendering
- **module-modern-frontend-twig** 2.3.0 — island markup and icon classes exposed to templates
- **theme-default** 3.2.0 — server-render the markup hydrating islands adopt

### Personalised content drawn before the first paint

Customer-data counters and the sign-in state are painted from a declaration in `di.xml`, before the
first frame, so personalisation no longer arrives as a visible flicker.

- **module-modern-frontend** 2.12.1 — draw customer-data counters before the first paint
- **module-storefront** 3.4.3 — declare the header counters
- **module-customer** 2.0.4 — account flag declared and the sign-in placeholder gated
- **theme-default** 3.4.5 — the pre-paint runtime owns the sign-in placeholder

### Tailwind for CMS content

Classes typed into CMS pages and blocks were invisible to the build. Content is now exported, scanned
and compiled on demand, served as a delta stylesheet behind a stable URL and an ETag.

- **module-modern-frontend** 2.11.0 — compile Tailwind classes the build never saw; export content for
  scanning; delta stylesheet from a stable URL with an ETag; per-page/block opt-out; the `Icon`
  component and Vue islands placeable from content via widget and directive
- **module-modern-frontend-cli** 2.4.0 — `cms:export` and `cms:jit` commands, wired into the doctor
- **js-package-utils** 2.5.0 — scan exported CMS content for Tailwind classes and pin the list per theme

### Cross-document view transitions

- **module-storefront** 3.3.0, 3.4.0 — transitions scoped to catalog moves; product cards reordered
  with duplicate names guarded
- **module-catalog** 3.2.0, 3.3.0 — the gallery image named as the card morph target; cards classed and
  the gallery swap calmed
- **theme-default** 3.3.0, 3.4.0 — the chrome held still across transitions; rules moved into a
  stylesheet, animating cards and cart lines

### A shared field system and UI primitives

- **module-storefront** 3.4.0 — a shared field component with required and error states; checkbox and
  slot primitives; button, link and field primitives as layered components

### Navigation

- **module-storefront** 2.1.0 — priority+ primary nav island with an overflow menu
- **module-storefront** 2.2.0 — nested mega menu with desktop flyouts and a mobile accordion;
  configurable mobile brand and home link
- **module-storefront** 3.1.0 — cache-tagged nav block for ESI fragments; menu tree cached in
  `block_html` with a 1 h TTL; category URL rewrite lookups batched into one query
- **module-catalog** 3.5.0 — layered navigation as a drawer on mobile
- **theme-default** 3.1.0, 3.4.0, 3.7.0 — nav blocks served as ESI fragments with a TTL; the primary nav
  split by container queries instead of client-side measuring; drawer filters and a two-row mobile toolbar

### One-page checkout layout

The checkout ships in two layouts behind a config flag: the stepped wizard, or a reactive one-page
layout.

- **module-checkout** 2.1.0 — reactive one-page checkout layout
- **module-modern-frontend** 2.8.0 — checkout layout mode config flag
- **module-checkout** 2.2.0 — native checkout configuration respected (agreements, guest login, summary
  cap, `display_billing_address_on`)

### MSI stock visualizer

- **module-inventory-stock-visualizer** 1.0.0 — new module: an availability panel routed by product
  type, redesigned around a segmented source rail, server-rendered and skipped entirely for
  out-of-stock products

### Twig engine

- **module-modern-frontend-twig** 2.1.0 – 2.5.0 — placeholder markup forwarded through `render_vue`;
  namespace aliases and `@parent` template inheritance; `inline_view_file` to embed a view file
  verbatim; `script()` to load a Vite enhancer without a rendering block

### Diagnostics

- **module-modern-frontend** 2.10.0, 2.11.0 — detect a page cache key that ignores `X-Magento-Vary`;
  report the Tailwind binary and unresolved CMS classes
- **module-modern-frontend-cli** 2.3.0, 2.4.0 — page cache vary handling reported; templates scanned for
  eager islands without hydration

### Speculation rules

- **module-storefront** 3.6.0 — configurable speculation rules

---

## June 2026 — the 2.0.0 line

The whole stack was cut together on 22 June: core engine, CLI, Vite harness, JS engine, the optional
Twig engine, `module-storefront`, both themes, and the compatibility modules for catalog, search,
checkout, customer, sales, wishlist, reviews, vault, gift message, downloadable, multishipping,
persistent, product alert, send-friend and instant purchase.

### Vue islands

- **module-modern-frontend** 2.0.0 — Vue components rendered as lazy-hydrated islands; `@api` interfaces,
  drift detection and hardening
- **js-package-utils** 2.0.0 — island hydration runtime
- **module-modern-frontend** 2.1.0 — customer-data section hydration deferred to idle, off the critical path
- **module-modern-frontend** 2.2.0, 2.2.1 — `modulepreload` of the eager island dependency graph, emitted
  inline per marker so body-end islands are covered too

### Critical CSS

- **js-package-utils** 2.4.0 — Beasties critical-CSS extractor
- **module-modern-frontend** 2.4.0 — critical-CSS path and per-theme HTML-minify opt-out
- **module-modern-frontend-cli** 2.2.0 — critical-CSS generation command
- **theme-base** 2.1.0 — stylesheet deferred per page when critical CSS exists

### Optional Twig engine

- **module-modern-frontend-twig** 2.0.0 — a `.twig` engine coexisting with `.phtml`, with i18n, eager
  mount and html-safe filters, a responsive `image` helper, a `json_ld` helper and DI-registered extensions

### SEO, images and i18n

- **module-modern-frontend** 2.0.0 — schema.org JSON-LD (Organization, WebSite, BreadcrumbList, Product);
  CWV-friendly image render helper
- **js-package-utils** 2.2.0 — i18n facade for plain ESM enhancers
- **module-modern-frontend-cli** 2.0.2 — `$t` phrases collected from `.ts` and `.js` sources
- **theme-base** 2.0.1 — translation dictionary preloaded off the island bootstrap chain

### Developer workflow

- **module-modern-frontend** 2.0.0, 2.3.0 — dev diagnostics core and client-side dev-server guard; Vite dev
  server lifecycle managed via process group; nginx proxy snippet derived from config; `DevWorkflow` and
  `ThemeSelector`
- **module-modern-frontend-cli** 2.0.0, 2.1.0 — doctor reports ignored config files; `jsconfig` and
  `.gitignore` scaffolding for editor types; one-shot `--up`/`--down` and a theme picker for `frontend:dev`
- **js-package-utils** 2.3.0 — theme prompt when `--dev-server` omits `--theme`
