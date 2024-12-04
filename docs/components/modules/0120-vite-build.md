# Generating Static Files for Production

When deploying a Magento site to production, it’s essential to generate optimized static files. **MageObsidian** uses Vite to process and bundle frontend assets, ensuring they are optimized for performance. This section explains how to generate these files for production environments.

---

## Steps to Generate Static Files

### **1. Generate Static Files for All Compatible Themes**

To process and generate all static files for all compatible themes, run the following command:

```bash
pnpm --prefix vite run build
```

This will:

- Process all frontend assets (CSS, JavaScript, Vue components, etc.) using Vite.
- Generate fully optimized static files ready for production.

---

### **2. Generate Static Files for a Specific Theme**

If you want to generate static files for a specific theme only, use this command:

```bash
pnpm --prefix vite run build:theme Vendor/Theme
```

Replace `Vendor/Theme` with the namespace and name of your desired theme. This is useful for deployments involving multiple themes or incremental updates.

---

## Important Notes

1. **Order of Execution**:  
    Always run the Vite build command before deploying Magento’s static content:
    ```bash
    bin/magento setup:static-content:deploy
    ```

2. **Why This Order?**  

    - The `vite build` command ensures all theme-related assets are processed and ready.
    - Magento's `setup:static-content:deploy` will include the Vite-generated assets in the final deployment package.

3. **Optimized Files**:  
    Vite automatically handles:
    - Minification of JavaScript and CSS files.
    - Tree-shaking to include only the necessary code.
    - Asset hashing for cache busting.

4. **Compatible Themes**:  
    Ensure that your themes are compatible with **MageObsidian** before running these commands. Themes without the required configuration will not generate files.

---

## Example Workflow

1. **Generate Assets for All Themes**:
    ```bash
    pnpm --prefix vite run build
    ```

2. **Deploy Static Content**:
    ```bash
    bin/magento setup:static-content:deploy
    ```

## Benefits of Using Vite for Static Files

1. **Optimized Performance**:  
    Vite ensures your assets are minified and optimized for fast loading.

2. **Modern Build Tools**:  
    Leverage Vite’s cutting-edge bundling capabilities, including ES module support.

3. **Seamless Integration**:  
    The generated files are automatically compatible with Magento’s static content deployment process.

---

By following these steps, you can ensure your frontend assets are fully optimized and ready for production, providing a seamless experience for your users.
