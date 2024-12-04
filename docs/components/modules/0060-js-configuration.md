# JavaScript Configuration

In **{{ config.extra.components_name }}**, all JavaScript files should be placed in the following directories:  
```
view/frontend/web/js
```
or  
```
view/frontend/web/components
```

### **Important Recommendation**

While it is possible to use the `components` directory for specific scripts, **we strongly recommend using the `js` directory for custom scripts**. This ensures better organization and separation of concerns, maintaining a clear and modular development structure.

> The `components` directory should be reserved only for logic that is tightly coupled to specific frontend components.

---

## Modifying Scripts in Themes

JavaScript files can be overridden in themes to provide custom functionality or adaptations specific to a project. This feature allows for flexibility while maintaining the original structure of the module.

> More details about overriding scripts will be provided in the section about themes.

---

## Best Practices

- **Structure and Organization**: Use the `js` directory as the primary location for all your custom scripts and logic. This promotes maintainability and ensures a clear project structure.
- **Integrating Node.js Packages**: You can integrate Node.js packages into your scripts to enhance functionality, or write plain JavaScript if no external dependencies are needed.
- **Default JavaScript Format**: All scripts should use **ESM (ECMAScript Modules)** by default. This ensures compatibility with modern browsers and promotes a modular architecture.

---

## How It Works

1. **Build Process with Vite**  
    All JavaScript files are processed and compiled by **Vite**, resulting in an optimized output. This ensures:
    - Improved performance through modern bundling techniques.
    - Tree-shaking to include only the code necessary for the final bundle.
    - Faster builds and hot module replacement (HMR) during development.

2. **Optimized Downloads**  
    **{{ config.extra.components_name }}** takes a performance-first approach:
    - Only JavaScript files explicitly used in the frontend are downloaded.
    - Unused code is excluded from the final bundle, reducing load times and improving efficiency.

3. **Integration with Views**  
    JavaScript files can be included in your views or `.phtml` templates as needed. Specific examples on how to integrate scripts will be provided later in this documentation.

---

## Example Directory Structure

Here is a suggested structure for your JavaScript files:

```
view/
└── frontend/
    └── web/
        ├── js/
        │   ├── main.js         // Entry point for custom logic
        │   ├── utils.js        // Reusable utility functions
        │   └── services/
        │       └── api.js      // API integration logic
        └── components/
            ├── navbar.vue      // Vue component for navbar
            └── modal.vue       // Vue component for modal
```

This structure ensures that the `js` directory is the primary location for custom scripts, while the `components` directory can be used for component-specific logic if absolutely necessary.

---

## Benefits

- **Modularity**: Keeping scripts in dedicated directories ensures clean and maintainable code.
- **Flexibility**: Scripts can be overridden in themes to adapt to specific requirements.
- **Performance**: By leveraging Vite’s build process, only the necessary JavaScript is included in the final bundle, reducing page load times.
- **Scalability**: The ability to integrate Node.js packages and write modular JavaScript ensures your codebase can grow with your project’s needs.

---

## Key Notes

- **Use the `js` directory as the primary location for custom scripts.**
- All JavaScript files must use **ESM (ECMAScript Modules)** as the default format.
- Files located in `view/frontend/web/js` and `view/frontend/web/components` are automatically tracked and processed.
- JavaScript files can be overridden in themes. Details about this will be covered in the section about themes.
- The system ensures that only scripts explicitly included in your frontend are downloaded, adhering to a performance-first approach.
- Examples of how to include JavaScript files in `.phtml` templates will be provided in later sections.
