{% raw %}
# Performance y compatibilidad con la build-config nativa

**MageObsidian** sirve cada hoja de estilos y script a través de **Vite**, no de los pipelines legacy de Magento (Less/RequireJS). Eso cambia cómo se comportan los flags nativos de build y habilita una optimización opcional que conviene entender: el **critical CSS**.

Esta página cubre ambas cosas: la función opt-in de critical CSS, y cómo los flags `dev/js/*`, `dev/css/*` y `dev/template/minify_html` de Magento interactúan con un theme Obsidian.

---

## Critical CSS (opcional)

En un theme Obsidian, el único recurso que bloquea el render en el head es la hoja de Vite (`style.css`). El critical CSS inyecta el CSS above-the-fold dentro del `<head>` y difiere esa hoja, de modo que el primer pintado ya no la espera.

Viene **desactivado por defecto** y es **opt-in**.

### Reusa el flag nativo

No hay **ninguna config propia de MageObsidian**. La función reusa el interruptor de Magento, `dev/css/use_css_critical_path` (off por defecto). Al activarlo, MageObsidian inyecta el critical CSS del handle de layout actual y difiere la hoja.

### El defer es per-página, no global

El interruptor nativo también activa el `AsyncCssPlugin`, que reescribe **todos** los `<link rel="stylesheet">` de la respuesta a una carga asíncrona (`media="print"`) — de forma global. En cualquier página **sin** critical CSS inyectado, eso produce un flash de contenido sin estilos (FOUC).

MageObsidian lo evita:

- **Neutraliza el `AsyncCssPlugin` solo para themes Obsidian** (los themes legacy y el admin conservan el comportamiento nativo).
- Difiere la hoja **por página**, en el template del head, **acoplado a si existe critical CSS para el handle activo**. Una página sin critical mantiene la hoja bloqueante — nunca se difiere sin su contraparte inline, así que nunca hay FOUC.

### Generar el critical CSS

El critical CSS se extrae de la **página renderizada real** (para que refleje el markup above-the-fold de verdad) con [Beasties](https://github.com/danielroe/beasties), mediante un comando de consola:

```bash
bin/magento mage-obsidian:frontend:critical-css --handle cms_index_index
```

El comando renderiza la URL, extrae el subconjunto crítico, reescribe el `url(...)` de los `@font-face` a una URL estática absoluta (root-relative) para que las fuentes self-hosted resuelvan al inyectarse en `<head>`, y escribe `web/generated/critical/<handle>.css` en el theme activo. Córrelo **después** del build del theme y de `setup:static-content:deploy`, porque lee la hoja construida y resuelve las URLs estáticas desplegadas.

| Opción | Default | Para qué |
|---|---|---|
| `--handle` | `cms_index_index` | Handle de layout del critical CSS. |
| `--url` | base URL segura del store | La página a renderizar. |
| `--store` | store view por defecto | Store a emular. |
| `--insecure` | off | Omite la verificación TLS (certificados self-signed de dev). |
| `--resolve` | — | Una entrada `host:port:ip` de curl, para entornos locales detrás de un host propio. |
| `--node` / `--bin` | `node` / bin incluido | Sobrescribe el binario de Node o el script extractor. |

La home (`cms_index_index`) es la página del LCP y el objetivo por defecto. Genera otros handles pasando `--handle`/`--url`; cualquier handle sin archivo generado degrada simplemente a la hoja bloqueante.

### Activarlo

```bash
bin/magento config:set dev/css/use_css_critical_path 1
bin/magento mage-obsidian:frontend:critical-css --handle cms_index_index
bin/magento cache:flush
```

El flag tiene scope por store view. Si el archivo generado falta o no se puede leer, el head cae a un stub mínimo de `[v-cloak]` y la hoja bloqueante normal — la página siempre es correcta.

### Cuándo no usarlo

El critical CSS es un trade-off: inyecta CSS en cada página cacheada (más HTML) para eliminar una petición bloqueante. Si un proyecto no lo quiere, **deja `dev/css/use_css_critical_path` apagado** — la hoja sigue bloqueante, que detrás de Varnish con gzip/brotli y HTTP/2 ya carga en decenas de milisegundos. No hay que cambiar nada más.

---

## Flags nativos de build

### Merge y minify de JS/CSS — inertes

`dev/js/merge_files`, `dev/js/minify_files`, `dev/css/merge_css_files`, `dev/css/minify_files` **no tienen efecto** en un theme Obsidian. Esos flags actúan sobre la `AssetCollection` de Magento; MageObsidian emite su CSS y JS directo desde la salida de Vite (el importmap, el `<link>`, el `<script type="module">`), que nunca entra en esa colección. Puedes dejarlos en cualquier valor — la minificación y el bundling ya los resuelve el build de Vite.

### Minificación de HTML — desactivada por theme

`dev/template/minify_html` se **desactiva para los themes Obsidian** (el admin y los themes legacy siguen minificando). Por dos razones:

- En producción, sin `force_html_minification` ni SCD-on-demand, Magento devuelve la ruta a un template `.min` pre-generado **sin crearlo**; ese archivo nunca existe para el pipeline Vite/Twig, así que el include falla con HTTP 500.
- El minificador por regex puede corromper el JSON inline que emite el runtime — `data-props` de las islas, el importmap, el JSON-LD — un riesgo sin ganancia real (Varnish + gzip/brotli ya colapsan el whitespace; el delta post-compresión es ~1–3 %).

Puedes dejar el flag activo globalmente; el storefront no se ve afectado.
{% endraw %}
