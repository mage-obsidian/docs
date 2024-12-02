# Modules

## How to Create a Module Compatible with {{ config.extra.components_name }}

To make a module compatible with **{{ config.extra.components_name }}**, you need to create a new XML file in the following path:

```
app/code/Vendor/ModuleName/etc
```

This file must extend the schema defined at:

```
urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd
```

Below is an example of the content that should be included in the file:

> mage_obsidian_compatibility.xml

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
    <features>
        <compatibility>true</compatibility>
    </features>
</config>
```

## Key Details

1. **File Path**:
   - The file must be located in `Vendor/ModuleName/etc/mage_obsidian_compatibility.xml`.

2. **Schema Extension**:
   - The declaration `xsi:noNamespaceSchemaLocation` must point to `urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd`.

3. **XML Structure**:
   - The `<features>` node contains the `<compatibility>` tag, which must be set to `true` to declare the module as compatible with **{{ config.extra.components_name }}**.

## Purpose

This approach ensures that only modules explicitly declared as compatible can interact with the features and architecture of **{{ config.extra.components_name }}**, promoting a cleaner and more controlled development process.
