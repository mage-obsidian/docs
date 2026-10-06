---
description: "Las variables de entorno que leen el harness de Vite y el motor de build, con su propósito y valor por defecto."
---
# Variables de entorno

El motor de compilación lee estas variables del entorno o del archivo `vite/.env` (ver `vite/.env.sample`). `bin/magento mage-obsidian:frontend:dev --sync-env` escribe `vite/.env` a partir de la configuración de Magento.

| Variable | Usada por | Propósito | Por defecto |
|---|---|---|---|
| `CURRENT_THEME` | `mage-obsidian:build-themes`, `vite.config.js` | Tema sobre el que trabaja la compilación o el servidor de desarrollo de Vite (`Vendor/theme`). `mage-obsidian:build-themes` lo fija para cada tema que compila, así que no hace falta definirlo a mano. | Lo fija `build-themes` por tema |
| `MAGENTO_HOST` | `vite.config.js` | Host público fijo para el websocket de HMR. Déjalo vacío en configuraciones multi-website con un tema compartido para que el cliente de Vite derive el host desde `window.location`. `frontend:dev --sync-env` lo escribe a partir de `mage_obsidian/dev_server/public_host`. | `magento.test` (`.env.sample`) |
| `MAGE_OBSIDIAN_BUILD_CONCURRENCY` | `mage-obsidian:build-themes` | Número máximo de temas que se compilan en paralelo. Debe ser un entero de 1 o más; cualquier otro valor usa el valor por defecto. El resultado no supera el número de temas. | Núcleos de CPU menos 1 |
| `MAGE_OBSIDIAN_MAGENTO_ROOT` | `js-package-utils` (`config/default.ts`) | Raíz explícita de Magento, usada para ubicar `app/etc/mage_obsidian_frontend_modules.json`. Defínela cuando el motor no se ejecuta desde el directorio `vite/` un nivel por debajo de la raíz de Magento. | Directorio padre del directorio de trabajo |
| `MAGE_OBSIDIAN_TYPES_PATH_MAP` | `js-package-utils` (`core/generateJsconfig.ts`) | Opcional. Reescribe las rutas absolutas del `jsconfig.json` generado del tema para que ir a la definición y el autocompletado apunten a donde tu editor abre los archivos. Solo es necesario cuando la compilación corre en un sistema de archivos o montaje distinto al de tu editor (por ejemplo un contenedor). Formato: `from=>to`, separado por comas para varios montajes; gana el `from` más largo que coincida. | Sin definir |
| `VITE_HMR_PATH` | `vite.config.js` | Ruta del websocket de HMR. También lo informa `frontend:dev --show` y lo revisa `frontend:doctor`. Se obtiene de `mage_obsidian/dev_server/hmr_path`. | `/__vite_ping` |
| `VITE_SERVER_ALLOWED_HOSTS` | `vite.config.js` | Lista separada por comas de los hosts autorizados a llegar al servidor de desarrollo. Cada host de la tienda que sirva el tema en desarrollo debe estar en la lista, o Vite responde con 403 a sus peticiones de assets. Se obtiene de `mage_obsidian/dev_server/allowed_hosts`. | `magento.test,localhost` (`.env.sample`) |
| `VITE_SERVER_HOST` | `mage-obsidian:build-themes --dev-server`, `vite.config.js` | Host al que se enlaza el servidor de desarrollo. Obligatoria para el servidor de desarrollo; además se añade a los hosts permitidos. Se obtiene de `mage_obsidian/dev_server/host`. | `phpfpm` (`.env.sample`) |
| `VITE_SERVER_PORT` | `mage-obsidian:build-themes --dev-server`, `vite.config.js` | Puerto en el que escucha el servidor de desarrollo. Obligatoria para el servidor de desarrollo. Se obtiene de `mage_obsidian/dev_server/port`. | `5173` |
| `VITE_SERVER_SECURE` | `vite.config.js` | Usa `wss` en lugar de `ws` para el socket de HMR. Acepta `true`, `1`, `yes` u `on` (sin distinguir mayúsculas); cualquier otro valor significa `ws`. Se obtiene de `mage_obsidian/dev_server/secure`. | `true` (`.env.sample`) |
