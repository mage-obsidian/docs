# Writing Vue.js Logic Directly in `.phtml` Templates

This section demonstrates how to integrate Vue.js logic directly within a `.phtml` file. It also showcases how PHP-rendered data can work seamlessly with Vue.js interactivity without creating a separate Single File Component (SFC).

---

## Example: Interactive Greeting

Below is a simple example where PHP generates static content, and Vue.js adds a dynamic, interactive element to the page.

### Code

```php
<?php
/** @var MageObsidian\ModernFrontend\Block\Template $block */

// PHP-rendered name
$userName = 'John Doe';
?>

<div class="greeting-container">
    <!-- Static content rendered by PHP -->
    <h1>Welcome, <?= $userName ?>!</h1>
    <p>Update your greeting dynamically:</p>

    <!-- Vue-powered dynamic section -->
    <div id="vue-greeting-app">
        <input type="text" v-model="greeting" placeholder="Enter your greeting" />
        <p>Your dynamic greeting: <strong>{{ greeting }}</strong></p>
    </div>
</div>

<script type="module">
    import { createApp, ref } from '<?= $block->getViewLibFileUrl('vue') ?>';

    // Initialize Vue app
    createApp({
        setup() {
            // Reactive greeting state
            const greeting = ref('Hello, <?= $userName ?>!');

            return {
                greeting
            };
        }
    }).mount('#vue-greeting-app');
</script>
```

---

## Explanation of the Example

1. **PHP-Rendered Static Content**  
   The initial greeting and page structure are rendered server-side by PHP:
   ```php
   <h1>Welcome, <?= $userName ?>!</h1>
   ```

2. **Dynamic Interaction Managed by Vue.js**  
   Vue.js handles the interactivity within the `#vue-greeting-app` container:
   - An input field allows the user to type a custom greeting.
   - The greeting is displayed dynamically in real-time using Vue’s `v-model`.

3. **Minimal Logic**  
   The Vue logic is simple and localized to a small section, ensuring clarity and maintainability:
   ```javascript
   const greeting = ref('Hello, <?= $userName ?>!');
   ```

---

## Benefits of This Approach

1. **Simple and Effective**: Combines PHP for static content with Vue for interactive features.
2. **Localized Reactivity**: Vue is only applied to a specific section of the page, minimizing complexity.
3. **Quick Prototyping**: Ideal for small, interactive elements without requiring separate Vue components.

---

## Result

1. **Initial Render**:
   ```
   Welcome, John Doe!
   Update your greeting dynamically:
   ```

2. **Dynamic Behavior**:
   - The user types in the input field, and the greeting updates instantly:
     ```
     Your dynamic greeting: Hello, [User Input]!
     ```

---

## Use Cases

- Quick enhancements to server-rendered pages.
- Adding interactivity to small sections without creating separate Vue components.
- Prototyping dynamic features with minimal overhead.
