# Módulos

## Cómo Crear un Módulo Compatible con {{ config.extra.components_name }}

Para que un módulo sea compatible con **{{ config.extra.components_name }}**, es necesario declarar un nuevo archivo XML en la ruta:

```
app/code/Vendor/ModuleName/etc
```

Este archivo debe extender el esquema definido en:

```
urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd
```

A continuación, se muestra un ejemplo del contenido que debe incluirse en el archivo:

> mage_obsidian_compatibility.xml

```xml
<?xml version="1.0"?>
<config xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd">
    <features>
        <compatibility>true</compatibility>
    </features>
</config>
```

## Detalles Clave

1. **Ruta del Archivo**: 
   - El archivo debe estar ubicado en `Vendor/ModuleName/etc/mage_obsidian_compatibility.xml`.

2. **Extensión del Esquema**:
   - La declaración `xsi:noNamespaceSchemaLocation` debe apuntar a `urn:magento:module:MageObsidian_ModernFrontend:etc/xsd/mage_obsidian_compatibility.xsd`.

3. **Estructura del XML**:
   - El nodo `<features>` incluye la etiqueta `<compatibility>` que debe estar configurada en `true` para declarar el módulo como compatible con **{{ config.extra.components_name }}**.

## Propósito
Este enfoque asegura que únicamente los módulos declarados explícitamente como compatibles puedan interactuar con las funcionalidades y arquitectura de **{{ config.extra.components_name }}**, promoviendo un desarrollo más limpio y controlado.
