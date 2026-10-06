# Configuración de Componentes Vue

En **{{ config.extra.components_name }}**, los componentes Vue se rastrean automáticamente cuando se colocan en el siguiente directorio:  
```
view/frontend/web/components
```

> Estos archivos deben seguir la estructura **Single File Component (SFC)** definida por Vue. Para más información, consulta la documentación oficial de Vue:  
[Vue Single File Components (SFC)](https://vuejs.org/guide/scaling-up/sfc)

> Para más detalles sobre estilos, Vue proporciona potentes características CSS en sus SFC. Aprende más en la documentación oficial:  
[Características CSS en SFC de Vue](https://vuejs.org/api/sfc-css-features.html)

---

## Sobrescritura de Componentes en Temas

**{{ config.extra.components_name }}** permite sobrescribir componentes Vue en los temas. Esto brinda flexibilidad para personalizar o reemplazar componentes completamente según los requisitos específicos de diseño o funcionalidad.  
Más detalles sobre cómo sobrescribir componentes se proporcionarán más adelante en la sección sobre temas.

---

## Añadiendo Estilos a los Componentes

### **Estilos Scoped**
Los estilos scoped garantizan que las reglas CSS solo se apliquen al componente correspondiente. Al agregar el atributo `scoped` en el bloque `<style>`, Vue utiliza un mecanismo de aislamiento basado en atributos para evitar conflictos de estilos. Este enfoque es el recomendado para todos los componentes en **{{ config.extra.components_name }}**.

Ejemplo:
```vue
<template>
    <div class="example bg-blue-500 text-white p-4 rounded-lg">
        <p class="text-lg font-bold">{{ message }}</p>
        <button 
            @click="updateMessage" 
            class="mt-4 px-4 py-2 bg-white text-blue-500 rounded hover:bg-gray-100">
            Actualizar Mensaje
        </button>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const message = ref("Estilización dinámica con Tailwind y Vue!");

        const updateMessage = () => {
            message.value = "¡Mensaje actualizado con éxito!";
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

## Buenas Prácticas para Estilizar Componentes Vue

- **Usa Clases de Tailwind en el Template**: Aplica las utilidades de Tailwind directamente en el `<template>` para garantizar una mejor legibilidad y mantenimiento.
- **Estilos Scoped para Reglas Específicas**: Usa estilos scoped solo para reglas CSS que no puedan manejarse con utilidades de Tailwind.
- **Sobrescribe Componentes Solo Cuando Sea Necesario**: Recuerda que los componentes pueden sobrescribirse en los temas. Utiliza esta funcionalidad estratégicamente para mantener la consistencia entre módulos y temas.
- **Aprovecha las Utilidades de Tailwind**: Usa las clases predefinidas de Tailwind para colores, espaciados, tipografía y más, para mantener un diseño consistente.

---

## Beneficios de los Estilos Scoped con Tailwind

1. **Aislamiento**: Los estilos scoped garantizan que no haya conflictos CSS entre componentes.
2. **Rendimiento**: Al rastrear los componentes Vue, Tailwind CSS genera una compilación optimizada que incluye solo las utilidades utilizadas.
3. **Flexibilidad**: La capacidad de sobrescribir componentes en temas permite personalización sin alterar los archivos del módulo original.
4. **Mantenibilidad**: Mantener los estilos dentro del `<template>` o como scoped styles facilita la depuración y actualización de los componentes sin afectar a otros.

---

## Ejemplo de Estructura de Directorios

Aquí tienes una estructura recomendada para organizar tus componentes Vue:

```
view/
└── frontend/
    └── web/
        └── components/
            ├── Navbar.vue       // Componente para barra de navegación
            ├── Modal.vue        // Componente para modales
            ├── shared/
            │   ├── Button.vue   // Componente compartido de botón
            │   └── Card.vue     // Componente compartido de tarjeta
            └── Example.vue      // Componente de ejemplo con clases de Tailwind
```

---

## Notas Clave

- Los componentes Vue pueden sobrescribirse en los temas. Esto se explicará con detalle en la sección sobre temas.
- Los estilos scoped son la recomendación predeterminada para todos los componentes Vue en **{{ config.extra.components_name }}**.
- **Tailwind CSS está totalmente integrado**, y sus utilidades deben usarse directamente en el `<template>` para estilización.
- El proceso de construcción utiliza **Vite** para optimizar los componentes, garantizando alto rendimiento y tiempos de carga rápidos.
- Para más detalles sobre características de estilos en Vue, consulta la [documentación sobre SFC CSS Features de Vue](https://vuejs.org/api/sfc-css-features.html).

---

## Próximos Pasos

En las próximas secciones cubriremos:

1. **Cómo Incluir Componentes Vue en Plantillas `.phtml`**: Instrucciones paso a paso para renderizar componentes Vue en las plantillas de Magento.
2. **Cómo Sobrescribir Componentes en los Temas**: Una guía detallada sobre cómo personalizar componentes Vue desde un tema.
3. **Técnicas Avanzadas de Estilización**: Estrategias para extender las utilidades de Tailwind y gestionar estilos complejos en componentes.
