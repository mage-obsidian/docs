# Configuración de CSS

En **{{ config.extra.components_name }}**, la inclusión de CSS personalizado desde módulos es sencilla y eficiente. El sistema rastrea automáticamente el siguiente punto de entrada en los módulos compatibles:  
```
app/code/Vendor/ModuleName/view/frontend/web/css/module.extend.css
```

Este archivo será incluido para cada módulo que lo defina, a menos que se configure explícitamente en el tema que se debe excluir (más detalles sobre esta funcionalidad se tratarán más adelante).

## ¿Cómo Funciona?

1. **Orden de Importación**  
    Los archivos CSS se cargan según la **prioridad de los módulos** definida en Magento. El orden se determina mediante la configuración de `sequence` en el archivo `module.xml` de cada módulo. Esto permite controlar el orden de importación del CSS de los módulos. Además, todo el CSS de los módulos se carga **antes del CSS de los temas**.
    
    Para más detalles sobre cómo configurar el orden de carga de los módulos, consulta la documentación oficial de Magento:  
    [Configurar el orden de carga de componentes](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

    Un ejemplo típico de orden de importación sería:

    ```css
    /* CSS de módulos */
    @import "/var/www/html/app/code/Vendor/ModuleA/view/frontend/web/css/module.extend.css"; /* Módulo A */
    @import "/var/www/html/app/code/Vendor/ModuleB/view/frontend/web/css/module.extend.css"; /* Módulo B */
    
    /* CSS de temas */
    @import "/var/www/html/app/design/frontend/Vendor/ThemeParent/web/css/theme.source.css"; /* Tema padre */
    @import "/var/www/html/app/design/frontend/Vendor/CurrentTheme/web/css/theme.source.css"; /* Tema actual */
    ```

    - **Módulos**: Si un módulo desea incluir CSS personalizado, debe usar el archivo ubicado en `view/frontend/web/css/module.extend.css` como su punto de entrada. **{{ config.extra.components_name }}** rastrea automáticamente estos archivos para módulos compatibles.
    - **Temas**: El punto de entrada del CSS de los temas siempre es `web/css/theme.source.css`.
    
2. **Flexibilidad con la Configuración del Tema**  
    Como se mencionó anteriormente, la configuración del tema permite **ignorar las entradas CSS de módulos específicos**. Esto brinda flexibilidad para determinar qué estilos se incluirán en la compilación final.

## Salida de CSS Optimizada

**{{ config.extra.components_name }}** utiliza **Tailwind CSS** y técnicas de tree-shaking para generar un único archivo CSS optimizado. Este archivo final incluye solo los estilos necesarios para el frontend, garantizando un tamaño mínimo y un rendimiento máximo.

## Beneficios Clave

- **Modularidad**: El CSS de los módulos se integra automáticamente sin esfuerzo adicional.
- **Control**: Ajusta el orden de importación utilizando la configuración de `sequence` en `module.xml`, o incluye/excluye CSS de módulos según las configuraciones del tema.
- **Rendimiento**: El archivo CSS final optimizado mejora los tiempos de carga y reduce el exceso de estilos innecesarios.
