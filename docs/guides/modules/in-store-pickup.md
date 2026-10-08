---
description: "Offer in-store pickup in the MageObsidian checkout with the optional module-inventory-in-store-pickup package, and add your own carrier renderer."
---
# In-store pickup

`mage-obsidian/module-inventory-in-store-pickup` adds Magento's in-store pickup (Multi-Source Inventory) to the checkout: a choice between shipping to an address and picking up in a store, and a finder for the pickup location. It is optional and `theme-base` does not require it, so a store without MSI never installs it.

## Install

```bash
composer require mage-obsidian/module-inventory-in-store-pickup
bin/magento setup:upgrade
bin/magento mage-obsidian:frontend:config --generate
```

Then rebuild the theme. The package needs the MSI pickup modules (`Magento_InventoryInStorePickupApi` and `Magento_InventoryInStorePickupShippingApi`).

## What the shopper sees

Pickup appears only when the **In-Store Pickup Delivery** carrier is active (`carriers/instore/active`) and the cart can be served from at least one pickup location.

- The shipping step offers **Ship to my address** and **Pick up in store**.
- Choosing pickup shows a search box for a postal code or a city, and lists the pickup locations that can serve every product in the cart.
- Choosing a location sets it as the shipping destination. The shopper's own address stays as the billing address, and the order is placed with the location's `pickup_location_code`.
- With the carrier inactive, or when no location can serve the cart, the checkout looks as if the package was not installed.

The search uses the core endpoint `POST /V1/inventory/in-store-pickup/pickup-locations/`. Searching by postal code or city needs a geocoder: set `cataloginventory/source_selection_distance_based/provider` to `offline` and import the geonames of your country (`bin/magento inventory-geonames:import`), or configure the Google provider with a key. Without one the endpoint answers with no location for an area search.

## Add your own carrier renderer

The package is built on a generic extension point of `module-checkout`, the shipping counterpart of the payment method renderers. A carrier that declares a renderer is no longer listed as a plain radio button: its component draws the carrier's interface inside the shipping step.

Declare the renderer in the layout, under the `checkout.shipping.carriers` container of `checkout_index_index`:

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

`component` is a qualified `Vendor_Module::path` reference to a Vue component, so a theme override stays reachable. For logic that needs the store, implement `MageObsidian\Checkout\Api\ShippingRendererInterface` yourself, as the pickup package does.

The component receives these props:

| Prop | Meaning |
|---|---|
| `code` | The carrier code. |
| `methods` | The carrier's rates for the current address. |
| `selected` | `true` while one of those rates is the chosen shipping method. |
| `config` | The array the renderer returned from `getConfig()`. |
| `address` | The shopper's shipping address, read-only. |
| `skus` | The SKUs in the cart. |

and emits:

| Event | Effect |
|---|---|
| `select(method)` | Chooses one of the carrier's rates. |
| `deselect` | Hands the choice back to the plain methods. |
| `destination(destination)` | Sets the address and `extensionAttributes` sent as the shipping address, or `null` to clear them. |

While a renderer's carrier is selected and no destination was given, the checkout does not save the shipping step and the payment methods stay hidden. A renderer that fails to load is withdrawn together with the carrier's rates.
