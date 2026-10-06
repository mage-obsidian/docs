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

!!! tip "Ejecuta primero el export del CMS"
    ```bash
    bin/magento mage-obsidian:cms:export
    ```
    Tailwind escanea archivos y el contenido CMS vive en una base de datos. El export lo vuelca para
    que el build cubra las clases escritas en páginas y bloques; sin él, esas clases caen al delta de
    runtime. Ver [Contenido CMS](cms.md).

---

## Despliegue a Producción

Los builds de producción corren dentro del deploy de contenido estático de Magento. Consulta [Despliegue a producción](../../getting-started/deploy.md).

---

## Beneficios

- **Salida optimizada** — assets minificados, con tree-shaking y hash, listos para producción.
- **Integración nativa** — los builds de producción ocurren dentro de `setup:static-content:deploy`; sin paso extra en tu pipeline de deploy.
- **Coexistencia** — los temas legacy siguen usando el deploy estático nativo de Magento; solo los temas modernos usan Vite.

---

Consulta [Flujo de Desarrollo](../../getting-started/development.md) para el dev server con HMR y el conjunto completo de comandos, y [HMR](hmr.md) para la recarga en vivo durante el desarrollo.
