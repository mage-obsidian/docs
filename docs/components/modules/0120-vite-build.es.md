# Generación de Archivos Estáticos para Producción

Al desplegar un sitio Magento en producción, es fundamental generar archivos estáticos optimizados. **MageObsidian** utiliza Vite para procesar y empaquetar los recursos del frontend, asegurando un rendimiento óptimo. Esta sección explica cómo generar estos archivos para entornos de producción.

---

## Pasos para Generar Archivos Estáticos

### **1. Generar Archivos Estáticos para Todos los Temas Compatibles**

Para procesar y generar todos los archivos estáticos para todos los temas compatibles, ejecuta el siguiente comando:

```bash
pnpm --prefix vite run build
```

Este comando:

- Procesa todos los recursos del frontend (CSS, JavaScript, componentes Vue, etc.) usando Vite.
- Genera archivos estáticos completamente optimizados y listos para producción.

---

### **2. Generar Archivos Estáticos para un Tema Específico**

Si deseas generar archivos estáticos para un solo tema, utiliza este comando:

```bash
pnpm --prefix vite run build:theme Vendor/Theme
```

Reemplaza `Vendor/Theme` con el espacio de nombres y el nombre de tu tema deseado. Esto es útil para despliegues que involucren múltiples temas o actualizaciones incrementales.

---

## Notas Importantes

1. **Orden de Ejecución**:  
   Siempre ejecuta el comando de compilación de Vite antes de desplegar el contenido estático de Magento:
   ```bash
   bin/magento setup:static-content:deploy
   ```

2. **¿Por Qué Este Orden?**  
   - El comando `vite build` asegura que todos los recursos relacionados con los temas estén procesados y listos.  
   - El comando `setup:static-content:deploy` de Magento incluirá los archivos generados por Vite en el paquete final de despliegue.

3. **Archivos Optimizados**:  
   Vite se encarga automáticamente de:
   - Minificar los archivos JavaScript y CSS.
   - Aplicar tree-shaking para incluir solo el código necesario.
   - Generar hashes para el versionado de los recursos y evitar problemas de caché.

4. **Temas Compatibles**:  
   Asegúrate de que tus temas sean compatibles con **MageObsidian** antes de ejecutar estos comandos. Los temas sin la configuración requerida no generarán archivos.

---

## Ejemplo de Flujo de Trabajo

1. **Generar Recursos para Todos los Temas**:
   ```bash
   pnpm --prefix vite run build
   ```

2. **Desplegar Contenido Estático**:
   ```bash
   bin/magento setup:static-content:deploy
   ```

3. **Limpiar Caché** (si es necesario):
   ```bash
   bin/magento cache:flush
   ```

---

## Beneficios de Usar Vite para Archivos Estáticos

1. **Rendimiento Optimizado**:  
   Vite asegura que tus recursos estén minificados y optimizados para una carga rápida.

2. **Herramientas Modernas**:  
   Aprovecha las capacidades de empaquetado de última generación de Vite, incluido el soporte para módulos ES.

3. **Integración Sencilla**:  
   Los archivos generados son automáticamente compatibles con el proceso de despliegue de contenido estático de Magento.

---

Siguiendo estos pasos, puedes asegurarte de que los recursos de tu frontend estén completamente optimizados y listos para producción, proporcionando una experiencia fluida a tus usuarios.
