# Module Configuration

In **{{ config.extra.components_name }}**, each compatible module can include additional configurations by creating a configuration file at:

```
view/frontend/web/module.config.cjs
```

This file follows the **CJS (CommonJS)** format for compatibility reasons and exports a configuration object that is read by **{{ config.extra.components_name }}**.

## How It Works

1. **Configuration File Loading**  
    Configuration files are loaded in the order defined by the `sequence` configuration in each module's `module.xml` file.
    
    > For more details on how to define the sequence of modules, see the official Magento documentation:  
    [Configuring Component Load Order](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

2. **Example Configuration File**  
    A basic example of a `module.config.cjs` file might look like this:

    ```javascript
    module.exports = {
         tailwind: {
              // Tailwind CSS configuration
         }
    };
    ```

    Currently, the only supported configuration option is for **Tailwind CSS**, but future updates will expand this functionality to allow additional module-specific options.

3. **Overriding Module Configurations**  
    Module configurations can be overridden directly in themes by creating a corresponding configuration file. For example:

    ```
    app/design/frontend/Vendor/Theme/Vendor_Module/web/module.config.cjs
    ```

    - When this file exists, it **completely replaces** the original configuration provided by the module.
    - The theme configuration is not treated as an extension or a merged version of the module's configuration; instead, it fully overrides the original settings.

---

## Benefits and Future Potential

- **Customizability**: Module configurations can be tailored to fit the needs of specific projects or themes without altering the module code.
- **Scalability**: The configuration system is designed to support additional options beyond Tailwind in future versions, providing greater flexibility for module developers.
- **Control**: Themes have the ability to fully override module configurations, ensuring a clean separation of concerns and avoiding unwanted side effects.

---

## Key Notes

- The file format is strictly **CJS** for compatibility across environments.
- Configurations are loaded in the sequence defined in `module.xml`. For detailed guidance, refer to the [official Magento documentation](https://developer.adobe.com/commerce/php/development/build/component-load-order/).
- Overriding configurations in themes fully replaces the module's original settings, without merging or extending them.
