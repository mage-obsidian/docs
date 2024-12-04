# Uso de Archivos JavaScript y Componentes Vue en Plantillas `.phtml`

Con **{{ config.extra.components_name }}**, integrar archivos JavaScript y componentes Vue en plantillas `.phtml` es más simple y poderoso gracias a la clase `MageObsidian\ModernFrontend\Block\Template`.

Esta clase mejorada proporciona métodos para cargar, resolver y renderizar recursos de manera eficiente, manteniendo la consistencia con las convenciones de importación explicadas anteriormente. [Importaciones Entre Módulos de Magento](../80-imports-configuration/)

---

## ¿Por Qué Usar `MageObsidian\ModernFrontend\Block\Template`?

Esta clase extiende la clase `Template` de Magento y añade métodos avanzados, entre ellos:

- **Resolución dinámica de recursos**: Soporta la notación `Vendor_Module::` para resolver rutas de archivos.
- **Integración simplificada con Vue**: Renderiza componentes Vue de manera dinámica con propiedades.
- **Acceso optimizado a bibliotecas**: Permite incluir archivos de bibliotecas o recursos generados por Vite con facilidad.

---

## Funciones Clave

### 1. Resolución de Rutas de Archivos

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

### 2. Renderización de Componentes Vue

El método `renderVueComponent()` genera el HTML y JavaScript necesarios para cargar y montar un componente Vue dinámicamente.

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

Esto genera:

- Un `<div>` con un ID único para alojar el componente Vue.
- Un bloque `<script>` para cargar la biblioteca Vue, importar el componente y montarlo dinámicamente.

**Salida Generada:**
```html
<div id="vue-component-4b3403665fea6"></div>
<script type="module">
    import { createApp } from 'https://magento.test/static/version1733144244/frontend/Vendor/theme/en_US/generated/lib/vue.js';
    import Component from 'https://magento.test/static/version1733144244/frontend/Vendor/theme/en_US/generated/Vendor_Module/components/NavBar.js';

    try {
        createApp(Component, {"title":"Bienvenido","userId":123}).mount('#vue-component-4b3403665fea6');
    } catch (error) {
        console.error('Failed to mount Vue component:', error);
    }
</script>
```

---

### 3. Carga de Archivos de Biblioteca

El método `getViewLibFileUrl()` permite incluir archivos de bibliotecas de forma sencilla. Por ejemplo, puedes cargar un script específico de una biblioteca:

**Ejemplo:**
```php
<script type="module" src="<?= $block->getViewLibFileUrl('some-library') ?>"></script>
```

Esto asegura consistencia con el proceso de construcción basado en Vite.

---

### 4. Archivos Generados por Vite

Utiliza el método `getViteFileUrl()` para cargar archivos generados por Vite, como scripts de entrada o recursos.

**Ejemplo:**
```php
<script type="module" src="<?= $block->getViteFileUrl('Vendor_Module::main') ?>"></script>
```

---

## Ejemplo Completo en una Plantilla `.phtml`

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

## Buenas Prácticas

1. **Evita Rutas de Archivos Codificadas**  
   No codifiques rutas directamente. En su lugar, utiliza los métodos del bloque como `resolvePathByName()`, `getViteFileUrl()` o `getViewLibFileUrl()` para garantizar una resolución consistente de archivos.

2. **Pasa Propiedades a los Componentes Vue**  
   Cuando renderices componentes Vue, pasa solo los datos necesarios como `props` para mantener tus componentes flexibles y reutilizables.

3. **Mantén las Plantillas Limpias**  
   Utiliza los métodos del bloque para encapsular la lógica, enfocando tus plantillas `.phtml` en la estructura y presentación.

---

## Beneficios de Este Enfoque

1. **Resolución Dinámica**  
   Los archivos y componentes se resuelven dinámicamente, respetando sobrescrituras realizadas en los temas.

2. **Consistencia**  
   Mantiene un enfoque consistente para manejar archivos entre JavaScript, componentes Vue y plantillas.

3. **Preparado para el Futuro**  
   Al aprovechar Vite y una clase de bloque moderna, tu integración está optimizada para escalabilidad y rendimiento.

4. **Facilidad de Uso**  
   Simplifica el proceso de inclusión de scripts y componentes, reduciendo la redundancia y los errores.

---

## Próximos Pasos

- Aprende más sobre cómo sobrescribir componentes y scripts en la sección **Temas**.
- Explora cómo integrar funciones avanzadas como carga diferida e importaciones condicionales.
