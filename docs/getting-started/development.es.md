# Flujo de Desarrollo

**{{ config.site_name }}** dirige todo el ciclo de desarrollo del frontend desde `bin/magento`. Nunca editas a mano el `.env` de Vite: se **deriva de tu configuración de Magento** (Stores → Configuration → MageObsidian), que es la fuente única de verdad para el host, el puerto y los ajustes de HMR del dev server. Los comandos de abajo lo sincronizan por ti.

---

## El Ciclo de un Vistazo

```bash
# una vez: pon Magento en modo developer y enciende HMR
bin/magento deploy:mode:set developer
bin/magento mage-obsidian:frontend:hmr --enable

# una vez: cablea nginx al dev server de Vite (pega el snippet en tu server block)
bin/magento mage-obsidian:frontend:dev --print-nginx

# día a día: arranca el dev server para el tema en el que trabajas
bin/magento mage-obsidian:frontend:dev --start --theme=Vendor/theme

# ...edita .vue / css / templates con HMR en vivo...

bin/magento mage-obsidian:frontend:dev --status   # ¿corriendo y alcanzable?
bin/magento mage-obsidian:frontend:dev --stop     # detén al terminar
```

---

## Comandos

### `mage-obsidian:frontend:dev`

Gestiona el `.env` de Vite y el dev server local.

| Opción | Qué hace |
|---|---|
| `--sync-env` | Escribe `vite/.env` desde la config actual de Magento. |
| `--show` | Imprime las env vars derivadas de la config sin escribir el archivo. |
| `--start --theme=Vendor/theme` | Sincroniza el env y arranca el dev server de Vite (HMR). |
| `--start --no-watch --theme=Vendor/theme` | Construye el tema una vez a disco en lugar de correr el servidor (sin HMR, sin daemon). |
| `--stop` | Detiene el dev server arrancado por `--start`. |
| `--status` | Reporta si el proceso del dev server corre y es alcanzable. |
| `--print-nginx` | Imprime el snippet de proxy nginx (host/puerto desde la config) para pegar en tu server block. |

`--start` requiere `--theme`. Arrancar siempre sincroniza el `.env` primero, así que rara vez llamas a `--sync-env` directamente —está para inspección o scripting. El comando corre el dev server **donde corre `bin/magento`**; correrlo en un contenedor distinto al del CLI es asunto de tu entorno.

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
