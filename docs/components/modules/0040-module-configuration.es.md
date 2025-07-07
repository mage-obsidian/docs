# Configuración de Módulos

En **{{ config.extra.components_name }}**, cada módulo compatible puede incluir configuraciones adicionales creando un archivo de configuración en:

```
view/frontend/web/module.config.js
```

Este archivo es un **módulo ESM (ECMAScript)** que hace `export default` de un objeto de configuración leído por **{{ config.extra.components_name }}**.

## ¿Cómo Funciona?

1. **Carga de Archivos de Configuración**  
    Los archivos de configuración se cargan en el orden definido por la configuración de `sequence` en el archivo `module.xml` de cada módulo.
    
    > Para más detalles sobre cómo definir el orden de carga de los módulos, consulta la documentación oficial de Magento:  
    [Configurar el orden de carga de componentes](https://developer.adobe.com/commerce/php/development/build/component-load-order/).

2. **Ejemplo de Archivo de Configuración**  
    Un ejemplo básico de un archivo `module.config.js` sería:

    ```javascript
    export default {
         tailwind: {
              // Configuración de Tailwind CSS
         }
    };
    ```

    Actualmente, la única opción de configuración disponible es para **Tailwind CSS**, pero en futuras actualizaciones se ampliará esta funcionalidad para incluir más opciones específicas de los módulos.

3. **Sobrescribir Configuraciones de los Módulos**  
    Las configuraciones de los módulos pueden ser sobrescritas directamente en los temas creando un archivo de configuración correspondiente. Por ejemplo:

    ```
    app/design/frontend/Vendor/Theme/Vendor_Module/web/module.config.js
    ```

    - Cuando este archivo existe, **reemplaza por completo** la configuración original proporcionada por el módulo.
    - La configuración en el tema no se trata como una extensión ni se combina (merge) con el archivo original; en su lugar, lo sobrescribe completamente.

---

## Beneficios y Potencial Futuro

- **Personalización**: Las configuraciones de los módulos se pueden adaptar para satisfacer las necesidades de proyectos o temas específicos sin modificar el código del módulo.
- **Escalabilidad**: El sistema de configuración está diseñado para admitir más opciones en futuras versiones, brindando mayor flexibilidad a los desarrolladores de módulos.
- **Control**: Los temas tienen la capacidad de sobrescribir completamente las configuraciones de los módulos, asegurando una separación clara de responsabilidades y evitando efectos no deseados.

---

## Notas Clave

- El archivo es un módulo **ESM** (`export default`), coherente con el engine de build ESM-only.
- Las configuraciones se cargan según la secuencia definida en `module.xml`. Para obtener más información, consulta la [documentación oficial de Magento](https://developer.adobe.com/commerce/php/development/build/component-load-order/).
- Las configuraciones sobrescritas en los temas reemplazan completamente las configuraciones originales del módulo, sin combinarlas ni extenderlas.
