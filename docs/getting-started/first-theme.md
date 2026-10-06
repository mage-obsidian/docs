---
description: Create a child theme of OBSIDIAN, change a color token, override a Vue component and see both on the storefront.
---

# Your first child theme

{{ verified('first-theme') }}

You will create `Acme/child`, a theme that inherits from `MageObsidian/default` (OBSIDIAN), change its accent color, override one Vue component, build it and see both changes on the home page. Every command and output below comes from running this tutorial end to end on a store. The last step removes everything the tutorial created and was checked on that store: the home page answers `200` with the same nine islands as before.

Commands are shown as `bin/magento …` from the Magento root. On a zento project, prefix them with `zento magento` and run them from the project root.

## 1. Generate the theme

```bash
bin/magento mage-obsidian:generate:theme Acme/child \
  --parent=MageObsidian/default --title="Child"
```

```text
 [!] Theme Acme/child created at /var/www/html/app/design/frontend/Acme/child

  Files generated
  registration.php
  theme.xml
  etc/mage_obsidian_compatibility.xml
  web/theme.config.js
  web/css/theme.source.css
  .gitignore

 Next steps:
     Activate the theme in Content > Design > Configuration (or via config),
     then: bin/magento mage-obsidian:frontend:config --generate
```

`theme.xml` now declares `<parent>MageObsidian/default</parent>`, and `etc/mage_obsidian_compatibility.xml` opts the theme into the frontend build. The options are in [Scaffolding](scaffolding.md#generate-a-theme).

## 2. Activate it

Magento registers a new theme during `setup:upgrade`:

```bash
bin/magento setup:upgrade --keep-generated
```

```text
Upgrade completed successfully.
```

Themes are identified by the id the `theme` table gives them, which differs from store to store. Read the ids of the child and of OBSIDIAN (on zento, with `zento mysql`):

```sql
SELECT theme_id, theme_path FROM theme
WHERE area = 'frontend' AND theme_path IN ('Acme/child', 'MageObsidian/default');
```

```text
theme_id	theme_path
6	MageObsidian/default
9	Acme/child
```

Then open **Content → Design → Configuration**, edit the row for your store view or the global row, and pick **Child** as the applied theme. The same setting from the command line is `design/theme/theme_id`, set to the id of `Acme/child` (`<child-id>`; 9 on the store used here) at the default scope:

```bash
bin/magento config:set design/theme/theme_id <child-id>
```

```text
Value was saved.
```

If you applied the theme at store-view scope in the admin, undo it there, or pass `--scope=stores --scope-code=<code>` to `config:set` in step 7.

## 3. Change a color token

OBSIDIAN defines its colors as Tailwind 4 tokens in its own `theme.source.css`, among them `--color-accent: #2f6e66`. The child's `theme.source.css` is loaded after the parent's, so redefining the token in the child wins. Edit `app/design/frontend/Acme/child/web/css/theme.source.css`:

```css
@import "tailwindcss";

@theme {
  --color-accent: #b4232a;
}
```

## 4. Override a Vue component

A theme overrides a module's file by recreating its path under a folder named after the module. The header cart badge is `MageObsidian_Storefront::cart/CartCount`. Copy the module's component into the child and change only the icon name:

```bash
mkdir -p app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart
cp vendor/mage-obsidian/module-storefront/src/view/frontend/web/components/cart/CartCount.vue \
   app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart/CartCount.vue
sed -i 's/name="shopping-bag"/name="shopping-cart"/' \
   app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart/CartCount.vue
```

The copy differs from the original by one line, which keeps the badge rules, the syncing ring and the accessible label of the original:

```diff
-        <Icon name="shopping-bag" set="outline" class="h-5 w-5" />
+        <Icon name="shopping-cart" set="outline" class="h-5 w-5" />
```

Cross-module imports inside the file use `Vendor_Module::path`, never a relative path, so the override stays reachable for children of your theme.

The server renders the first frame of this island from a template of OBSIDIAN, and that markup must match the component, or the bag icon would show until Vue mounts. Override the template in the child with the same icon change:

```bash
THEME_SRC=$(ls -d vendor/mage-obsidian/theme-default \
  app/design/frontend/MageObsidian/default 2>/dev/null | head -1)
mkdir -p app/design/frontend/Acme/child/Magento_Theme/templates/html/header
cp "$THEME_SRC"/Magento_Theme/templates/html/header/cart-count.twig \
   app/design/frontend/Acme/child/Magento_Theme/templates/html/header/cart-count.twig
sed -i "s/hero_icon('shopping-bag'/hero_icon('shopping-cart'/" \
   app/design/frontend/Acme/child/Magento_Theme/templates/html/header/cart-count.twig
```

OBSIDIAN lives in `vendor/mage-obsidian/theme-default` on a store installed with Composer, and in `app/design/frontend/MageObsidian/default` on a store where it is a checkout; the first command picks whichever exists.

## 5. Regenerate the contract and build

```bash
bin/magento mage-obsidian:frontend:config --generate
```

```text
 ===========================================================
  /var/www/html/app/etc/mage_obsidian_frontend_modules.php
  /var/www/html/app/etc/mage_obsidian_frontend_modules.json
 ===========================================================
```

The contract is a PHP file, and PHP-FPM with `opcache.validate_timestamps=0` (the usual production setting, and the zento default) does not re-read it. Until PHP-FPM is reloaded, the web tier does not know the child exists, treats it as a legacy theme and drops the header's cart, account and search islands. Reload PHP-FPM or reset its opcache. On zento:

```bash
zento compose restart php php-noxdebug
```

Check that the contract lists the theme:

```bash
bin/magento mage-obsidian:frontend:config --show --themes
```

```text
 ========================= ===========================================================
  Theme                     Path
 ========================= ===========================================================
  MageObsidian/default      /var/www/html/app/design/frontend/MageObsidian/default
  MageObsidian/theme-base   /var/www/html/app/design/frontend/MageObsidian/theme-base
  Acme/child                /var/www/html/app/design/frontend/Acme/child
 ========================= ===========================================================
```

Then build it, from the `vite/` folder of the Magento root:

```bash
pnpm build:theme Acme/child
```

```text
✓ built in 1.29s
✓ Acme/child built
```

Flush the cache so the store picks up the new theme:

```bash
bin/magento cache:flush
```

## 6. See it on the home page

```bash
curl -sk -o home.html -w "%{http_code}\n" https://your-store.test/
```

```text
200
```

The page loads its assets from the child:

```bash
grep -o 'frontend/[A-Za-z-]*/[a-z-]*' home.html | sort | uniq -c
```

```text
     40 frontend/Acme/child
```

It also keeps every island OBSIDIAN renders: the header's `MiniCart`, `AccountMenu` and `SearchAutocomplete` are all there, and the page mounts nine islands, the same number as with `MageObsidian/default`:

```bash
for n in MiniCart AccountMenu SearchAutocomplete; do
  grep -c "$n" home.html
done
grep -o 'data-mage-island data-component' home.html | wc -l
```

```text
1
1
1
9
```

The server-rendered first frame already uses the cart icon:

```bash
grep -o 'heroicons/24/outline/shopping-[a-z]*' home.html
```

```text
heroicons/24/outline/shopping-cart
```

Fetch the built files and look for both changes:

```bash
ASSETS='https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated'
curl -sk "$ASSETS/css/style.css" | grep -o -- '--color-accent:[^;]*' | head -1
curl -sk "$ASSETS/MageObsidian_Storefront/components/cart/CartCount.js" \
  | grep -o 'shopping-[a-z]*' | sort -u
```

```text
--color-accent:#b4232a
shopping-cart
```

`<version>` is the number in the asset URLs of `home.html`. Opened in a browser (here, headless Chrome), the header shows the cart icon in place of the bag.

## 7. Undo the tutorial

Skip this if you are keeping the theme. To put the store back, reactivate OBSIDIAN, remove everything the tutorial created, regenerate the contract and reload PHP-FPM.

Reactivate OBSIDIAN with its id, `<default-id>` in step 2 (6 on the store used here):

```bash
bin/magento config:set design/theme/theme_id <default-id>
```

Before any `rm` on a project that mounts folders into a container, confirm that none of the paths you are about to delete is a mount, or contains one. On zento:

```bash
zento cli cat /proc/self/mountinfo | grep /var/www/html | awk '{print $5}'
```

```text
/var/www/html
/var/www/html/vite
/var/www/html/app/etc/config.php
/var/www/html/app/code/Development/AdminBypass
/var/www/html/app/code/Development/Core
/var/www/html/app/code/Development/CustomerBypass
/var/www/html/app/code/Development/LiveReload
/var/www/html/app/code/Development/McpDevTools
/var/www/html/app/code/MageObsidian/Search
/var/www/html/app/code/MageObsidian/Showcase
/var/www/html/app/design/frontend/MageObsidian/theme-base
```

None of `app/design/frontend/Acme`, `pub/static/frontend/Acme` or `vite/.precompiled/Acme` appears. `vite` does appear: it is a mount, so delete only the `Acme` folder inside `.precompiled`, never `vite` itself.

Then remove the theme sources, the deployed static files and the build cache:

```bash
rm -rf app/design/frontend/Acme pub/static/frontend/Acme vite/.precompiled/Acme
```

`theme:uninstall` does not remove a theme that was not installed with Composer, so its row stays in the `theme` table. Delete it only when nothing references it. Each of these, with your `<child-id>`, must return `0`:

```sql
SELECT COUNT(*) FROM design_config_grid_flat WHERE theme_theme_id = <child-id>;
SELECT COUNT(*) FROM core_config_data WHERE path LIKE 'design/%' AND value = '<child-id>';
SELECT COUNT(*) FROM theme_file WHERE theme_id = <child-id>;
SELECT COUNT(*) FROM theme WHERE parent_id = <child-id>;
```

Then delete the row, regenerate the contract, reload PHP-FPM again and flush the cache:

```sql
DELETE FROM theme WHERE theme_path = 'Acme/child' AND area = 'frontend';
```

```bash
bin/magento mage-obsidian:frontend:config --generate
zento compose restart php php-noxdebug
bin/magento cache:flush
```

The store is back as it was when the same checks as in step 6 pass for OBSIDIAN: the home page answers `200`, no `Acme` appears in the page or in `--show --themes`, and the page mounts nine islands:

```bash
curl -sk -o home.html -w "%{http_code}\n" https://your-store.test/
grep -c Acme home.html
grep -o 'data-mage-island data-component' home.html | wc -l
```

```text
200
0
9
```

## Where to go next

- [Theme configuration](../guides/themes/configuration.md) and [CSS](../guides/themes/css.md): the files a theme can ship.
- [Components](../guides/themes/components.md): scripts and Vue components in a theme.
