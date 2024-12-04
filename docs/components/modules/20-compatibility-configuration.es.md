# Configuración de Compatibilidad

Para hacer que un módulo sea compatible con **{{ config.extra.components_name }}**, sigue estos pasos. El proceso es el mismo tanto si estás creando un nuevo módulo como si estás añadiendo compatibilidad a uno existente.

Si estás creando un nuevo módulo, consulta la documentación oficial de Magento:  
[Creación de un módulo en Magento](https://experienceleague.adobe.com/en/docs/commerce-learn/tutorials/backend-development/create-module)

Una vez que el módulo esté listo, incluye la configuración de compatibilidad como se describe a continuación.

---

## Pasos para Configurar la Compatibilidad

1. **Crear el Archivo de Compatibilidad**  
        - Nombre del archivo:  
            `mage_obsidian_compatibility.xml`

        - Ruta del archivo:  
            Guarda el archivo en la siguiente ubicación:  
            ```
            app/code/Vendor/ModuleName/etc/mage_obsidian_compatibility.xml
            ```

2. **Agregar el Contenido del Archivo**  
        - Copia y pega el siguiente contenido en el archivo:
            ```xml
            <?xml version="1.0"?>
            <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                        xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
                    <features>
                        <compatibility>true</compatibility>
                    </features>
            </config>
            ```

---

## Pasos Finales

Después de configurar el archivo de compatibilidad, debes ejecutar los siguientes comandos para integrar el módulo en Magento y generar los metadatos necesarios:

1. **Cargar el Módulo en Magento**  
    ```bash
    bin/magento setup:upgrade
    ```

2. **Generar metadatos para {{ config.extra.components_name }}**  
    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

---

## Detalles Clave

- El archivo de compatibilidad debe guardarse en la siguiente ruta:  
  `Vendor/ModuleName/etc/mage_obsidian_compatibility.xml`

- La declaración `xsi:noNamespaceSchemaLocation` ya apunta al esquema requerido:  
  `urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd`

- El nodo `<features>` incluye la etiqueta `<compatibility>`, que debe configurarse como `true` para indicar compatibilidad con **{{ config.extra.components_name }}**.

---

## Propósito

Esta configuración asegura que solo los módulos declarados explícitamente como compatibles puedan interactuar con las funcionalidades y la arquitectura de **{{ config.extra.components_name }}**, logrando un proceso de desarrollo más organizado y confiable.

---

## Flexibilidad Futura

Esta estructura está diseñada para soportar mejoras futuras. Al actualizar este archivo XML, será posible activar o desactivar nuevas funcionalidades introducidas en **{{ config.extra.components_name }}**. Este enfoque ofrece mayor flexibilidad y control sobre el comportamiento de los módulos, permitiendo una adopción fluida de las nuevas características.
