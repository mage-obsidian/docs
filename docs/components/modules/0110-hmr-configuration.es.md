# Configuración y Uso de HMR (Hot Module Replacement)

Hot Module Replacement (HMR) es una funcionalidad clave de **MageObsidian**, impulsada por Vite, que permite actualizaciones en tiempo real en tu frontend sin necesidad de refrescar el navegador. Esto mejora drásticamente la productividad al proporcionar retroalimentación instantánea durante el desarrollo.

---

> ⚠️ **Aviso Importante**  
> Las configuraciones descritas en esta sección son exclusivamente para **entornos de desarrollo**.  
> **No apliques estas configuraciones en entornos de producción**, ya que podrían exponer tu aplicación a riesgos innecesarios y degradar el rendimiento.

---

## Requisitos Previos: Configuración de Nginx

Una de las principales ventajas de Vite es su capacidad para gestionar HMR de manera eficiente. Sin embargo, para aprovechar esta funcionalidad en tu entorno Magento, necesitas configurar tu servidor Nginx para redirigir adecuadamente el tráfico al servidor de desarrollo de Vite.

### **1. Reglas Generales para Proxy de Vite**

Añade este bloque para manejar el tráfico específico de HMR y las conexiones WebSocket necesarias:

```nginx
location ~* ^/(?:@fs|@id|@vite|node_modules|__vite_ping|\.precompiled) {
    proxy_pass http://phpfpm:5173;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### **2. Reglas para Proxy de Recursos Estáticos**

Este bloque garantiza que los archivos estáticos generados por Vite, como CSS o JavaScript compilados, sean correctamente proxys:

```nginx
location ~* ^/static/frontend/.+/.+/.+/vite_generated/(.*)$ {
    proxy_pass http://phpfpm:5173/$1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # Habilitar WebSocket para HMR
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### **3. Ubicación de las Reglas de Proxy**

Asegúrate de colocar estas reglas debajo del bloque existente para recursos estáticos, como:

```nginx
location ~ ^/static/version\d*/ {
    rewrite ^/static/version\d*/(.*)$ /static/$1 last;
}
```

---

## 1. Iniciar el Servidor de Vite

El servidor de desarrollo de Vite debe estar en ejecución para que HMR funcione. Usa el siguiente comando para iniciarlo para un tema específico:

```bash
pnpm --prefix vite run dev:theme Vendor/theme
```

Este comando inicializa Vite, configurando su servidor HMR incorporado para escuchar en el host y puerto especificados.

### **Configuración del Entorno**

- El host y puerto del servidor Vite son configurables mediante variables de entorno.
- En la primera ejecución, si estas variables no están configuradas, Vite te pedirá configurarlas.

---

## 2. Configurar Magento para HMR

Asegúrate de que las siguientes configuraciones estén activas en tu entorno Magento:

1. **Modo Developer**:  
   Magento debe estar ejecutándose en modo developer. Actívalo con:
   ```bash
   bin/magento deploy:mode:set developer
   ```

2. **Configuración de HMR en MageObsidian**:  
   La clave de configuración `'mage-obsidian/hmr/enabled'` debe estar configurada en `true`. Este ajuste está habilitado por defecto al instalar **MageObsidian**.

---

## 3. Uso de HMR en tu Flujo de Trabajo

Una vez que todas las configuraciones estén en su lugar:

1. Inicia el servidor de Vite para tu tema:
   ```bash
   pnpm --prefix vite run dev:theme Vendor/theme
   ```

2. Abre tu sitio Magento en el navegador. Cualquier cambio realizado en el código de tu frontend se reflejará inmediatamente sin necesidad de recargar la página.

---

## Ventajas Clave de HMR en Vite

1. **Retroalimentación en Tiempo Real**:  
   Ve los cambios en tu frontend instantáneamente sin necesidad de recargar el navegador, mejorando drásticamente la velocidad de desarrollo.

2. **Actualizaciones Basadas en WebSocket**:  
   El uso de conexiones WebSocket por parte de Vite garantiza actualizaciones fluidas, incluyendo inyección de CSS en vivo y cambios en JavaScript.

3. **Gestión Optimizada de Recursos**:  
   Vite sirve dinámicamente los recursos, evitando recompilaciones completas y reduciendo la sobrecarga del servidor de desarrollo.

4. **Configuración Sencilla**:  
   Con Nginx y las variables de entorno configuradas correctamente, el flujo de trabajo es fluido.

---

## Ejemplo de Flujo de Trabajo

1. **Editar un Archivo CSS**:  
   Modifica un archivo en `view/frontend/web/css/module.extend.css`. El navegador se actualiza instantáneamente.

2. **Editar un Componente Vue**:  
   Actualiza un componente en `view/frontend/web/components`. HMR reemplaza dinámicamente el módulo y el cambio aparece inmediatamente.

3. **Observar Resultados**:  
   Sin recargas de página. Sin intervenciones manuales. Solo actualizaciones instantáneas.

---

## Solución de Problemas

1. **HMR No Funciona**:  
   - Asegúrate de que el servidor de Vite esté ejecutándose en el host y puerto correctos.
   - Verifica que Nginx esté configurado correctamente para hacer proxy al tráfico de HMR.

2. **Archivos Estáticos No se Actualizan**:  
   - Comprueba que la configuración `'mage-obsidian/hmr/enabled'` esté en `true`.
   - Asegúrate de que Magento esté en modo developer.

3. **Problemas con Variables de Entorno**:  
   - Asegúrate de que las variables de entorno para el host y puerto de Vite estén configuradas correctamente.

---

Con HMR configurado, puedes aprovechar al máximo las herramientas modernas de Vite y disfrutar de un proceso de desarrollo más rápido y fluido con **MageObsidian**.
