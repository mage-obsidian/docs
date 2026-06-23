# {{ config.extra.theme_name }}

**{{ config.extra.theme_name }}** is the reference storefront theme built entirely with
**{{ config.extra.components_name }}**. It replaces Magento's Luma frontend with a modern stack —
**Twig** templates, **Vite**, **TailwindCSS 4**, and lazy-hydrated **Vue islands** — while keeping
Magento's native layouts, blocks, and view models. It is already functional and covers the same
ground as Luma (catalog, checkout, customer, search, cart, wishlist, compare, reviews, and sales).

[:material-open-in-new: See OBSIDIAN live]({{ config.extra.demo_url }}){ .md-button .md-button--primary target=_blank rel=noopener }

This page is a practical guide to **using and extending** the theme. For the underlying mechanism
shared by every compatible theme, see [Compatibility Themes](../components/themes/0010-overview.md).

!!! warning "Compatibility"

    - ✅ **Magento Open Source 2.4.6+** — supported today.
    - 🚧 **Adobe Commerce** and **Mage-OS** — not supported yet. Support is planned for the future.

---

## Architecture: two layers

The theme ships as two stacked themes so design is cleanly separated from plumbing:

<div class="grid cards" markdown>

-   :material-cube-outline:{ .lg .middle } __`MageObsidian/theme-base`__

    ---

    The neutral, technical foundation: build wiring and structural templates, **without** any
    design tokens. This is the parent you usually inherit from when starting a brand-new look.

    Package: `mage-obsidian/theme-base`

    [:material-github: View source]({{ config.extra.gh_theme_base_url }}){ .md-button }

-   :material-palette-swatch:{ .lg .middle } __`MageObsidian/default`__

    ---

    The **OBSIDIAN** skin: design tokens, styled Twig templates, and a replaceable apparel demo
    layer. Inherit from it when you want to keep OBSIDIAN and tweak; replace its tokens to rebrand.

    Package: `mage-obsidian/theme-default`

    [:material-github: View source]({{ config.extra.gh_theme_default_url }}){ .md-button }

</div>

The storefront logic — view models, legacy-layout neutralization, and shared Vue islands — lives in
the **[`mage-obsidian/module-storefront`]({{ config.extra.gh_storefront_url }})** repository, pulled
in automatically by `theme-base`.

Inheritance is declared with Magento's native `theme.xml`:

```xml
<theme xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:noNamespaceSchemaLocation="urn:magento:framework:Config/etc/theme.xsd">
    <title>MageObsidian — Default (Obsidian)</title>
    <parent>MageObsidian/theme-base</parent>
</theme>
```

A theme directory looks like this:

```text
app/design/frontend/MageObsidian/default/
├── theme.xml                         # title + parent
├── registration.php
├── etc/
│   └── mage_obsidian_compatibility.xml   # opt-in to the MageObsidian build
├── web/
│   ├── theme.config.js               # build options (ESM)
│   ├── css/
│   │   └── theme.source.css          # @theme design tokens + global styles
│   └── generated/                    # Vite build output (do not edit)
└── Magento_Theme/                    # per-module Twig overrides
    └── templates/
        └── html/
            ├── header.twig
            └── footer.twig
```

---

## Install & activate

1. Require the theme with Composer. `mage-obsidian/theme-default` pulls in `theme-base`, the
   modern-frontend engine, and the full storefront module stack (Luma-level parity) automatically:

    ```bash
    composer require mage-obsidian/theme-default
    bin/magento setup:upgrade
    ```

2. Select it in the Admin under **Stores → Configuration → General → Design → Design Theme**
   (or via `bin/magento config:set`), then apply it to your store view.
3. Regenerate the PHP ↔ JS contract so the build engine sees the theme:

    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

4. Build the frontend assets to disk:

    ```bash
    mage-obsidian:build-themes --theme <theme>   # omit --theme to build all
    ```

See [Installation](../getting-started/installation.md) for first-time setup.

---

## Develop with live reload (HMR)

For day-to-day work, run the Vite dev server so edits to `.vue`, CSS, and Twig hot-reload in the
browser. Enable HMR and wire nginx once, then start the server per session:

```bash
bin/magento deploy:mode:set developer
bin/magento mage-obsidian:frontend:hmr --enable                # once: HMR is a developer-mode flag
bin/magento mage-obsidian:frontend:dev --print-nginx           # once: paste the snippet into your nginx server block
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme   # per session
```

The nginx snippet proxies `/static` requests to the Vite dev server — host and port come from your
config, you don't hand-pick them. HMR is ignored in production mode. Full walkthrough and
troubleshooting in [HMR Configuration](../components/modules/0110-hmr-configuration.md) and
[Development Workflow](../getting-started/development.md).

---

## Deploy to production

There is **no separate build step**. MageObsidian hooks into Magento's standard static-content
deploy: its plugins exclude modern themes from the legacy Less/RequireJS pipeline and inject the
Vite output (minified, tree-shaken, hashed) as part of the normal command:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

Only themes shipping `etc/mage_obsidian_compatibility.xml` go through the Vite pipeline; everything
else follows Magento's native deploy untouched. See
[Building Static Assets](../components/modules/0120-vite-build.md).

---

## Re-theme it: design tokens

Re-skinning OBSIDIAN is **CSS-first**: every color, font, radius, and easing lives in the
`@theme` block of `web/css/theme.source.css`. Change these tokens and the whole theme follows —
no JavaScript config involved.

