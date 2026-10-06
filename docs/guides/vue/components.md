# Vue Component Configuration

In **{{ config.extra.components_name }}**, Vue components are automatically tracked when placed in the following directory:  
```
view/frontend/web/components
```

> These files must follow the **Single File Component (SFC)** structure defined by Vue. For more information, refer to the official Vue documentation:  
[Vue Single File Components (SFC)](https://vuejs.org/guide/scaling-up/sfc)

> For styling details, Vue provides powerful CSS features in its SFCs. Learn more in the official documentation:  
[Vue SFC CSS Features](https://vuejs.org/api/sfc-css-features.html)

---

## Overriding Components in Themes

**{{ config.extra.components_name }}** allows Vue components to be overridden in themes. This provides flexibility for customizing or replacing components entirely to suit specific design and functionality requirements.  
More details on how to override components will be provided later in the section about themes.

---

## Adding Styles to Components

### **Scoped Styles**
Scoped styles ensure that CSS rules only apply to their respective components. By adding the `scoped` attribute to the `<style>` block, Vue uses attribute-based scoping to isolate the styles. This is the recommended approach for all components in **{{ config.extra.components_name }}**.

Example:
```vue
<template>
    <div class="example bg-blue-500 text-white p-4 rounded-lg">
        <p class="text-lg font-bold">{{ message }}</p>
        <button 
            @click="updateMessage" 
            class="mt-4 px-4 py-2 bg-white text-blue-500 rounded hover:bg-gray-100">
            Update Message
        </button>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const message = ref("Dynamic styling with Tailwind and Vue!");

        const updateMessage = () => {
            message.value = "Message updated successfully!";
        };

        return { message, updateMessage };
    }
};
</script>

<style scoped>
.example {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}
</style>
```

---

## Best Practices for Styling Vue Components

- **Use Tailwind Classes in Templates**: Apply Tailwind utilities directly in the `<template>` for better readability and maintainability.
- **Scoped Styles for Specific Rules**: Use scoped styles for CSS rules that cannot be handled with Tailwind utilities.
- **Override Components Only When Necessary**: Remember that components can be overridden in themes. Use this feature strategically to maintain consistency across modules and themes.
- **Leverage Tailwind Design Tokens**: Use Tailwind’s predefined classes for colors, spacing, typography, and more to maintain consistency.

---

## Benefits of Scoped Styles with Tailwind

1. **Isolation**: Scoped styles ensure no unintended CSS conflicts between components.
2. **Performance**: By tracking Vue components, Tailwind CSS generates an optimized final build, including only the utilities actually used.
3. **Flexibility**: The ability to override components in themes allows for customization without altering the core module files.
4. **Maintainability**: Keeping styles within the `<template>` or scoped styles makes it easier to debug and update components without affecting others.

---

## Example Directory Structure

Here is a recommended structure for organizing your Vue components:

```
view/
└── frontend/
    └── web/
        └── components/
            ├── Navbar.vue       // Component for navigation bar
            ├── Modal.vue        // Component for modals
            ├── shared/
            │   ├── Button.vue   // Shared button component
            │   └── Card.vue     // Shared card component
            └── Example.vue      // Example component with Tailwind classes
```

---

## Key Notes

- Vue components can be overridden in themes. This will be explained in detail in the section about themes.
- Scoped styles are the default recommendation for all Vue components in **{{ config.extra.components_name }}**.
- **Tailwind CSS is fully integrated**, and its utilities should be used directly in `<template>` for styling.
- The build process uses **Vite** to optimize components, ensuring high performance and fast loading.
- For more details on styling features in Vue, refer to the [Vue SFC CSS Features documentation](https://vuejs.org/api/sfc-css-features.html).

---

## Next Steps

In upcoming sections, we will cover:

1. **How to Include Vue Components in `.phtml` Templates**: Step-by-step instructions for rendering Vue components in Magento templates.
2. **How to Override Components in Themes**: A detailed guide on overriding Vue components in your theme for customization.
3. **Advanced Styling Techniques**: Strategies for extending Tailwind utilities and managing complex component styles.
