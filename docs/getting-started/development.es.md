# Flujo de Desarrollo

**{{ config.site_name }}** dirige todo el ciclo de desarrollo del frontend desde `bin/magento`. Nunca editas a mano el `.env` de Vite: se **deriva de tu configuración de Magento** (Stores → Configuration → MageObsidian), que es la fuente única de verdad para el host, el puerto y los ajustes de HMR del dev server. Los comandos de abajo lo sincronizan por ti.

---

## El Ciclo de un Vistazo

Dos comandos manejan todo el ciclo — `--up` para entrar, `--down` para volver. Sin encadenar deploy mode + HMR + cache flush + dev server a mano.

```bash
# una vez: cablea nginx al dev server de Vite (pega el snippet en tu server block)
bin/magento mage-obsidian:frontend:dev --print-nginx

# entrar: modo developer + HMR on + .env sincronizado + caches flusheadas + dev server arriba
bin/magento mage-obsidian:frontend:dev --up               # pregunta el tema en una terminal
bin/magento mage-obsidian:frontend:dev --up --theme=Vendor/theme

# ...edita .vue / css / templates con HMR en vivo...

bin/magento mage-obsidian:frontend:dev --status   # ¿corriendo y alcanzable?

# volver a los assets construidos: detiene el dev server + HMR off + rebuild a disco
bin/magento mage-obsidian:frontend:dev --down
bin/magento mage-obsidian:frontend:dev --down --production   # además cambia a modo producción
```

`--up` es **probe-first**: si ya hay un dev server respondiendo (p. ej. uno que gestiona tu entorno), lo deja en paz en vez de arrancar un segundo. Es idempotente —seguro de re-correr. Omite `--theme` en una terminal y aparece un picker de los temas disponibles; pasa `--no-start` para setear solo el estado de Magento y dejar que tu entorno corra el servidor.

> **Docker / Zento.** En un proyecto Zento el dev server corre como el servicio gestionado `vite`, así que usa el wrapper: `zento frontend up [theme]` (setea el estado con `--no-start` y enciende el servicio) y `zento frontend down [--production]` (rebuildea y apaga el servicio). `zento frontend dev` sigue sirviendo para ver los logs de HMR.

---

## Comandos

### `mage-obsidian:frontend:dev`

Gestiona el `.env` de Vite y el dev server local.

| Opción | Qué hace |
|---|---|
| `--up [--theme=Vendor/theme] [--no-start]` | De una: modo developer + HMR on + sync `.env` + flush + dev server (probe-first). |
| `--down [--production]` | De una, de vuelta a los assets construidos: detiene el dev server + HMR off + flush + rebuild a disco. |
| `--sync-env` | Escribe `vite/.env` desde la config actual de Magento. |
| `--show` | Imprime las env vars derivadas de la config sin escribir el archivo. |
| `--start [--theme=Vendor/theme]` | Sincroniza el env y arranca el dev server de Vite (HMR). |
| `--start --no-watch [--theme=Vendor/theme]` | Construye el tema una vez a disco en lugar de correr el servidor (sin HMR, sin daemon). |
| `--stop` | Detiene el dev server arrancado por `--start`. |
| `--status` | Reporta si el proceso del dev server corre y es alcanzable. |
| `--print-nginx` | Imprime el snippet de proxy nginx (host/puerto desde la config) para pegar en tu server block. |

Cuando hace falta un tema (`--up`, `--start`) y omites `--theme`, el comando te deja elegir uno de los temas habilitados en una terminal, y falla ruidosamente (sin adivinar) si se corre de forma no interactiva. Arrancar siempre sincroniza el `.env` primero, así que rara vez llamas a `--sync-env` directamente. El comando corre el dev server **donde corre `bin/magento`**; correrlo en un contenedor distinto al del CLI es asunto de tu entorno (`--up` es probe-first, así que no duplica uno que tu entorno ya corra).

### `mage-obsidian:frontend:hmr`

HMR es un flag de configuración de Magento, ignorado en modo producción.

```bash
bin/magento mage-obsidian:frontend:hmr --enable
bin/magento mage-obsidian:frontend:hmr --disable
bin/magento mage-obsidian:frontend:hmr --show
```

Consulta [HMR](../components/modules/0110-hmr-configuration.md) para los detalles y el proxy de nginx.

### `mage-obsidian:frontend:doctor`

Diagnóstico de una sola pasada del entorno de desarrollo —modo de la app, el contrato (y drift), el flag de HMR, el alcance del dev server y las env vars requeridas. Cada chequeo se reporta ok / warn / error con una pista.

```bash
bin/magento mage-obsidian:frontend:doctor
```

Córrelo primero cuando algo no se comporte: suele señalar la causa (modo equivocado, HMR apagado, dev server inalcanzable, env var faltante, contrato desactualizado).

---

## Build a Disco

Para producir los assets construidos reales sin el dev server (inspección local o CI), usa `--no-watch`, o el bin de bajo nivel del engine. Consulta [Generación de Archivos Estáticos](../components/modules/0120-vite-build.md).

```bash
bin/magento mage-obsidian:frontend:dev --start --no-watch --theme=Vendor/theme
```

---

## Próximos Pasos

- [Generadores](scaffolding.md) — genera módulos, temas y componentes.
- [HMR](../components/modules/0110-hmr-configuration.md) — los detalles de recarga en vivo y nginx.
- [Generación de Archivos Estáticos](../components/modules/0120-vite-build.md) — deploy a producción.
