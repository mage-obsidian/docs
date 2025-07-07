# HMR (Hot Module Replacement)

Hot Module Replacement (HMR) es una característica central de **MageObsidian** impulsada por Vite: actualiza tu frontend en el navegador en tiempo real, sin recargar la página completa. Esta página cubre las piezas específicas de HMR; para el ciclo completo del día a día (arrancar/detener el servidor, sincronizar el env, diagnóstico) consulta [Flujo de Desarrollo](../../getting-started/development.md).

---

> ⚠️ **Aviso Importante**
> HMR es una característica **solo de desarrollo**. El flag de HMR se ignora cuando Magento corre en modo **producción**, así que no hay nada que deshacer antes de salir a producción.

---

## 1. Habilitar HMR

HMR es un flag de configuración de Magento, que se activa con un comando —sin editar archivos:

```bash
bin/magento mage-obsidian:frontend:hmr --enable
bin/magento mage-obsidian:frontend:hmr --show      # ver el estado actual
bin/magento mage-obsidian:frontend:hmr --disable   # volver a apagarlo
```

Magento además debe estar en **modo developer** (`bin/magento deploy:mode:set developer`); en producción el flag se ignora.

## 2. Configurar Nginx

El navegador debe poder alcanzar el dev server de Vite para que funcione HMR. Genera el snippet de proxy derivado de tu configuración y pégalo en tu server block:

```bash
bin/magento mage-obsidian:frontend:dev --print-nginx
```

El snippet enruta el tráfico HMR de Vite (con soporte WebSocket) y los assets generados hacia el dev server, por ejemplo:

```nginx
location ~* ^/(?:@fs|@id|@vite|node_modules|__vite_ping|\.precompiled) {
    proxy_pass http://<vite-host>:<vite-port>;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}

location ~* ^/static/frontend/.+/.+/.+/vite_generated/(.*)$ {
    proxy_pass http://<vite-host>:<vite-port>/$1;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
}
```

Coloca estas reglas **debajo** de tu rewrite de static-version existente (`location ~ ^/static/version\d*/ { ... }`). El host y el puerto vienen de tu configuración de MageObsidian —no los eliges a mano; `--print-nginx` los rellena.

## 3. Arrancar el Dev Server

```bash
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme
```

Esto sincroniza el `.env` de Vite desde tu config de Magento y lanza el dev server con HMR. Abre tu tienda —los cambios en un componente `.vue`, un `module.extend.css` o una fuente del tema se reflejan al instante. Deténlo con `--stop`, compruébalo con `--status`. Consulta [Flujo de Desarrollo](../../getting-started/development.md) para el conjunto completo de comandos.

---

## Resolución de Problemas

Ejecuta el doctor —comprueba el modo de la app, el flag de HMR, el alcance del dev server, el contrato y el env de una sola vez:

```bash
bin/magento mage-obsidian:frontend:doctor
```

Causas comunes cuando HMR "no actualiza":

- **Flag de HMR apagado o modo producción** — `mage-obsidian:frontend:hmr --show`; el flag se ignora fuera de modo developer.
- **Nginx no proxya a Vite** — regenera y vuelve a pegar el snippet con `--print-nginx`; confirma que el dev server es alcanzable (`--status` / doctor).
- **Dev server no corriendo** — `mage-obsidian:frontend:dev --status`, luego `--start --theme=…`.

---

Con HMR habilitado y el proxy en su lugar, obtienes inyección de CSS y actualización de componentes al instante —sin recargas de página, sin rebuilds manuales.
