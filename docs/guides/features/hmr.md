# HMR (Hot Module Replacement)

Hot Module Replacement (HMR) is a core feature of **MageObsidian** powered by Vite: it updates your frontend in the browser in real time, without a full reload. This page covers the HMR-specific pieces; for the full day-to-day loop (starting/stopping the server, syncing the env, diagnostics) see [Development Workflow](../../getting-started/development.md).

This is what it feels like — design tokens re-theme the page and a `.vue` template hot-swaps while the component keeps its state (the search panel never closes):

<video autoplay loop muted playsinline style="max-width:100%;border-radius:8px" src="/assets/hmr-live-edit-v2.mp4"></video>

---

> ⚠️ **Important Notice**
> HMR is a **development-only** feature. The HMR flag is ignored when Magento runs in **production** mode, so there is nothing to undo before going live.

---

## 1. Enable HMR

HMR is a Magento config flag, toggled with a command — no file editing:

```bash
bin/magento mage-obsidian:frontend:hmr --enable
bin/magento mage-obsidian:frontend:hmr --show      # check the current state
bin/magento mage-obsidian:frontend:hmr --disable   # turn it back off
```

Magento must also be in **developer mode** (`bin/magento deploy:mode:set developer`); in production the flag is ignored.

> **Tip:** `bin/magento mage-obsidian:frontend:dev --up` does this in one shot — developer mode, the HMR flag, the `.env` sync, the cache flush and the dev server — and `--down` reverses it. See [Development Workflow](../../getting-started/development.md).

## 2. Configure Nginx

The browser must reach the Vite dev server for HMR. Generate the proxy snippet derived from your configuration and paste it into your server block:

```bash
bin/magento mage-obsidian:frontend:dev --print-nginx
```

The snippet routes Vite's HMR traffic (WebSocket-aware) and the generated assets to the dev server, e.g.:

```nginx
location ~* ^/(?:@fs|@id|@vite|node_modules|__vite_ping|\.precompiled) {
    proxy_pass http://<vite-host>:<vite-port>;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}

location ~* ^/static/frontend/.+/.+/.+/vite_generated/(.*)$ {
    proxy_pass http://<vite-host>:<vite-port>/$1;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

Place these rules **below** your existing static-version rewrite (`location ~ ^/static/version\d*/ { ... }`). The host and port come from your MageObsidian config — you do not hand-pick them; `--print-nginx` fills them in.

## 3. Start the Dev Server

```bash
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme
```

This syncs the Vite `.env` from your Magento config and launches the dev server with HMR. Open your storefront — edits to a `.vue` component, a `module.extend.css`, or a theme source are reflected instantly. Stop it with `--stop`, check it with `--status`. See [Development Workflow](../../getting-started/development.md) for the complete command set.

## Multi-website with a shared theme

When the same theme is served on more than one website (different hosts), each host must reach the dev server over its **own** origin, or the secondary host gets `403` on Vite's assets and a "Vite dev server is not responding" banner.

- **`VITE_SERVER_ALLOWED_HOSTS`** — list every storefront host that serves the theme (comma-separated). Vite answers asset requests only for allowed hosts.
- **`MAGENTO_HOST`** — leave it **empty** for the multi-website case. The HMR websocket host is then derived from the browser's `window.location`, so each website opens a **same-origin** `wss` connection. Set a fixed value only when a proxy/tunnel forces one public host for all traffic.

## Troubleshooting

Run the doctor — it checks app mode, the HMR flag, dev-server reachability, the contract, and the env in one shot:

```bash
bin/magento mage-obsidian:frontend:doctor
```

Common causes when HMR "doesn't update":

- **HMR flag off or production mode** — `mage-obsidian:frontend:hmr --show`; the flag is ignored outside developer mode.
- **Nginx not proxying to Vite** — regenerate and re-paste the snippet with `--print-nginx`; confirm the dev server is reachable (`--status` / doctor).
- **Dev server not running** — `mage-obsidian:frontend:dev --status`, then `--start --theme=…`.

---

With HMR enabled and the proxy in place, you get instant CSS injection and component updates — no page reloads, no manual rebuilds.