```css
@import "tailwindcss";

@theme {
  /* — Obsidian: vitreous near-black, cool violet undertone — */
  --color-obsidian-950: #08070b;
  --color-obsidian-900: #0d0c12;
  --color-obsidian-800: #16151d;

  /* — Alabaster: cool mineral light base (not warm cream) — */
  --color-alabaster: #eceaf0;
  --color-alabaster-raised: #f6f5f8;
  --color-paper: #ffffff;

  /* — Ink (text) + restrained functional accents — */
  --color-ink: #141319;
  --color-accent: #2f6e66;
  --color-sale: #9a5b3f;

  /* — Typography — */
  --font-display: "Bodoni Moda", Georgia, serif;
  --font-body: "Hanken Grotesk", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  /* — Sharpened conchoidal edge + signature easing — */
  --radius-edge: 2px;
  --ease-obsidian: cubic-bezier(0.22, 0.61, 0.36, 1);
}
```

Templates consume these as Tailwind utilities (`font-display`, `text-ink`, `bg-alabaster`,
`rounded-edge`, …), so editing a token re-flows every screen at once.

!!! tip "Don't edit `default` in place"

    To rebrand, create your own child theme (below) and override only the tokens you need. That
    keeps your changes upgrade-safe. For the full set of CSS options and module-CSS exclusion, see
    [CSS Configuration](../components/themes/0030-css-configuration.md).

---

## Build your own theme on top

Create a theme under `app/design/frontend/Vendor/Custom/` and inherit from `theme-base` (clean
slate) or `default` (keep OBSIDIAN and tweak):

!!! tip "`theme-base` or `default`?"

    Inherit from **`default`** when OBSIDIAN is close to what you want — retheme its tokens and
    override a few templates. It's the fastest path and you keep the styled, parity-complete
    storefront. Start from **`theme-base`** only when you want a clean slate and will design every
    surface from zero.

1. **`registration.php`** and **`theme.xml`** with the parent of your choice:

    ```xml
    <theme xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:noNamespaceSchemaLocation="urn:magento:framework:Config/etc/theme.xsd">
        <title>Acme — Storefront</title>
        <parent>MageObsidian/theme-base</parent>
    </theme>
    ```

2. **Opt in** to the MageObsidian build with `etc/mage_obsidian_compatibility.xml`:

    ```xml
    <?xml version="1.0"?>
    <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
        <features>
            <compatibility>true</compatibility>
        </features>
    </config>
    ```

3. **`web/theme.config.js`** — build options (ESM). Tokens go in CSS, not here:

    ```javascript
    export default {
        includeParentThemes: false,
        ignoredCssFromModules: [],
        exposeNpmPackages: [
            { package: 'pinia', exposePath: 'pinia' },
        ],
    }
    ```

4. **`web/css/theme.source.css`** — your `@theme` tokens (and any overrides).

Then run `--generate` and `mage-obsidian:build-themes` again. Full reference:
[Compatibility Configuration](../components/themes/0020-compatibility-configuration.md) and
[Theme Configuration](../components/themes/0040-theme-configuration.md).

---

## Override templates (Twig)

Templates live at `<Vendor>_<Module>/templates/**/*.twig`. To override one, recreate the same path
in your theme — Magento's fallback resolves the most specific version. For example, the page title:

{% raw %}
```twig
{# Page heading (<h1>). `block` is Magento\Theme\Block\Html\Title. #}
{% set heading = block.getPageHeading() %}
{% if heading|trim %}
<div class="page-title-wrapper mb-6{{ block.getCssClass() ? ' ' ~ block.getCssClass() }}">
    <h1 class="page-title font-display text-3xl leading-tight tracking-[0.01em] text-ink md:text-4xl">
        <span class="base" data-ui-id="page-title-wrapper" {{ block.getAddBaseAttribute()|raw }}>{{ heading }}</span>
    </h1>
    {{ child_html() }}
</div>
{% endif %}
```
{% endraw %}

Notice the design tokens surfacing as utility classes (`font-display`, `text-ink`). For the Twig
runtime, helpers, and filters, see [Twig Engine](../twig/index.md) and
[Helpers & Filters](../twig/helpers.md).

---

## Vue islands & JavaScript

The `default` theme mounts interactive **Vue islands** for the dynamic bits — header search,
cart / wishlist / compare counts, the mobile menu, the store switcher, drawers, and toasts — each
hydrated lazily so the page stays fast. You extend the theme by adding or overriding components and
exposing the NPM packages you need (Pinia is exposed out of the box).

- Add components and scripts under `web/` — see
  [Creating Scripts and Components](../components/themes/0050-components-workflow.md).
- Learn how islands are mounted in
  [Vue Islands](../components/modules/0105-vue-islands.md).

---

## What's included (Luma parity)

The theme covers the same storefront surface as Luma, rebuilt in Twig + Vue:

- **Chrome:** header, footer, navigation, mobile menu, store/currency switcher.
- **Catalog:** category listing, layered navigation, product detail page, swatches.
- **Purchase:** cart, checkout, instant purchase, gift messages, multishipping.
- **Account:** customer login & account, wishlist, compare, reviews, sales/orders.
- **Search:** quick search with autocomplete.

---

## Next steps

<div class="grid cards" markdown>

-   :material-puzzle-outline:{ .lg .middle } __Compatibility Themes__

    ---

    The full mechanism behind compatible themes: compatibility, CSS, config, and components.

    [:octicons-arrow-right-24: Overview](../components/themes/0010-overview.md)

-   :material-leaf:{ .lg .middle } __Twig Engine__

    ---

    Write and override templates in Twig, with helpers and filters.

    [:octicons-arrow-right-24: Explore Twig](../twig/index.md)

-   :material-rocket-launch:{ .lg .middle } __Getting started__

    ---

    Install the components and build a theme from scratch.

    [:octicons-arrow-right-24: Requirements](../getting-started/requirements.md)

</div>
