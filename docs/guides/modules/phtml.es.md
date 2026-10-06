# Plantillas (.phtml)

## Uso de Archivos JavaScript y Componentes Vue en Plantillas `.phtml`

Con **{{ config.extra.components_name }}**, integrar archivos JavaScript y componentes Vue en plantillas `.phtml` es más simple y poderoso gracias a la clase `MageObsidian\ModernFrontend\Block\Template`.

Esta clase mejorada proporciona métodos para cargar, resolver y renderizar recursos de manera eficiente, manteniendo la consistencia con las convenciones de importación explicadas anteriormente. [Importaciones Entre Módulos de Magento](javascript.md)

---

### ¿Por Qué Usar `MageObsidian\ModernFrontend\Block\Template`?

Esta clase extiende la clase `Template` de Magento y añade métodos avanzados, entre ellos:

- **Resolución dinámica de recursos**: Soporta la notación `Vendor_Module::` para resolver rutas de archivos.
- **Integración simplificada con Vue**: Renderiza componentes Vue de manera dinámica con propiedades.
- **Acceso optimizado a bibliotecas**: Permite incluir archivos de bibliotecas o recursos generados por Vite con facilidad.

---

### Funciones Clave

#### 1. Resolución de Rutas de Archivos

Los archivos se pueden resolver dinámicamente usando el método `resolvePathByName()`. Este método permite referenciar archivos con la notación `Vendor_Module::` o directamente desde temas utilizando `Theme::`.

**Ejemplo:**
```php
// Resolver un archivo JavaScript
$fileUrl = $block->resolvePathByName('Vendor_Module::js/main');

// Resolver un componente Vue
$componentPath = $block->resolvePathByName('Vendor_Module::components/NavBar');

// Resolver un archivo desde el tema
$themeFile = $block->resolvePathByName('Theme::custom-component');
```

---

#### 2. Renderización de Componentes Vue

El método `renderVueComponent()` monta un componente Vue como una **isla**. En lugar de un `<script>` en línea por cada llamada, emite un marcador pequeño e inerte que un único bootstrap a nivel de página descubre y monta. Por defecto la isla se hidrata de forma **perezosa** —solo cuando entra en el viewport—, así que los componentes por debajo del pliegue no cuestan nada hasta que realmente se necesitan.

**Firma**
```php
$block->renderVueComponent(
    string $componentName,
    array $props = [],
    bool $eager = false,
    string $serverHtml = '',
    bool $hydrate = false
): string;
```

| Parámetro | Descripción |
|---|---|
| `$componentName` | Componente en notación `Vendor_Module::Component` (el prefijo `components/` está implícito). |
| `$props` | Datos pasados al componente como props de Vue. Se codifican como JSON seguro para atributo; un valor no codificable lanza una excepción en vez de emitir markup roto. |
| `$eager` | `false` (por defecto) hidrata cuando el marcador se vuelve visible; `true` monta de inmediato — úsalo para componentes por encima del pliegue. |
| `$serverHtml` | Markup renderizado dentro del marcador, para que pinte junto con el documento en lugar de esperar al chunk del componente. |
| `$hydrate` | `true` significa que `$serverHtml` **es** el estado inicial del componente y Vue lo adopta en el lugar. `false` (por defecto) lo trata como un placeholder que Vue reemplaza al montar. |

**Ejemplo: Renderizar un Componente Vue en una Plantilla `.phtml`**
```php
<?= $block->renderVueComponent(
    'Vendor_Module::NavBar',
    [
        'title' => 'Bienvenido',
        'userId' => 123
    ]
) ?>
```

Esto emite un único marcador, sin script de montaje en línea:

**Salida Generada:**
```html
<div data-mage-island
     data-component="https://magento.test/static/version1733144244/frontend/Vendor/theme/en_US/generated/Vendor_Module/components/NavBar.js"
     data-props="{&quot;title&quot;:&quot;Bienvenido&quot;,&quot;userId&quot;:123}"
     data-strategy="visible"></div>
```

Para un componente por encima del pliegue que no deba esperar al viewport, activa el montaje eager:
```php
<?= $block->renderVueComponent('Vendor_Module::Hero', [], true) ?>
```

Una isla eager por encima del pliegue no debería dejar su contenedor vacío — eso es un hueco en la página hasta que llega su chunk. Renderiza su estado inicial en el servidor y deja que Vue lo hidrate:

```php
<?= $block->renderVueComponent('Vendor_Module::Hero', $props, true, $serverHtml, true) ?>
```

> **Nota:** El runtime de Vue y el plugin de i18n se cargan **una sola vez por página** y se comparten entre todas las islas; una página sin islas no carga Vue en absoluto. Consulta [Islas Vue](../vue/islands.md) para conocer la arquitectura completa, las estrategias `visible`/`eager` y cómo generar `$serverHtml`.

---

