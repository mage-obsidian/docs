# Compatibility Configuration

To make a module compatible with **{{ config.extra.components_name }}**, follow these steps. The process is the same whether you are creating a new module or adding compatibility to an existing one.

If you are creating a new module, refer to the official Magento documentation for the standard setup process:  
[Creating a module in Magento](https://experienceleague.adobe.com/en/docs/commerce-learn/tutorials/backend-development/create-module)

Once the module is prepared, include the compatibility configuration as described below.

---

## Steps to Configure Compatibility

1. **Create the Compatibility File**  
      - File Name:  
         
         `mage_obsidian_compatibility.xml`

      - File Path:  
         
         > Save the file in the following location: 
          
         ```
         app/code/Vendor/ModuleName/etc/mage_obsidian_compatibility.xml
         ```

2. **Add the File Content**  
      - Copy and paste the following content into the file:
         ```xml
         <?xml version="1.0"?>
         <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
                  <features>
                     <compatibility>true</compatibility>
                  </features>
         </config>
         ```

---

## Final Steps

After configuring the compatibility file, you must run the following commands to integrate the theme into Magento and generate the necessary metadata:

1. **Load Module in Magento**  
    ```bash
    bin/magento setup:upgrade
    ```

2. **Generate metadata for {{ config.extra.components_name }}**  
    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

---

## Key Details

- The compatibility file must be saved at:  
  `Vendor/ModuleName/etc/mage_obsidian_compatibility.xml`

- The declaration `xsi:noNamespaceSchemaLocation` already points to the required schema:  
  `urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd`

- The `<features>` node includes the `<compatibility>` tag, which must be set to `true` to indicate compatibility with **{{ config.extra.components_name }}**.

---

## Optional: `universal` flag (multi-theme coexistence)

By default a compatible module's layout is collected **only** under a **{{ config.extra.components_name }}** theme. Under a legacy (non-Obsidian) theme its layout is suppressed, so enabling the module never breaks a store that still runs Luma/Blank. This is what makes a per-website migration safe: the active theme of each request decides whether the module participates.

Set `<universal>true</universal>` to opt a module into **every** theme, legacy included:

```xml
<features>
    <compatibility>true</compatibility>
    <universal>true</universal>
</features>
```

Use it only for modules whose layout is theme-agnostic. A universal module contributes its **entire** layout to legacy themes — both its Vue islands and any legacy-block neutralization (`remove="true"`) — so anything theme-specific there will reach the legacy theme too. Omitting the flag (or setting it to `false`) keeps the default, theme-gated behavior.

Re-run `mage-obsidian:frontend:config --generate` after changing the flag so the contract picks it up.

---

## Purpose

This setup ensures that only modules explicitly declared as compatible can interact with the features and architecture of **{{ config.extra.components_name }}**, resulting in a more organized and reliable development process.

---

## Future Flexibility

This structure is designed to support future enhancements. By updating this XML file, it will be possible to activate or deactivate new features introduced in **{{ config.extra.components_name }}**. This approach provides greater flexibility and control over module behavior, enabling seamless adoption of upcoming functionality.
