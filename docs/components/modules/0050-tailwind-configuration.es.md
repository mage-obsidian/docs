# Configuración de Tailwind

En **{{ config.extra.components_name }}**, cada módulo puede definir su propia configuración de Tailwind CSS bajo la clave `tailwind` en el archivo de configuración del módulo (`module.config.cjs`). Esta configuración sigue la estructura y sintaxis de Tailwind CSS versión 3.

> Para más detalles sobre cómo estructurar una configuración de Tailwind CSS, consulta la documentación oficial:  
[Configuración de Tailwind CSS](https://tailwindcss.com/docs/configuration)

## Ejemplo de Configuración

Un ejemplo básico de un archivo de configuración de módulo con opciones para Tailwind CSS:

```javascript
module.exports = {
    tailwind: {
        theme: {
            extend: {} // Extiende las configuraciones predeterminadas aquí
        },
        plugins: [], // Agrega plugins de Tailwind CSS si es necesario
        content: [
            '../templates/**/*.phtml' // Define las rutas a tus archivos de plantillas
        ]
    }
};
```

## ¿Cómo Funciona?

1. **Unión de Configuraciones (Merging)**  
    Las configuraciones de Tailwind CSS definidas en los módulos se **unen** durante el proceso de compilación:
    - Primero, se unen las configuraciones de todos los módulos respetando el orden definido por el `sequence` en el archivo `module.xml`.
    
        > Para más detalles sobre cómo configurar el orden de carga de los módulos, consulta la documentación oficial de Magento:  
        [Configurar el Orden de Carga de Componentes](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

    - Después, se une la configuración de los temas, que tiene mayor prioridad sobre las configuraciones de los módulos.

2. **Priorización**  
    - Las configuraciones de los módulos se procesan según el orden de dependencias definido en su archivo `module.xml`.
    - Las configuraciones de los temas siempre tienen la **mayor prioridad**, permitiendo que los temas sobrescriban o extiendan las configuraciones de Tailwind de los módulos.

3. **Ignorar Configuraciones de Módulos**  
    - Un tema puede elegir explícitamente **ignorar la configuración de Tailwind de un módulo específico**. Cuando esto ocurre, la configuración del módulo es completamente excluida del proceso de unión, dando al tema un control total sobre la compilación final.

---

## Notas Clave

- El objeto de configuración de Tailwind debe seguir la sintaxis y estructura definidas en la [documentación de Tailwind CSS](https://tailwindcss.com/docs/configuration).
- El array `content` debe incluir las rutas a las plantillas donde se utilizan clases de Tailwind. Esto es esencial para que la funcionalidad de purge de Tailwind funcione correctamente.
- El proceso de unión garantiza flexibilidad, permitiendo que tanto módulos como temas contribuyan al archivo final de Tailwind CSS mientras se mantiene una jerarquía de prioridades clara.
- Un tema puede excluir completamente las configuraciones de los módulos, ofreciendo control total sobre la configuración de Tailwind.
- Para más información sobre el orden de dependencia de los módulos, consulta la [documentación oficial de Magento](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

---

## Beneficios

- **Modularidad**: Cada módulo puede definir su propia configuración de Tailwind CSS de forma independiente.
- **Flexibilidad**: Los temas pueden tomar el control completo sobrescribiendo o ignorando las configuraciones de los módulos.
- **Rendimiento**: El proceso de unión garantiza un archivo de Tailwind CSS optimizado que incluye solo los estilos necesarios.
