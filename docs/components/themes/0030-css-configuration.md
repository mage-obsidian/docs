# CSS Configuration

In **{{ config.extra.components_name }}**, themes play a crucial role in customizing the design and structure of the frontend. This section explains how to configure CSS for compatible themes and leverage the flexibility offered by **{{ config.extra.components_name }}** to optimize and personalize styles.

---

## CSS Entry Point for Themes

The primary CSS entry point for a theme is:

```
web/css/theme.source.css
```

This file defines the theme's specific styling rules and is located at:

```
app/design/frontend/Vendor/Theme/web/css/theme.source.css
```

> For more information on configuring Tailwind CSS, refer to its [official documentation](https://tailwindcss.com/docs).

---

## Example `theme.source.css`

A typical `theme.source.css` file using **Tailwind CSS** might look like this:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
body {
    font-family: 'Helvetica, Arial, sans-serif';
}
```

This file takes advantage of **Tailwind CSS**, enabling efficient customization through utility classes.

---

## How It Works

1. **Import Order**  
    Theme styles are loaded **after** all styles defined in compatible modules. This ensures that themes can override module styles if necessary.  

    An example of the import order is:

    ```css
    /* Module CSS */
    @import "/var/www/html/app/code/Vendor/ModuleA/view/frontend/web/css/module.extend.css"; /* Module A */
    @import "/var/www/html/app/code/Vendor/ModuleB/view/frontend/web/css/module.extend.css"; /* Module B */
    
    /* Theme CSS */
    @import "/var/www/html/app/design/frontend/Vendor/ThemeParent/web/css/theme.source.css"; /* Parent Theme */
    @import "/var/www/html/app/design/frontend/Vendor/CurrentTheme/web/css/theme.source.css"; /* Current Theme */
    ```

2. **Flexibility to Ignore Module CSS**  
    Themes can **exclude specific module styles** through custom configurations. This provides full control over which styles are included in the final build, resulting in a cleaner and more optimized design.

---

## Integration with Tailwind CSS

Using **Tailwind CSS** as part of **{{ config.extra.components_name }}** allows developers to take advantage of utility classes and tree-shaking techniques to remove unused styles. This results in a fully optimized CSS file.

1. **Base Styles**:  
    ```css
    @tailwind base;
    ```
    Provides essential base styles.

2. **Custom Components**:  
    ```css
    @tailwind components;
    ```
    Includes reusable components defined by the developer.

3. **Utilities**:  
    ```css
    @tailwind utilities;
    ```
    Generates utilities for quick and precise customization.

---

## Key Benefits

1. **Controlled Overrides**:  
    Theme styles can easily override those defined in modules.

2. **Optimized CSS**:  
    Only necessary styles are included in the final file thanks to Tailwind CSS and tree-shaking.

3. **Flexibility**:  
    Configure which styles are included or excluded using theme-specific settings.

4. **Enhanced Performance**:  
    The final CSS file is lightweight and optimized, improving frontend load times.

---

By following these guidelines, you can create fully customized and optimized themes for **{{ config.extra.components_name }}**, maximizing control and efficiency in your frontend design.
