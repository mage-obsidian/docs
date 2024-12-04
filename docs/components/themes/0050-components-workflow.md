# Creating Scripts and Components

In **{{ config.extra.components_name }}**, themes can include custom JavaScript logic and Vue components to extend their functionality. These files should be placed under the theme directory:

```
app/design/frontend/Vendor/Theme
```

Specifically:

- **Custom JavaScript**:  
  ```
  app/design/frontend/Vendor/Theme/web/js
  ```
- **Vue Components**:  
  ```
  app/design/frontend/Vendor/Theme/web/components
  ```

This process follows the same workflow explained for modules, ensuring consistency and ease of use.

---

## Workflow

### 1. **JavaScript in `web/js`**

The `web/js` directory is intended for general-purpose JavaScript files that handle custom logic or utility functions. Files placed here are automatically processed by **Vite** and included in the frontend as needed.

**Example**:

    ```javascript
    // app/design/frontend/Vendor/Theme/web/js/theme-utils.js
    export function greetUser(name) {
         console.log(`Hello, ${name}! Welcome to our theme.`);
    }
    ```

**Usage in `.phtml`**:
    ```php
    <script type="module" src="<?= $block->getViteFileUrl('Theme::js/theme-utils.js') ?>"></script>
    <script type="module">
         import { greetUser } from 'Theme::js/theme-utils.js';
         greetUser('John');
    </script>
    ```

---

### 2. **Vue Components in `web/components`**

The `web/components` directory is designed for Vue Single File Components (SFC). Each component should follow Vue’s structure, leveraging the Composition API for better modularity and flexibility.

**Example**:
    ```vue
    <!-- app/design/frontend/Vendor/Theme/web/components/Greeting.vue -->
    <template>
         <div>
              <h1>Hello, {{ name }}!</h1>
         </div>
    </template>

    <script>
    import { ref } from 'vue';

    export default {
         setup() {
              const name = ref('John');
              return { name };
         },
    };
    </script>
    ```

**Usage in `.phtml`**:
    ```php
    <?= $block->renderVueComponent('Theme::components/Greeting', ['name' => 'John Doe']) ?>
    ```

---

## Guidelines and Recommendations

1. **Consistent Workflow**  
    The workflow for including scripts in themes is the same as for modules:
    - Use `web/js` for general-purpose JavaScript.
    - Use `web/components` for Vue components.

2. **File Location**  
    Ensure that your files are placed under the correct paths in the theme directory:
    - JavaScript: `app/design/frontend/Vendor/Theme/web/js`
    - Components: `app/design/frontend/Vendor/Theme/web/components`

3. **File Naming Conventions**  
    - Use **kebab-case** or **camelCase** for file names in `web/js`.
    - Use **PascalCase** for Vue component files in `web/components`.

4. **Dynamic Imports**  
    Dynamic imports can be used for JavaScript files to optimize performance:
    ```javascript
    import('Theme::js/theme-utils.js').then(({ greetUser }) => greetUser('Dynamic Import'));
    ```

5. **Vite Processing**  
    Both `web/js` and `web/components` are processed by **Vite**:
    - Files are optimized and bundled.
    - Tree-shaking ensures only necessary code is included.

---

## Example Workflow

Here’s a practical example of including both a custom script and a Vue component in a theme:

1. **Create a Custom Script**:  
    File: `app/design/frontend/Vendor/Theme/web/js/theme-logic.js`  
    ```javascript
    export function calculateTotal(items) {
         return items.reduce((sum, item) => sum + item.price, 0);
    }
    ```

2. **Create a Vue Component**:  
    File: `app/design/frontend/Vendor/Theme/web/components/CartSummary.vue`  
    ```vue
    <template>
         <div>
              <h2>Total: {{ total }}</h2>
         </div>
    </template>

    <script>
    import { ref } from 'vue';

    export default {
         props: {
              items: {
                    type: Array,
                    required: true,
              },
         },
         setup(props) {
              const total = ref(
                    props.items.reduce((sum, item) => sum + item.price, 0)
              );
              return { total };
         },
    };
    </script>
    ```

3. **Include in `.phtml`**:  
    ```php
    <?php
    $items = [
         ['price' => 10],
         ['price' => 20],
    ];
    ?>
    <script type="module" src="<?= $block->getViteFileUrl('Theme::js/theme-logic.js') ?>"></script>
    <?= $block->renderVueComponent('Theme::components/CartSummary', ['items' => $items]) ?>
    ```

---

## Benefits

1. **Unified Workflow**  
    Consistent methodology across modules and themes simplifies development and maintenance.

2. **Modern Tooling**  
    Vite ensures optimized bundling and faster builds, with support for tree-shaking and ES modules.

3. **Flexibility**  
    Allows custom logic and Vue components to seamlessly integrate into the frontend, enhancing functionality and user experience.

By following these guidelines, you can create a well-organized and efficient theme that leverages **{{ config.extra.components_name }}** for maximum performance and scalability.
