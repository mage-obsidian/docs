# Tailwind Configuration

In **{{ config.extra.components_name }}**, each module can define its own Tailwind CSS configuration under the `tailwind` key in the module configuration file (`module.config.cjs`). This configuration follows the structure and syntax of Tailwind CSS version 3.

For details on how to structure a Tailwind CSS configuration, refer to the official documentation:  
[Tailwind CSS Configuration](https://tailwindcss.com/docs/configuration)

## Example Configuration

A basic example of a module configuration file with Tailwind CSS options:

```javascript
module.exports = {
    tailwind: {
        theme: {
            extend: {} // Extend default theme settings here
        },
        plugins: [], // Add Tailwind CSS plugins if needed
        content: [
            '../templates/**/*.phtml' // Define the paths to your template files
        ]
    }
};
```

## How It Works

1. **Merging Configurations**  
    Tailwind CSS configurations defined in modules are **merged** during the build process:
    - Configurations from all modules are merged first, respecting the order defined by the `sequence` in `module.xml`.
    
        > For more details on configuring module load order, refer to the official Magento documentation:  
        [Configuring Component Load Order](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

    - Theme configurations are merged afterwards, taking precedence over all module configurations.

2. **Prioritization**  
    - Module configurations are processed based on their dependency order as defined in their `module.xml`.
    - Theme configurations always have the highest priority, allowing themes to override or extend Tailwind settings from modules.

3. **Ignoring Module Configurations**  
    - A theme can explicitly choose to **ignore the Tailwind configuration of a specific module**. When this is done, the module's configuration is excluded entirely from the merging process, giving themes full control over the final build.

---

## Key Notes

- The Tailwind configuration object should follow the syntax and structure defined in [Tailwind CSS documentation](https://tailwindcss.com/docs/configuration).
- The `content` array must include the paths to the templates where Tailwind classes are used. This is essential for Tailwind's purge functionality to work correctly.
- The merging process ensures flexibility, allowing both modules and themes to contribute to the final Tailwind CSS build while maintaining a clear prioritization hierarchy.
- A theme can exclude module configurations entirely, providing full control over the Tailwind setup.
- For more information on module dependency order, see the [official Magento documentation](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

---

## Benefits

- **Modularity**: Each module can define its own Tailwind CSS configuration independently.
- **Flexibility**: Themes can take full control by overriding or ignoring module configurations.
- **Performance**: The merging process ensures an optimized Tailwind CSS build that includes only the necessary styles.