#### 3. Carga de Archivos de Biblioteca

El método `getViewLibFileUrl()` permite incluir archivos de bibliotecas de forma sencilla. Por ejemplo, puedes cargar un script específico de una biblioteca:

**Ejemplo:**
```php
<script type="module" src="<?= $block->getViewLibFileUrl('some-library') ?>"></script>
```

Esto asegura consistencia con el proceso de construcción basado en Vite.

---

#### 4. Archivos Generados por Vite

Utiliza el método `getViteFileUrl()` para cargar archivos generados por Vite, como scripts de entrada o recursos.

**Ejemplo:**
```php
<script type="module" src="<?= $block->getViteFileUrl('Vendor_Module::main') ?>"></script>
```

---

### Ejemplo Completo en una Plantilla `.phtml`

Aquí tienes un ejemplo completo que demuestra múltiples casos de uso:

```php
<?php
/** @var MageObsidian\ModernFrontend\Block\Template $block */
?>

<!-- Incluir una biblioteca de JavaScript -->
<script type="module" src="<?= $block->getViewLibFileUrl('some-library') ?>"></script>

<!-- Cargar un archivo de entrada generado por Vite -->
<script type="module" src="<?= $block->getViteFileUrl('Vendor_Module::main') ?>"></script>

<!-- Renderizar un componente Vue dinámicamente -->
<?= $block->renderVueComponent('Vendor_Module::NavBar', ['title' => 'Bienvenido a ModernFrontend', 'theme' => 'dark']) ?>

<!-- Resolver un archivo desde el tema -->
<script type="module" src="<?= $block->resolvePathByName('Theme::custom-script') ?>"></script>
```

---

### Buenas Prácticas

1. **Evita Rutas de Archivos Codificadas**  
   No codifiques rutas directamente. En su lugar, utiliza los métodos del bloque como `resolvePathByName()`, `getViteFileUrl()` o `getViewLibFileUrl()` para garantizar una resolución consistente de archivos.

2. **Pasa Propiedades a los Componentes Vue**  
   Cuando renderices componentes Vue, pasa solo los datos necesarios como `props` para mantener tus componentes flexibles y reutilizables.

3. **Mantén las Plantillas Limpias**  
   Utiliza los métodos del bloque para encapsular la lógica, enfocando tus plantillas `.phtml` en la estructura y presentación.

---

### Beneficios de Este Enfoque

1. **Resolución Dinámica**  
   Los archivos y componentes se resuelven dinámicamente, respetando sobrescrituras realizadas en los temas.

2. **Consistencia**  
   Mantiene un enfoque consistente para manejar archivos entre JavaScript, componentes Vue y plantillas.

3. **Preparado para el Futuro**  
   Al aprovechar Vite y una clase de bloque moderna, tu integración está optimizada para escalabilidad y rendimiento.

4. **Facilidad de Uso**  
   Simplifica el proceso de inclusión de scripts y componentes, reduciendo la redundancia y los errores.

---

### Próximos Pasos

- Aprende más sobre cómo sobrescribir componentes y scripts en la sección **Temas**.
- Lee [Islas Vue](../vue/islands.md) para entender la hidratación perezosa y las estrategias `visible`/`eager`.

## Escribir Lógica de Vue.js Directamente en Plantillas `.phtml`

Esta sección demuestra cómo integrar lógica de Vue.js directamente en un archivo `.phtml`. También muestra cómo los datos generados por PHP pueden trabajar sin problemas con la interactividad de Vue.js sin necesidad de crear un componente Single File Component (SFC).

> **Consejo:** Este patrón en línea es útil para una mejora puntual y pequeña sobre una página renderizada en el servidor. Para cualquier cosa que construirías como componente, prefiere [`renderVueComponent`](phtml.md#2-renderizacion-de-componentes-vue), que lo monta como una [isla Vue](../vue/islands.md) de hidratación perezosa: el runtime de Vue se comparte en toda la página en lugar de importarse de nuevo en cada bloque en línea.

---

### Ejemplo: Saludo Interactivo

A continuación, un ejemplo simple donde PHP genera contenido estático, y Vue.js añade un elemento dinámico e interactivo a la página.

#### Código

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

### Explicación del Ejemplo

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

### Beneficios de Este Enfoque

1. **Simple y Efectivo**: Combina PHP para contenido estático con Vue para características interactivas.
2. **Reactividad Localizada**: Vue solo se aplica a una sección específica de la página, minimizando la complejidad.
3. **Prototipado Rápido**: Ideal para elementos interactivos pequeños sin necesidad de crear componentes Vue separados.

---

### Resultado

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

### Casos de Uso

- Mejoras rápidas a páginas renderizadas por el servidor.
- Añadir interactividad a pequeñas secciones sin crear componentes Vue separados.
- Prototipar características dinámicas con un costo mínimo en complejidad.
