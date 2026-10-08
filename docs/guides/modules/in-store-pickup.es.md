---
description: "Ofrece la recogida en tienda en el checkout de MageObsidian con el paquete opcional module-inventory-in-store-pickup y añade tu propio renderizador de transportista."
---
# Recogida en tienda

`mage-obsidian/module-inventory-in-store-pickup` añade al checkout la recogida en tienda de Magento (Multi-Source Inventory): la elección entre envío a una dirección y recogida en una tienda, y un buscador del punto de recogida. Es opcional y `theme-base` no lo exige, así que una tienda sin MSI nunca lo instala.

## Instalación

```bash
composer require mage-obsidian/module-inventory-in-store-pickup
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
```

Después recompila el tema. El paquete necesita los módulos de recogida de MSI (`Magento_InventoryInStorePickupApi` y `Magento_InventoryInStorePickupShippingApi`).

## Qué ve el cliente

La recogida aparece solo cuando el transportista **In-Store Pickup Delivery** está activo (`carriers/instore/active`) y el carrito puede surtirse desde al menos un punto de recogida.

- El paso de envío ofrece **Ship to my address** y **Pick up in store**.
- Al elegir la recogida aparece un buscador por código postal o ciudad, con los puntos que pueden surtir todos los productos del carrito.
- Al elegir un punto, este pasa a ser el destino del envío. La dirección del cliente queda como dirección de facturación y el pedido se coloca con el `pickup_location_code` del punto.
- Con el transportista inactivo, o cuando ningún punto puede surtir el carrito, el checkout se ve como si el paquete no estuviera instalado.

La búsqueda usa el endpoint del core `POST /V1/inventory/in-store-pickup/pickup-locations/`. Buscar por código postal o ciudad necesita un geocodificador: configura `cataloginventory/source_selection_distance_based/provider` en `offline` e importa los geonames de tu país (`bin/magento inventory-geonames:import`), o configura el proveedor de Google con una clave. Sin uno, el endpoint no devuelve ningún punto para una búsqueda por zona.

## Añade tu propio renderizador de transportista

El paquete se apoya en un punto de extensión genérico de `module-checkout`, el equivalente de envío de los renderizadores de método de pago. Un transportista que declara un renderizador deja de aparecer como un botón de opción simple: su componente dibuja la interfaz del transportista dentro del paso de envío.

Declara el renderizador en el layout, en el contenedor `checkout.shipping.carriers` de `checkout_index_index`:

```xml
<referenceContainer name="checkout.shipping.carriers">
    <block class="MageObsidian\ModernFrontend\Block\Template" name="acme.shipping.locker"
           ifconfig="carriers/acme_locker/active">
        <arguments>
            <argument name="renderer" xsi:type="object">AcmeLockerRenderer</argument>
        </arguments>
    </block>
</referenceContainer>
```

```xml
<virtualType name="AcmeLockerRenderer" type="MageObsidian\Checkout\ViewModel\ShippingRenderer">
    <arguments>
        <argument name="carriers" xsi:type="array">
            <item name="acme_locker" xsi:type="string">acme_locker</item>
        </argument>
        <argument name="component" xsi:type="string">Acme_Locker::shipping/LockerFinder</argument>
        <argument name="config" xsi:type="array">
            <item name="radius" xsi:type="number">50</item>
        </argument>
    </arguments>
</virtualType>
```

`component` es una referencia cualificada `Vendor_Module::path` a un componente Vue, de modo que un override del tema siga siendo alcanzable. Si la lógica necesita la tienda, implementa tú mismo `MageObsidian\Checkout\Api\ShippingRendererInterface`, como hace el paquete de recogida.

El componente recibe estas props:

| Prop | Significado |
|---|---|
| `code` | El código del transportista. |
| `methods` | Las tarifas del transportista para la dirección actual. |
| `selected` | `true` mientras una de esas tarifas es el método de envío elegido. |
| `config` | El arreglo que el renderizador devolvió en `getConfig()`. |
| `address` | La dirección de envío del cliente, de solo lectura. |
| `skus` | Los SKU del carrito. |

y emite:

| Evento | Efecto |
|---|---|
| `select(method)` | Elige una de las tarifas del transportista. |
| `deselect` | Devuelve la elección a los métodos simples. |
| `destination(destination)` | Fija la dirección y los `extensionAttributes` que se envían como dirección de envío, o `null` para borrarlos. |

Mientras el transportista de un renderizador está elegido y no se indicó destino, el checkout no guarda el paso de envío y los métodos de pago siguen ocultos. Un renderizador que no logra cargar se retira junto con las tarifas de su transportista.
