# Generación de Archivos Estáticos

**MageObsidian** utiliza Vite para procesar y empaquetar los recursos del frontend (CSS, JavaScript, componentes Vue). Esta página cubre cómo generar esos recursos a disco —para inspección local sin HMR, para CI y para el despliegue a producción.

---

## Build de un Tema a Disco (sin HMR)

Para construir un único tema una vez a disco —los mismos artefactos que recibiría un navegador, pero escritos en `web/generated` en lugar de servidos por el dev server— usa el comando de dev con `--no-watch`:

```bash
bin/magento mage-obsidian:frontend:dev --start --no-watch --theme=Vendor/theme
```

Es el inverso de `--start` (HMR): sin daemon, sin watch —corre un build y termina. Útil para inspeccionar la salida real o reproducir un build de CI en local.

> Salir del ciclo de dev con `bin/magento mage-obsidian:frontend:dev --down` corre este mismo build por ti (HMR off + rebuild a disco). Usa `--no-watch` directo cuando solo quieras un build puntual sin tocar HMR.

### El bin del engine por debajo

`frontend:dev` envuelve el bin propio del engine de build, que también puedes correr directamente desde el harness `vite/` (es lo que usa CI):

```bash
# desde el directorio vite/ del componente
mage-obsidian:build-themes                  # construir todos los temas compatibles
mage-obsidian:build-themes --theme Vendor/theme   # construir uno
```

`frontend:dev` es el punto de entrada del lado Magento (primero deriva el `.env` de Vite desde tu config); `build-themes` es el comando de bajo nivel del engine. Ambos producen la misma salida.

---

## Despliegue a Producción

Para producción **no** corres un paso de build aparte. MageObsidian se engancha al deploy de contenido estático estándar de Magento: sus plugins de deploy excluyen los temas modernos del pipeline legacy de Less/RequireJS y producen/inyectan la salida de Vite como parte del comando normal:

```bash
bin/magento deploy:mode:set production
bin/magento setup:static-content:deploy
```

Los assets generados por Vite quedan en el contenido estático desplegado junto a todo lo demás. Vite se encarga de la minificación, el tree-shaking y el hashing de assets para cache-busting automáticamente.

> **Solo temas compatibles.** Solo los temas que entregan `etc/mage_obsidian_compatibility.xml` (y han sido detectados por `mage-obsidian:frontend:config --generate`) pasan por el pipeline de Vite. Los temas sin él siguen el deploy nativo de Magento intacto.

### Requisitos del servidor

Como el build de Vite corre *dentro* de `setup:static-content:deploy`, la máquina que ejecute ese comando necesita el toolchain JS de [Requisitos](../../getting-started/requirements.md) —Node ≥ 22 y pnpm ≥ 11— además de PHP. Esto aplica a tu servidor de deploy, imagen de CI o build server, no solo a las máquinas de desarrollo. Si tu pipeline construye el contenido estático en un build host separado, solo ese host necesita Node/pnpm.

> **Mismatch de versión con corepack.** `vite/package.json` fija la versión exacta de pnpm vía el campo `packageManager`. Si el servidor tiene corepack habilitado con otro pnpm activo, el build aborta con un error de version-mismatch antes de hacer nada. Se arregla activando la versión fijada:
>
> ```bash
> corepack prepare pnpm@11.7.0 --activate
> ```
>
> (Ajusta la versión al pin `packageManager` vigente en `vite/package.json`.)

---

## Beneficios

- **Salida optimizada** — assets minificados, con tree-shaking y hash, listos para producción.
- **Integración nativa** — los builds de producción ocurren dentro de `setup:static-content:deploy`; sin paso extra en tu pipeline de deploy.
- **Coexistencia** — los temas legacy siguen usando el deploy estático nativo de Magento; solo los temas modernos usan Vite.

---

Consulta [Flujo de Desarrollo](../../getting-started/development.md) para el dev server con HMR y el conjunto completo de comandos, y [HMR](0110-hmr-configuration.md) para la recarga en vivo durante el desarrollo.
