# Content Security Policy

Under an Obsidian theme, `script-src` and `style-src` carry no `'unsafe-inline'`. An injected `<script>` does not run unless the policy authorizes it, which makes the policy the main barrier against stored XSS. This page explains how the storefront keeps that barrier standing on the pages the full-page cache serves.

---

## How inline code is authorized

A policy can authorize an inline `<script>` in two ways:

- **Nonce:** a random value the response declares in its header and repeats on each script. It protects only while it is secret and different on every response.
- **Hash:** the sha256 of the script's exact content, listed in the header. It is not a secret, so a cache can store and share it.

A page in the full-page cache is the same response for every visitor. Under Varnish or Fastly, a nonce stored with the page is shared by everyone until the TTL expires, and anyone who reads it in their own response knows it for every visitor. Under Magento's built-in page cache, a cache hit rebuilds the header without the nonce at all, and the page's own scripts are blocked.

MageObsidian therefore picks the method per response:

| Response | Inline scripts are authorized by |
|---|---|
| May be stored in the full-page cache (the default for catalog, CMS and search pages) | the sha256 of their content |
| Certainly not stored: page cache disabled, a layout declared non-cacheable (cart, checkout, account), or a request other than GET and HEAD | a nonce generated for that response |
| Rendered into the block cache | the sha256 of their content, whatever the response, because that HTML can be served later on a cacheable page |

When in doubt, the hash wins: a hash on a response that is never cached costs nothing, while a nonce on a cached response is shared by every visitor.

ESI blocks follow the page that includes them. Magento renders a block with a TTL during the main request before it swaps it for `<esi:include>`, so its hashes are already in the header the visitor receives.

The runtime configuration the server hands to the storefront (translations, section data, UX flags, icon base, pre-paint) travels as JSON data blocks, `<script type="application/json" data-mage-obsidian-config="…">`. The browser does not execute them, so the policy has nothing to authorize, and the inline code that remains has the same hash in every store view of a deployment.

## Magento's built-in page cache

Varnish and Fastly store the policy header together with the page. Magento's built-in page cache does not: it stores the page before the header exists and rebuilds the header on every hit. MageObsidian therefore stores, with each built-in cache entry, every authorization the page collected while it rendered: hashes, nonces, hosts, schemes and event-handler permissions. A hit puts them back before Magento writes the header, so the header a visitor receives matches the one of the response that was stored. The stored copy travels in a private header of the cache entry and never reaches the browser.

An entry stored before this behaviour existed carries no such copy. MageObsidian treats it as absent and renders the page once more, so the store never serves a page whose header would block its own scripts, even if nobody cleans the cache after upgrading.

### When you upgrade

- Rebuild the theme. The static content deploy does it.
- Run `bin/magento cache:clean full_page block_html`. Blocks cached before the upgrade can carry an old nonce in their HTML.
- Purge Varnish or Fastly. Pages cached before the upgrade carry the nonce every visitor shares until their TTL expires.

### If you roll back

Go back to the previous version and run `bin/magento cache:clean full_page`. Without the clean, the previous code serves the private header stored in the newer entries. It is harmless, because it only lists hashes and hosts the policy header already publishes, but it adds noise to the response.

## The recommended policy

Under an Obsidian theme, MageObsidian applies a recommended policy on top of the final policy of every storefront response. It is on by default, on a new install and on a store that upgrades:

- enforce mode, even when the store configuration asks for report-only;
- no `'unsafe-eval'` in any directive;
- no `'unsafe-inline'` in `script-src`, `style-src` or `default-src`, except in `style-src` on a page a module declared for inline styles (see [Payment pages](#payment-pages));
- `base-uri 'self'` and `object-src 'none'`, replacing whatever was collected for them.

It runs after every collector, including the authorizations modules add while the page renders, so a template that adds `'unsafe-inline'` to `script-src` during the render does not get it into the header. Hosts, schemes, hashes and nonces are kept.

While the Vite dev server is on, the policy stays in report-only, so the dev server's own inline client and assets keep working. The dev server is always off in production mode.

### Upgrading a store in report-only

Magento sends the storefront policy in report-only by default, so most stores block nothing today. With this version the browser starts blocking whatever the policy does not authorize: an inline `<script>` written by hand in a template, an `on*=` attribute written in markup, and any `eval`. Before upgrading production, open the pages that matter in a staging copy with the browser console open: every blocked script or style is listed there. Move what is blocked to the secure renderer, as [a third-party module should](#what-a-third-party-module-should-do).

### Turning it off

No admin setting turns it off: relaxing the storefront's security goes through code review. A module turns it off in its `etc/frontend/di.xml`:

```xml
<type name="MageObsidian\ModernFrontend\Service\Csp\RecommendedPolicy">
    <arguments>
        <argument name="enabled" xsi:type="boolean">false</argument>
    </arguments>
</type>
```

Then run `bin/magento setup:di:compile` and `bin/magento cache:clean full_page`. The policy goes back to what Magento's configuration and the store's own produce, with MageObsidian's inline script and style hardening still applied.

### Why `form-action` is left as Magento declares it

Magento and the payment modules declare `form-action` as `'self'` plus the hosts of the payment providers. The recommended policy does not reduce it to `'self'`: Chrome also applies `form-action` to the redirects that follow a form submission, and PayPal Express and 3-D Secure redirect to the provider after a POST. A store that has tested every payment flow can tighten it through Magento's own `csp/policies/storefront/forms` configuration.

### Varnish and the size of the header

Each distinct inline script adds about 55 bytes to the policy header. Varnish refuses a backend response with a header longer than `http_resp_hdr_len`, 8 KB by default, and the visitor gets a 503. The storefront's own pages send about 5 KB of policy, and the verification suite fails any page over 8192 bytes. If your modules push a page past the limit, raise it in the Varnish start parameters, together with the total it has to fit in:

```
-p http_resp_hdr_len=16k -p http_resp_size=64k
```

## Payment pages

Magento's own configuration lets any inline style through on the checkout and on the multishipping billing step. MageObsidian does not: both pages forbid unauthorized inline styles like the rest of the storefront, and the styles the storefront emits there are authorized by hash. An order completes with check / money order, bank transfer and purchase order, and with reCAPTCHA on the payment step, without a single violation.

A payment method that injects its own `<style>` element is blocked. Before upgrading a store that takes payments, place a test order with every payment method it runs. If one of them needs inline styles, prefer authorizing the exact content it injects by its hash, in a `csp_whitelist.xml`. When that content changes on every load, the module that integrates the payment method can declare the page in its `etc/frontend/di.xml`:

```xml
<type name="MageObsidian\ModernFrontend\Plugin\Csp\ApplyStrictInlinePolicy">
    <arguments>
        <argument name="inlineStylePages" xsi:type="array">
            <item name="checkout" xsi:type="string">checkout_index_index</item>
        </argument>
    </arguments>
</type>
```

That page gets `'unsafe-inline'` back in `style-src`, the recommended policy keeps it there, and every other page stays strict. On a declared page MageObsidian stops hashing its own styles, because a browser ignores `'unsafe-inline'` as soon as the directive lists a hash. On that page, a `csp/policies/storefront_<action>/styles` value the store set itself, in `config.xml` or `env.php`, still decides.

There is no admin setting for this, on purpose: allowing inline styles lets injected markup restyle the page, and that decision goes through code review. No store configuration allows inline styles on a page the code did not declare.

## What a third-party module should do

Emit inline scripts and styles through Magento's `SecureHtmlRenderer`:

```php
echo $secureRenderer->renderTag('script', [], $javascript, false);
```

MageObsidian intercepts the same `InlineUtil` the renderer uses, so the module needs no change to be authorized by hash on cacheable pages. A `<script>` written by hand in a template is not authorized at all and stays blocked.

Two practices keep the header small and stable:

- Keep values that change per page out of inline code. Put them in a data attribute or a JSON data block and read them from the script.
- Never put visitor-specific data in an inline script on a cacheable page. That was a leak before this policy and remains one.

## The nonce some components still ask for

A component can ask Magento for the nonce directly instead of going through the renderer. The PayPal and Payment Services SDKs do this to inject their own scripts. MageObsidian does not take that nonce away, because the button would stop working. On a cacheable page such as the product page, that nonce is still shared by every visitor, exactly as before. The storefront verification suite lists the cacheable pages whose header carries a nonce, so this residual risk stays visible.
