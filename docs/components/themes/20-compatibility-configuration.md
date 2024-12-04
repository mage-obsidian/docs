# Compatibility Configuration

Unlike modules, **we do not recommend adding support for {{ config.extra.components_name }} to existing themes** that use methodologies related to Luma or Blank. This approach is radical and completely removes support for technologies like LESS, Knockout, RequireJS, among others. Therefore, we suggest using this approach only for **new themes** or themes based on **{{ config.extra.components_name }}**.

## Creating a Compatible Theme

To create a theme, first follow the standard steps described in the official Magento documentation:  
[Creating a Theme in Magento](https://developer.adobe.com/commerce/php/tutorials/frontend/create-theme/)  

In summary, you need to create a structure like this:

```
app/design/frontend/Vendor/ThemeName
```

### Basic Files

Make sure to include the minimum required files to register a theme in Magento:

1. **registration.php**  
2. **theme.xml**  

### Declaring Theme Inheritance

When configuring the `theme.xml` file, pay attention if you want to inherit from a compatible theme. Declaring a non-compatible theme as a parent will result in **inheritance being ignored during the compilation process**, and the theme will not work as expected.

---

## Configuring Theme Compatibility

To configure a theme as compatible with **{{ config.extra.components_name }}**, follow these steps:

1. **Create the Compatibility File**  
        - File Name:  
          `mage_obsidian_compatibility.xml`

        - File Path:  
          Save the file in the following location:  
          ```
          app/design/frontend/Vendor/ThemeName/etc/mage_obsidian_compatibility.xml
          ```

2. **Add the File Content**  
        - Copy and paste the following content into the file:

          ```xml
          <?xml version="1.0"?>
          <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
                <features>
                     <compatibility>true</compatibility>
                </features>
          </config>
          ```

---

## Final Steps

After configuring the compatibility file, you must run the following commands to integrate the theme into Magento and generate the necessary metadata:

1. **Load the theme in Magento**  
    ```bash
    bin/magento setup:upgrade
    ```

2. **Generate metadata for {{ config.extra.components_name }}**  
    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

---

## Final Notes

With these steps, your theme will be fully integrated with **{{ config.extra.components_name }}**. This approach ensures that the theme leverages the modern functionalities of the architecture, removing dependencies on outdated technologies and promoting a cleaner, more efficient experience.
