# Generadores

**{{ config.site_name }}** incluye generadores de `bin/magento` que crean módulos, temas y componentes Vue ya cableados para el frontend —de modo que el resolver los detecta sin configuración manual. Viven en el paquete `mage-obsidian/module-modern-frontend-cli`.

| Comando | Qué crea |
|---|---|
| `mage-obsidian:generate:module` | Un módulo nuevo en `app/code`, adherido al frontend. |
| `mage-obsidian:generate:theme` | Un tema de frontend nuevo en `app/design`, precableado. |
| `mage-obsidian:generate:component` | Un componente Vue single-file dentro de un módulo o tema. |

---

## Generar un Módulo

```bash
bin/magento mage-obsidian:generate:module Acme_Catalog
```

El nombre debe tener la forma `Vendor_Module`. Crea, bajo `app/code/Acme/Catalog/`:

- `registration.php`
- `etc/module.xml` (secuenciado después del core)
- `etc/mage_obsidian_compatibility.xml` (el opt-in del frontend)
- `view/frontend/web/module.config.js`

Un módulo es invisible para el stack de frontend hasta que entrega el archivo de compatibilidad, por eso se genera por defecto. Sigue los próximos pasos impresos para activarlo:

```bash
bin/magento module:enable Acme_Catalog
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
bin/magento mage-obsidian:generate:component <Name> --module=Acme_Catalog
```

| Opción | Descripción |
|---|---|
| `--force`, `-f` | Sobrescribe los archivos si ya existen. |

---

## Generar un Tema

```bash
bin/magento mage-obsidian:generate:theme Acme/aurora --parent=Magento/blank --title="Aurora"
```

El código debe tener la forma `Vendor/theme`. Crea, bajo `app/design/frontend/Acme/aurora/`:

- `registration.php`
- `theme.xml` (con el `<parent>` si se pasa `--parent`)
- `etc/mage_obsidian_compatibility.xml`
- `web/theme.config.js`
- `web/css/theme.source.css` (una fuente de Tailwind 4)
- `.gitignore`

| Opción | Descripción |
|---|---|
| `--parent` | Tema padre, p. ej. `Magento/blank`. |
| `--title` | Título legible del tema (por defecto, el código). |
| `--force`, `-f` | Sobrescribe archivos existentes. |

Luego actívalo en **Content → Design → Configuration** (o vía config) y regenera el contrato:

```bash
bin/magento mage-obsidian:frontend:config --generate
```

---

## Generar un Componente

Apunta a **exactamente uno** de módulo o tema:

```bash
# dentro de un módulo
bin/magento mage-obsidian:generate:component Button --module=Acme_Catalog

# dentro de un tema
bin/magento mage-obsidian:generate:component ProductCard --theme=Acme/aurora
```

El destino debe ser un módulo/tema **habilitado y compatible con el frontend**; de lo contrario el comando te indica que entregues el archivo de compatibilidad y ejecutes `mage-obsidian:frontend:config --generate`.

El componente se escribe siguiendo la convención del framework, así que el resolver lo encuentra sin registro:

- módulo → `view/frontend/web/components/<name>.vue`
- tema → `web/components/<name>.vue`

Funcionan las rutas anidadas (`elements/Button`), y un `components/` inicial o un `.vue` final en el nombre se normalizan. El comando imprime entonces cómo renderizarlo:

```php
$block->renderVueComponent('Acme_Catalog::Button');
```

(Para un destino de tema la referencia usa el namespace `Theme::`, p. ej. `Theme::ProductCard`.)

| Opción | Descripción |
|---|---|
| `--module` | Módulo destino (`Vendor_Module`). |
| `--theme` | Tema destino (`Vendor/theme`). |
| `--wire` | Genera además un stub `.phtml` que renderiza el componente. |
| `--force`, `-f` | Sobrescribe archivos existentes. |

### Cablear un stub phtml

Con `--wire`, el comando también escribe un `.phtml` que renderiza el nuevo componente e imprime un snippet de bloque de layout para colocarlo en un handle:

- módulo → `view/frontend/templates/<name>.phtml`
- tema → `Magento_Theme/templates/<name>.phtml`

```xml
<referenceContainer name="content">
    <block class="MageObsidian\ModernFrontend\Block\Template"
           name="acme.catalog.button"
           template="Acme_Catalog::button.phtml"/>
</referenceContainer>
```

---

## Ejemplo de Punta a Punta

```bash
# 1. Módulo nuevo, habilitado y compatible
bin/magento mage-obsidian:generate:module Acme_Catalog
bin/magento module:enable Acme_Catalog
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate

# 2. Un componente cableado con un stub phtml
bin/magento mage-obsidian:generate:component ProductCard --module=Acme_Catalog --wire

# 3. Agrega el <block> impreso a un handle de layout, luego haz build
```

El componente se renderiza como una [isla Vue](../components/modules/0105-vue-islands.md) de hidratación perezosa. Edita el `.vue` generado y el [watcher de desarrollo](../components/modules/0085-import-tooling.md#watcher-en-vivo-de-desarrollo) mantiene sincronizadas la resolución y el autocompletado del editor.
