# Configuración de Compatibilidad

A diferencia de los módulos, **no recomendamos incluir soporte para {{ config.extra.components_name }} en temas existentes** que utilicen metodologías relacionadas con Luma o Blank. Este enfoque es radical y elimina completamente el soporte para tecnologías como LESS, Knockout, RequireJS, entre otros. Por lo tanto, sugerimos que este enfoque sea empleado únicamente en **temas nuevos** o en temas basados en **{{ config.extra.components_name }}**.

---

## Crear un Tema Compatible

Para crear un tema, primero sigue los pasos estándar descritos en la documentación oficial de Magento:  
[Creación de un tema en Magento](https://developer.adobe.com/commerce/php/tutorials/frontend/create-theme/)  

En resumen, necesitas crear una estructura como esta:

```
app/design/frontend/Vendor/ThemeName
```

### Archivos Básicos

Asegúrate de incluir los archivos mínimos necesarios para registrar un tema en Magento:

1. **registration.php**  
2. **theme.xml**  

### Declarar la Herencia del Tema

Al configurar el archivo `theme.xml`, presta atención si deseas heredar de un tema compatible. Si declaras un tema no compatible como tema padre, **la herencia será ignorada durante los pasos de compilación** y el tema no funcionará como se espera.

---

## Configuración de Compatibilidad del Tema

Para configurar un tema como compatible con **{{ config.extra.components_name }}**, sigue estos pasos:

1. **Crear el Archivo de Compatibilidad**  
        - Nombre del archivo:  
          `mage_obsidian_compatibility.xml`

        - Ruta del archivo:  
          Guarda el archivo en la siguiente ubicación:  
          ```
          app/design/frontend/Vendor/ThemeName/etc/mage_obsidian_compatibility.xml
          ```

2. **Agregar el Contenido del Archivo**  
        - Copia y pega el siguiente contenido en el archivo:

          ```xml
          <?xml version="1.0"?>
          <config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_theme_compatibility.xsd">
                <features>
                     <compatibility>true</compatibility>
                </features>
          </config>
          ```

---

## Pasos Finales

Una vez configurado el archivo de compatibilidad, es necesario ejecutar los siguientes comandos para integrar el tema en Magento y generar los metadatos necesarios:

1. **Cargar el tema en Magento**  
    ```bash
    bin/magento setup:upgrade
    ```

2. **Generar metadatos para {{ config.extra.components_name }}**  
    ```bash
    bin/magento mage-obsidian:frontend:config --generate
    ```

---

## Notas Finales

Con estos pasos, tu tema estará completamente integrado con **{{ config.extra.components_name }}**. Este enfoque garantiza que el tema aproveche al máximo las funcionalidades modernas de la arquitectura, eliminando dependencias de tecnologías obsoletas y promoviendo una experiencia más eficiente y limpia.
