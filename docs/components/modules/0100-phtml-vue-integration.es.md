# Escribir Lógica de Vue.js Directamente en Plantillas `.phtml`

Esta sección demuestra cómo integrar lógica de Vue.js directamente en un archivo `.phtml`. También muestra cómo los datos generados por PHP pueden trabajar sin problemas con la interactividad de Vue.js sin necesidad de crear un componente Single File Component (SFC).

---

## Ejemplo: Saludo Interactivo

A continuación, un ejemplo simple donde PHP genera contenido estático, y Vue.js añade un elemento dinámico e interactivo a la página.

### Código

```php
<?php
/** @var MageObsidian\ModernFrontend\Block\Template $block */

// Nombre generado por PHP
$userName = 'Juan Pérez';
?>

<div class="greeting-container">
    <!-- Contenido estático generado por PHP -->
    <h1>¡Bienvenido, <?= $userName ?>!</h1>
    <p>Actualiza tu saludo dinámicamente:</p>

    <!-- Sección dinámica manejada por Vue -->
    <div id="vue-greeting-app">
        <input type="text" v-model="greeting" placeholder="Escribe tu saludo" />
        <p>Tu saludo dinámico: <strong>{{ greeting }}</strong></p>
    </div>
</div>

<script type="module">
    import { createApp, ref } from '<?= $block->getViewLibFileUrl('vue') ?>';

    // Inicializar la aplicación Vue
    createApp({
        setup() {
            // Estado reactivo para el saludo
            const greeting = ref('¡Hola, <?= $userName ?>!');

            return {
                greeting
            };
        }
    }).mount('#vue-greeting-app');
</script>
```

---

## Explicación del Ejemplo

1. **Contenido Estático Generado por PHP**  
   El saludo inicial y la estructura de la página son generados por PHP en el servidor:
   ```php
   <h1>¡Bienvenido, <?= $userName ?>!</h1>
   ```

2. **Interacción Dinámica Manejada por Vue.js**  
   Vue.js gestiona la interactividad dentro del contenedor `#vue-greeting-app`:
   - Un campo de entrada permite al usuario escribir un saludo personalizado.
   - El saludo se muestra dinámicamente en tiempo real utilizando `v-model` de Vue.

3. **Lógica Mínima**  
   La lógica de Vue es simple y está localizada en una pequeña sección, garantizando claridad y facilidad de mantenimiento:
   ```javascript
   const greeting = ref('¡Hola, <?= $userName ?>!');
   ```

---

## Beneficios de Este Enfoque

1. **Simple y Efectivo**: Combina PHP para contenido estático con Vue para características interactivas.
2. **Reactividad Localizada**: Vue solo se aplica a una sección específica de la página, minimizando la complejidad.
3. **Prototipado Rápido**: Ideal para elementos interactivos pequeños sin necesidad de crear componentes Vue separados.

---

## Resultado

1. **Renderizado Inicial**:
   ```
   ¡Bienvenido, Juan Pérez!
   Actualiza tu saludo dinámicamente:
   ```

2. **Comportamiento Dinámico**:
   - El usuario escribe en el campo de texto y el saludo se actualiza instantáneamente:
     ```
     Tu saludo dinámico: ¡Hola, [Entrada del Usuario]!
     ```

---

## Casos de Uso

- Mejoras rápidas a páginas renderizadas por el servidor.
- Añadir interactividad a pequeñas secciones sin crear componentes Vue separados.
- Prototipar características dinámicas con un costo mínimo en complejidad.
