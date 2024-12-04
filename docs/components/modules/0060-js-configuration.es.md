# Configuración de JavaScript

En **{{ config.extra.components_name }}**, todos los archivos JavaScript deben colocarse en los siguientes directorios:  
```
view/frontend/web/js
```
o  
```
view/frontend/web/components
```

### **Recomendación Importante**

Aunque es posible utilizar el directorio `components` para scripts específicos, **recomendamos encarecidamente usar el directorio `js` para scripts personalizados**. Esto asegura una mejor organización y separación de conceptos, manteniendo una estructura de desarrollo clara y modular.

> El directorio `components` debe reservarse únicamente para lógica estrechamente vinculada a componentes específicos del frontend.

---

## Modificación de Scripts en los Temas

Los archivos JavaScript pueden ser sobrescritos en los temas para proporcionar funcionalidades o adaptaciones personalizadas específicas de un proyecto. Esta funcionalidad permite flexibilidad mientras se mantiene la estructura original del módulo.

> Más detalles sobre cómo sobrescribir scripts se explicarán en la sección dedicada a los temas.

---

## Mejores Prácticas

- **Estructura y Organización**: Usa el directorio `js` como la ubicación principal para todos tus scripts y lógica personalizada. Esto fomenta el mantenimiento y asegura una estructura de proyecto clara.
- **Integración con Paquetes de Node.js**: Puedes integrar paquetes de Node.js en tus scripts para ampliar funcionalidades o escribir JavaScript puro si no necesitas dependencias externas.
- **Formato Predeterminado de JavaScript**: Todos los scripts deben usar **ESM (ECMAScript Modules)** de forma predeterminada. Esto asegura compatibilidad con navegadores modernos y promueve una arquitectura modular.

---

## ¿Cómo Funciona?

1. **Proceso de Compilación con Vite**  
    Todos los archivos JavaScript son procesados y compilados por **Vite**, lo que resulta en una salida optimizada. Esto garantiza:
    - Rendimiento mejorado a través de técnicas modernas de empaquetado.
    - Tree-shaking para incluir solo el código necesario en el paquete final.
    - Compilaciones más rápidas y reemplazo en caliente de módulos (HMR) durante el desarrollo.

2. **Descargas Optimizadas**  
    **{{ config.extra.components_name }}** adopta un enfoque centrado en el rendimiento:
    - Solo se descargan los archivos JavaScript explícitamente utilizados en el frontend.
    - El código no utilizado se excluye del paquete final, reduciendo los tiempos de carga y mejorando la eficiencia.

3. **Integración con Vistas**  
    Los archivos JavaScript pueden ser incluidos en tus vistas o plantillas `.phtml` según sea necesario. Ejemplos específicos sobre cómo integrar scripts se proporcionarán más adelante en esta documentación.

---

## Ejemplo de Estructura de Directorios

Aquí tienes una estructura sugerida para tus archivos JavaScript:

```
view/
└── frontend/
    └── web/
        ├── js/
        │   ├── main.js         // Punto de entrada para lógica personalizada
        │   ├── utils.js        // Funciones utilitarias reutilizables
        │   └── services/
        │       └── api.js      // Lógica de integración con API
        └── components/
            ├── navbar.vue      // Componente Vue para la barra de navegación
            └── modal.vue       // Componente Vue para un modal
```

Esta estructura asegura que el directorio `js` sea la ubicación principal para scripts personalizados, mientras que el directorio `components` puede usarse para lógica específica de componentes si es absolutamente necesario.

---

## Beneficios

- **Modularidad**: Mantener los scripts en directorios dedicados asegura un código limpio y fácil de mantener.
- **Flexibilidad**: Los scripts pueden ser sobrescritos en los temas para adaptarse a requisitos específicos.
- **Rendimiento**: Gracias al proceso de compilación de Vite, solo se incluye el JavaScript necesario en el paquete final, reduciendo los tiempos de carga.
- **Escalabilidad**: La capacidad de integrar paquetes de Node.js y escribir JavaScript modular asegura que tu base de código pueda crecer según las necesidades del proyecto.

---

## Notas Clave

- **Usa el directorio `js` como la ubicación principal para scripts personalizados.**
- Todos los archivos JavaScript deben usar **ESM (ECMAScript Modules)** como formato predeterminado.
- Los archivos ubicados en `view/frontend/web/js` y `view/frontend/web/components` son rastreados y procesados automáticamente.
- Los archivos JavaScript pueden ser sobrescritos en los temas. Los detalles sobre esto se explicarán en la sección sobre temas.
- El sistema asegura que solo los scripts explícitamente incluidos en el frontend sean descargados, siguiendo un enfoque centrado en el rendimiento.
- Ejemplos de cómo incluir archivos JavaScript en plantillas `.phtml` se proporcionarán en secciones posteriores.
