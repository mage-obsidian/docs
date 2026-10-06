---
description: Crea un tema hijo de OBSIDIAN, cambia un token de color, sobrescribe un componente Vue y comprueba ambos cambios en la tienda.
---

# Tu primer tema hijo

{{ verified('first-theme') }}

Vas a crear `Acme/child`, un tema que hereda de `MageObsidian/default` (OBSIDIAN), cambiar su color de acento, sobrescribir un componente Vue, compilarlo y ver ambos cambios en la página de inicio. Cada comando y cada salida de abajo proviene de ejecutar este tutorial de principio a fin en una tienda. El último paso elimina todo lo que el tutorial creó y se comprobó en esa tienda: la página de inicio responde `200` con las mismas nueve islas de antes.

Los comandos se muestran como `bin/magento …` desde la raíz de Magento. En un proyecto zento, antepón `zento magento` y ejecútalos desde la raíz del proyecto.

## 1. Genera el tema

```bash
bin/magento mage-obsidian:generate:theme Acme/child --parent=MageObsidian/default --title="Child"
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

`theme.xml` declara ahora `<parent>MageObsidian/default</parent>` y `etc/mage_obsidian_compatibility.xml` incorpora el tema al build del frontend. Las opciones están en [Scaffolding](scaffolding.md#generar-un-tema).

## 2. Actívalo

Magento registra un tema nuevo durante `setup:upgrade`:

```bash
bin/magento setup:upgrade --keep-generated
```

```text
Upgrade completed successfully.
```

Los temas se identifican por el id que les da la tabla `theme`, y ese id cambia de una tienda a otra. Lee los ids del hijo y de OBSIDIAN (en zento, con `zento mysql`):

```sql
SELECT theme_id, theme_path FROM theme WHERE area = 'frontend' AND theme_path IN ('Acme/child', 'MageObsidian/default');
```

```text
theme_id	theme_path
6	MageObsidian/default
9	Acme/child
```

Luego abre **Content → Design → Configuration**, edita la fila de tu vista de tienda o la global y elige **Child** como tema aplicado. El mismo ajuste por línea de comandos es `design/theme/theme_id`, con el id de `Acme/child` (`<child-id>`; 9 en la tienda usada aquí) en el ámbito por defecto:

```bash
bin/magento config:set design/theme/theme_id <child-id>
```

```text
Value was saved.
```

Si aplicaste el tema en el ámbito de vista de tienda desde el admin, deshazlo allí, o pasa `--scope=stores --scope-code=<código>` a `config:set` en el paso 7.

## 3. Cambia un token de color

OBSIDIAN define sus colores como tokens de Tailwind 4 en su propio `theme.source.css`, entre ellos `--color-accent: #2f6e66`. El `theme.source.css` del hijo se carga después del padre, así que redefinir el token en el hijo gana. Edita `app/design/frontend/Acme/child/web/css/theme.source.css`:

```css
@import "tailwindcss";

@theme {
  --color-accent: #b4232a;
}
```

## 4. Sobrescribe un componente Vue

Un tema sobrescribe un archivo de un módulo recreando su ruta bajo una carpeta con el nombre del módulo. El indicador del carrito en el encabezado es `MageObsidian_Storefront::cart/CartCount`. Copia el componente del módulo en el hijo y cambia solo el nombre del icono:

```bash
mkdir -p app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart
cp vendor/mage-obsidian/module-storefront/src/view/frontend/web/components/cart/CartCount.vue \
   app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart/CartCount.vue
sed -i 's/name="shopping-bag"/name="shopping-cart"/' \
   app/design/frontend/Acme/child/MageObsidian_Storefront/web/components/cart/CartCount.vue
```

La copia se diferencia del original en una sola línea, así que conserva las reglas del indicador, el anillo de sincronización y la etiqueta accesible del original:

```diff
-        <Icon name="shopping-bag" set="outline" class="h-5 w-5" />
+        <Icon name="shopping-cart" set="outline" class="h-5 w-5" />
```

Las importaciones entre módulos dentro del archivo usan `Vendor_Module::path`, nunca una ruta relativa, para que la sobrescritura siga siendo alcanzable por los hijos de tu tema.

El servidor renderiza el primer fotograma de esta isla desde una plantilla de OBSIDIAN, y ese marcado debe coincidir con el componente; si no, se vería la bolsa hasta que Vue monte. Sobrescribe la plantilla en el hijo con el mismo cambio de icono:

```bash
mkdir -p app/design/frontend/Acme/child/Magento_Theme/templates/html/header
cp app/design/frontend/MageObsidian/default/Magento_Theme/templates/html/header/cart-count.twig \
   app/design/frontend/Acme/child/Magento_Theme/templates/html/header/cart-count.twig
sed -i "s/hero_icon('shopping-bag'/hero_icon('shopping-cart'/" \
   app/design/frontend/Acme/child/Magento_Theme/templates/html/header/cart-count.twig
```

## 5. Regenera el contrato y compila

```bash
bin/magento mage-obsidian:frontend:config --generate
```

