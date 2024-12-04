# CSS Configuration

In **{{ config.extra.components_name }}**, including custom CSS from modules is straightforward and efficient. The system automatically tracks the following entry point in compatible modules:  
```
/var/www/html/app/code/Vendor/ModuleName/view/frontend/web/css/module.extend.css
```

This file will be included for each module that defines it, unless explicitly excluded by the theme configuration (more details on this functionality will be covered later).

## How It Works

1. **Import Order**  
    CSS files are loaded based on the **module priority** defined in Magento. The order is determined by the `sequence` configuration in each module’s `module.xml` file. This allows you to control the import order of module CSS. Additionally, all module CSS is loaded **before theme CSS**.

    > For more details on configuring the module load order, see the official Magento documentation:  
    [Configuring Component Load Order](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

    A typical import order might look like this:

    ```css
    /* Module CSS */
    @import "/var/www/html/app/code/Vendor/ModuleA/view/frontend/web/css/module.extend.css"; /* Module A */
    @import "/var/www/html/app/code/Vendor/ModuleB/view/frontend/web/css/module.extend.css"; /* Module B */
    
    /* Theme CSS */
    @import "/var/www/html/app/design/frontend/Vendor/ThemeParent/web/css/theme.source.css"; /* Parent theme */
    @import "/var/www/html/app/design/frontend/Vendor/CurrentTheme/web/css/theme.source.css"; /* Current theme */
    ```

    - **Modules**: If a module wants to include custom CSS, it should use the file located at `view/frontend/web/css/module.extend.css` as its entry point. **{{ config.extra.components_name }}** automatically tracks these files for compatible modules.
    - **Themes**: The CSS entry point for themes is always `theme.source.css`.

2. **Flexibility with Theme Configuration**  
    As mentioned earlier, the theme configuration allows you to **exclude CSS entries from specific modules**. This provides flexibility in determining which styles are included in the final build.

## Optimized CSS Output

**{{ config.extra.components_name }}** leverages **Tailwind CSS** and tree-shaking techniques to generate a single, optimized CSS file. This final file includes only the styles required for the frontend, ensuring minimal size and maximum performance.

## Key Benefits

- **Modularity**: CSS from modules is automatically integrated without additional effort.
- **Control**: Adjust the import order using the `sequence` configuration in `module.xml`, or selectively include/exclude module CSS via theme settings.
- **Performance**: The final optimized CSS file improves load times and reduces unnecessary styles.
