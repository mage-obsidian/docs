# Creación de Scripts y Componentes

En **{{ config.extra.components_name }}**, los temas pueden incluir lógica personalizada en JavaScript y componentes Vue para extender su funcionalidad. Estos archivos deben ubicarse dentro del directorio del tema:

```
app/design/frontend/Vendor/Theme
```

Específicamente:

- **JavaScript Personalizado**:  
  ```
  app/design/frontend/Vendor/Theme/web/js
  ```
- **Componentes Vue**:  
  ```
  app/design/frontend/Vendor/Theme/web/components
  ```

Este proceso sigue el mismo flujo de trabajo explicado para los módulos, garantizando consistencia y facilidad de uso.

---

## Flujo de Trabajo

### 1. **JavaScript en `web/js`**

El directorio `web/js` está destinado a archivos de JavaScript de propósito general que manejan lógica personalizada o funciones utilitarias. Los archivos colocados aquí son procesados automáticamente por **Vite** e incluidos en el frontend según sea necesario.

**Ejemplo**:

```javascript
// app/design/frontend/Vendor/Theme/web/js/theme-utils.js
export function greetUser(name) {
     console.log(`Hola, ${name}! Bienvenido a nuestro tema.`);
}
```

**Uso en `.phtml`**:
```php
<script type="module" src="<?= $block->getViteFileUrl('Theme::js/theme-utils.js') ?>"></script>
<script type="module">
     import { greetUser } from 'Theme::js/theme-utils.js';
     greetUser('Juan');
</script>
```

---

### 2. **Componentes Vue en `web/components`**

El directorio `web/components` está diseñado para componentes Vue de un solo archivo (SFC). Cada componente debe seguir la estructura de Vue, aprovechando la Composition API para una mayor modularidad y flexibilidad.

**Ejemplo**:
```vue
<!-- app/design/frontend/Vendor/Theme/web/components/Greeting.vue -->
<template>
     <div>
          <h1>Hola, {{ name }}!</h1>
     </div>
</template>

<script>
import { ref } from 'vue';

export default {
     setup() {
          const name = ref('Juan');
          return { name };
     },
};
</script>
```

**Uso en `.phtml`**:
```php
<?= $block->renderVueComponent('Theme::components/Greeting', ['name' => 'Juan Pérez']) ?>
```

---

## Guías y Recomendaciones

1. **Flujo de Trabajo Consistente**  
    El flujo de trabajo para incluir scripts en los temas es el mismo que para los módulos:
    - Usa `web/js` para lógica general en JavaScript.
    - Usa `web/components` para componentes Vue.

2. **Ubicación de Archivos**  
    Asegúrate de que tus archivos estén en las rutas correctas dentro del directorio del tema:
    - JavaScript: `app/design/frontend/Vendor/Theme/web/js`
    - Componentes: `app/design/frontend/Vendor/Theme/web/components`

3. **Convenciones de Nombres**  
    - Usa **kebab-case** o **camelCase** para los nombres de archivos en `web/js`.
    - Usa **PascalCase** para los archivos de componentes Vue en `web/components`.

4. **Imports Dinámicos**  
    Los imports dinámicos pueden usarse para los archivos de JavaScript para optimizar el rendimiento:
    ```javascript
    import('Theme::js/theme-utils.js').then(({ greetUser }) => greetUser('Importación Dinámica'));
    ```

5. **Procesamiento con Vite**  
    Tanto `web/js` como `web/components` son procesados por **Vite**:
    - Los archivos se optimizan y agrupan.
    - El tree-shaking asegura que solo el código necesario sea incluido.

---

## Ejemplo de Flujo de Trabajo

Aquí tienes un ejemplo práctico de cómo incluir un script personalizado y un componente Vue en un tema:

1. **Crear un Script Personalizado**:  
    Archivo: `app/design/frontend/Vendor/Theme/web/js/theme-logic.js`  
    ```javascript
    export function calculateTotal(items) {
         return items.reduce((sum, item) => sum + item.price, 0);
    }
    ```

2. **Crear un Componente Vue**:  
    Archivo: `app/design/frontend/Vendor/Theme/web/components/CartSummary.vue`  
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

3. **Incluir en `.phtml`**:  
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

## Beneficios

1. **Flujo de Trabajo Unificado**  
    Una metodología consistente entre módulos y temas simplifica el desarrollo y el mantenimiento.

2. **Herramientas Modernas**  
    Vite asegura una agrupación optimizada y compilaciones más rápidas, con soporte para tree-shaking y módulos ES.

3. **Flexibilidad**  
    Permite que la lógica personalizada y los componentes Vue se integren sin problemas en el frontend, mejorando la funcionalidad y la experiencia del usuario.

Siguiendo estas pautas, puedes crear un tema bien organizado y eficiente que aproveche **{{ config.extra.components_name }}** para un máximo rendimiento y escalabilidad.