```text
 ===========================================================
  /var/www/html/app/etc/mage_obsidian_frontend_modules.php
  /var/www/html/app/etc/mage_obsidian_frontend_modules.json
 ===========================================================
```

El contrato es un archivo PHP, y PHP-FPM con `opcache.validate_timestamps=0` (el ajuste habitual en producción y el valor por defecto de zento) no lo vuelve a leer. Mientras no se recargue PHP-FPM, la capa web no sabe que el hijo existe, lo trata como un tema legacy y descarta las islas del carrito, la cuenta y la búsqueda del encabezado. Recarga PHP-FPM o reinicia su opcache. En zento:

```bash
zento compose restart php php-noxdebug
```

Comprueba que el contrato lista el tema:

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

Luego compílalo, desde la carpeta `vite/` de la raíz de Magento:

```bash
pnpm build:theme Acme/child
```

```text
✓ built in 1.29s
✓ Acme/child built
```

Vacía la caché para que la tienda tome el tema nuevo:

```bash
bin/magento cache:flush
```

## 6. Míralo en la página de inicio

```bash
curl -sk -o home.html -w "%{http_code}\n" https://your-store.test/
```

```text
200
```

La página carga sus assets desde el hijo:

```bash
grep -o 'frontend/[A-Za-z-]*/[a-z-]*' home.html | sort | uniq -c
```

```text
     40 frontend/Acme/child
```

También conserva todas las islas que renderiza OBSIDIAN: `MiniCart`, `AccountMenu` y `SearchAutocomplete` del encabezado están presentes, y la página monta nueve islas, el mismo número que con `MageObsidian/default`:

```bash
for n in MiniCart AccountMenu SearchAutocomplete; do grep -c "$n" home.html; done
grep -o 'data-mage-island data-component' home.html | wc -l
```

```text
1
1
1
9
```

El primer fotograma renderizado en el servidor ya usa el icono de carrito:

```bash
grep -o 'heroicons/24/outline/shopping-[a-z]*' home.html
```

```text
heroicons/24/outline/shopping-cart
```

Descarga los archivos compilados y busca ambos cambios:

```bash
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/css/style.css | grep -o -- '--color-accent:[^;]*' | head -1
curl -sk https://your-store.test/static/<version>/frontend/Acme/child/en_US/generated/MageObsidian_Storefront/components/cart/CartCount.js | grep -o 'shopping-[a-z]*' | sort -u
```

```text
--color-accent:#b4232a
shopping-cart
```

`<version>` es el número que aparece en las URL de assets de `home.html`. Abierta en un navegador (aquí, Chrome sin interfaz), la cabecera muestra el icono de carrito en lugar de la bolsa.

## 7. Deshaz el tutorial

Omite este paso si te quedas con el tema. Para devolver la tienda a su estado, reactiva OBSIDIAN, elimina todo lo que creó el tutorial, regenera el contrato y recarga PHP-FPM.

Reactiva OBSIDIAN con su id, `<default-id>` en el paso 2 (6 en la tienda usada aquí):

```bash
bin/magento config:set design/theme/theme_id <default-id>
```

Antes de cualquier `rm` en un proyecto que monta carpetas en un contenedor, confirma que ninguna de las rutas que vas a borrar es un montaje ni contiene uno. En zento:

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

Ninguna de `app/design/frontend/Acme`, `pub/static/frontend/Acme` ni `vite/.precompiled/Acme` aparece. `vite` sí aparece: es un montaje, así que borra solo la carpeta `Acme` dentro de `.precompiled`, nunca `vite`.

Luego elimina las fuentes del tema, los archivos estáticos desplegados y la caché del build:

```bash
rm -rf app/design/frontend/Acme pub/static/frontend/Acme vite/.precompiled/Acme
```

`theme:uninstall` no elimina un tema que no se instaló con Composer, así que su fila queda en la tabla `theme`. Elimínala solo cuando nada la referencie. Cada una de estas consultas, con tu `<child-id>`, debe devolver `0`:

```sql
SELECT COUNT(*) FROM design_config_grid_flat WHERE theme_theme_id = <child-id>;
SELECT COUNT(*) FROM core_config_data WHERE path LIKE 'design/%' AND value = '<child-id>';
SELECT COUNT(*) FROM theme_file WHERE theme_id = <child-id>;
SELECT COUNT(*) FROM theme WHERE parent_id = <child-id>;
```

Después elimina la fila, regenera el contrato, vuelve a recargar PHP-FPM y vacía la caché:

```sql
DELETE FROM theme WHERE theme_path = 'Acme/child' AND area = 'frontend';
```

```bash
bin/magento mage-obsidian:frontend:config --generate
zento compose restart php php-noxdebug
bin/magento cache:flush
```

La tienda está como estaba cuando las mismas comprobaciones del paso 6 pasan para OBSIDIAN: la página de inicio responde `200`, no aparece `Acme` en la página ni en `--show --themes`, y la página monta nueve islas:

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

## Siguientes pasos

- [Configuración del tema](../guides/themes/configuration.md) y [CSS](../guides/themes/css.md): los archivos que puede incluir un tema.
- [Componentes](../guides/themes/components.md): scripts y componentes Vue en un tema.
