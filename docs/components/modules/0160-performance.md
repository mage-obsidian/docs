{% raw %}
# Performance & native build-config compatibility

**MageObsidian** serves every stylesheet and script through **Vite**, not Magento's legacy Less/RequireJS pipelines. That changes how the native build-configuration flags behave, and it opens one optional optimization worth understanding: the **critical CSS** path.

This page covers both: the opt-in critical-CSS feature, and how Magento's `dev/js/*`, `dev/css/*` and `dev/template/minify_html` flags interact with an Obsidian theme.

---

## Critical CSS (optional)

On an Obsidian theme the only render-blocking resource left in the head is the Vite stylesheet (`style.css`). The critical-CSS path inlines the above-the-fold CSS into the `<head>` and defers that stylesheet, so the first paint no longer waits for it.

It is **off by default** and **opt-in**.

### Reuses the native flag

There is **no MageObsidian-specific config**. The feature reuses Magento's own switch, `dev/css/use_css_critical_path` (off by default). When you turn it on, MageObsidian inlines the critical CSS for the current layout handle and defers the stylesheet.

### The defer is per-page, not global

Magento's native critical-path switch also activates `AsyncCssPlugin`, which rewrites **every** `<link rel="stylesheet">` in the response to an async (`media="print"`) load — globally. On any page that has **no** inlined critical CSS that produces a flash of unstyled content (FOUC).

MageObsidian avoids this:

- It **neutralizes `AsyncCssPlugin` for Obsidian themes only** (legacy and admin themes keep the native behaviour).
- It defers the stylesheet **per page**, in the head template, **coupled to whether critical CSS exists for the active handle**. A page with no critical CSS keeps the stylesheet render-blocking — never deferred without an inline counterpart, so there is never a FOUC.

### Generating the critical CSS

The critical CSS is extracted from the **real rendered page** (so it reflects the actual above-the-fold markup) with [Beasties](https://github.com/danielroe/beasties), by a console command:

```bash
bin/magento mage-obsidian:frontend:critical-css --handle cms_index_index
```

The command renders the URL, extracts the critical subset, rewrites the `@font-face` `url(...)` to an absolute (root-relative) static URL so the self-hosted fonts resolve once inlined in `<head>`, and writes `web/generated/critical/<handle>.css` in the active theme. Run it **after** the theme build and `setup:static-content:deploy`, because it reads the built stylesheet and resolves the deployed static URLs.

| Option | Default | Purpose |
|---|---|---|
| `--handle` | `cms_index_index` | Layout handle the critical CSS is for. |
| `--url` | store secure base URL | The page to render. |
| `--store` | default store view | Store to emulate. |
| `--insecure` | off | Skip TLS verification (self-signed dev certs). |
| `--resolve` | — | A curl `host:port:ip` entry, for local setups behind a custom host. |
| `--node` / `--bin` | `node` / shipped bin | Override the Node binary or the extractor script. |

### Which pages to cover — it depends on your traffic

Critical CSS is generated **per layout handle** — one file per handle, and only pages whose handle has a generated file get the inline treatment. It is not a global switch; think of it as a per-entry-page optimization:

- The benefit concentrates on the **first page of a visit, with a cold cache**. From the second page on, `style.css` is already in the browser cache and the render-blocking request costs close to nothing.
- If visitors mostly enter through the home page, the default `cms_index_index` covers most of the win.
- If organic search or ads land visitors **directly on products and categories**, those are first pages too — generate their handles as well:

```bash
bin/magento mage-obsidian:frontend:critical-css --handle catalog_product_view --url https://store.example/a-product.html
bin/magento mage-obsidian:frontend:critical-css --handle catalog_category_view --url https://store.example/a-category.html
```

One granularity caveat: a handle's critical CSS is extracted from **one representative page** and applied to every page sharing that handle (all product pages share `catalog_product_view`). The above-the-fold structure is normally identical across them; anything a specific page needs beyond the extract simply arrives with the deferred stylesheet — correctness is guaranteed, the optimization is partial.

Any handle without a generated file degrades to the render-blocking stylesheet.

### Regenerate on every deploy

`web/generated/critical/` is **build output, not shipped source**: a `composer update` of the theme — or any deploy that replaces it — wipes the generated files. Bake the generation into your deploy pipeline as its **last step**, once the site is already serving the new release (caches flushed, PHP-FPM restarted):

```text
setup:static-content:deploy  →  cache:flush + restart FPM  →  critical-css (per handle)  →  cache:clean full_page
```

Generating earlier extracts the CSS from the *previous* release — or fails outright against a half-deployed site. The final `cache:clean full_page` matters because pages cached before the file existed were rendered with the fallback stub.

### Read-only infrastructure (Adobe Commerce Cloud)

The generated file is written into the active theme's directory, which is **read-only at runtime** on Adobe Commerce Cloud and similar immutable deployments — while generation needs the live site, which only exists after the build phase. On those platforms, leave `dev/css/use_css_critical_path` off for now: pages stay correct with the render-blocking stylesheet. A runtime-writable storage location (so generation can run in a `post_deploy` hook) is under consideration.

### Enabling it

```bash
bin/magento config:set dev/css/use_css_critical_path 1
bin/magento mage-obsidian:frontend:critical-css --handle cms_index_index
bin/magento cache:flush
```

The flag is scoped per store view. If the generated file is missing or unreadable, the head falls back to a tiny `[v-cloak]` stub and the normal render-blocking stylesheet — the page is always correct.

### When not to use it

Critical CSS is a trade-off: it inlines CSS into every cached page (more HTML) to remove one render-blocking request. If a project does not want it, **leave `dev/css/use_css_critical_path` off** — the stylesheet stays render-blocking, which behind Varnish with gzip/brotli and HTTP/2 already loads in tens of milliseconds. Nothing else needs to change.

---

## Native build-config flags

### JS/CSS merge & minify — inert

`dev/js/merge_files`, `dev/js/minify_files`, `dev/css/merge_css_files`, `dev/css/minify_files` have **no effect** on an Obsidian theme. Those flags act on Magento's `AssetCollection`; MageObsidian emits its CSS and JS straight from Vite output (the importmap, the `<link>`, the `<script type="module">`), which never enters that collection. You can leave them at any value — minification and bundling are already handled by the Vite build.

### HTML minification — disabled per theme

`dev/template/minify_html` is **turned off for Obsidian themes** (admin and legacy themes still minify). Two reasons:

- In production, with neither `force_html_minification` nor SCD-on-demand set, Magento returns the path to a pre-generated `.min` template **without creating it**; that file never exists for the Vite/Twig pipeline, so the include fails with HTTP 500.
- The regex minifier can corrupt the inline JSON the runtime emits — island `data-props`, the importmap, JSON-LD — which is risky for no real gain (Varnish + gzip/brotli already collapse whitespace; the post-compression delta is ~1–3%).

You can leave the flag on globally; the storefront is unaffected.
{% endraw %}
