# Islas Vue

En **{{ config.extra.components_name }}**, cada componente Vue renderizado desde una plantilla `.phtml` (o `.twig`) se monta como una **isla**: una app Vue autocontenida adosada a un único marcador en la página, hidratada de forma independiente del resto del documento.

El método puente de `.phtml` [`renderVueComponent`](0090-phtml-configuration.md#2-renderizado-de-componentes-vue) no emite un script de montaje en línea. Emite un marcador que un único bootstrap de página descubre y monta — por defecto solo cuando el marcador entra en el viewport.

Así se ve en una página de producto real sobre una conexión limitada: el HTML renderizado en el servidor pinta primero —legible antes de que se ejecute un solo byte de Vue— y luego las islas se hidratan a medida que llegan sus chunks:

<video autoplay loop muted playsinline style="max-width:100%;border-radius:8px" src="/assets/islands-hydration.mp4"></video>

---

## Por Qué Islas

- **Un bootstrap por página, no uno por componente.** El runtime de Vue y el plugin de i18n se importan **una vez** y los comparten todas las islas, en lugar de que cada llamada a `renderVueComponent` los reimporte.
- **Costo cero cuando no hay islas.** El bootstrap revisa primero si hay marcadores; si no los hay, retorna antes de importar Vue o el diccionario. Una página sin islas no envía Vue en absoluto.
- **Lazy por defecto.** Los componentes por debajo del pliegue no se hidratan —ni siquiera se descarga su módulo— hasta que entran en el viewport.
- **Se preserva el aislamiento.** Cada isla sigue siendo su propia app Vue, así que un componente que falla o se re-renderiza nunca afecta a otro.

---

## Los Dos Modos

Una isla puede **poseer** su markup o **adoptar** el markup que renderizó el servidor. Esa elección decide si el componente aparece de la nada o si simplemente ya está desde el primer pintado.

| Modo | Quién posee el markup | Úsalo para |
|---|---|---|
| **mount** (por defecto) | el componente | UI que no existe sin JS: modales, drawers, toasts, autocomplete. Manténla lazy, o fuera del flujo del documento. |
| **hydrate** | la plantilla, adoptado por el componente | todo lo que esté por encima del pliegue y en el flujo: buy boxes, navegación, formularios. |

### mount

El marcador está vacío (o lleva un placeholder) y Vue renderiza el componente dentro, reemplazando lo que hubiera:

```php
<?= $block->renderVueComponent('Vendor_Module::Toast', $props, true) ?>
```

Es lo correcto cuando el componente no tiene un estado significativo del lado del servidor: un host de toasts no tiene nada que mostrar hasta que ocurre algo. Es incorrecto para cualquier cosa que ocupe espacio en la página: el contenedor está vacío cuando el documento pinta y crece cuando llega el chunk, empujando hacia abajo todo lo que está debajo.

### hydrate

La plantilla renderiza el estado inicial del componente y Vue se adosa a ese DOM en lugar de recrearlo:

```php
<?= $block->renderVueComponent('Vendor_Module::BuyBox', $props, true, $serverHtml, true) ?>
```

Nada se mueve, porque nada se inserta: el markup ya estaba en pantalla, y sigue siendo legible si el chunk tarda o no llega nunca.

Eso no es lo mismo que decir que la página *funciona* sin JavaScript. Depende del markup: el add-to-cart de la tarjeta de producto es un `<form>` real que postea a `checkout/cart/add`, así que funciona igual; el form de la isla del configurable no tiene action y sus swatches son botones, por eso sigue enviando un `<noscript>`. La hidratación preserva lo que el servidor renderizó — no lo vuelve funcional.

La hidratación es **opt-in** mediante ese quinto argumento, y a propósito. Vue adopta el markup del servidor solo si coincide con lo que el componente renderizaría; un markup que apenas lo aproxima no coincide y se re-renderiza, que es exactamente el reflow que este mecanismo existe para evitar. Pasar markup sin `$hydrate` lo mantiene como placeholder que Vue limpia al montar — seguro, y no peor que un contenedor vacío.

---

## Escribir el Markup del Servidor

El estado inicial debe coincidir con lo que renderiza el componente. Lo que cuenta es la estructura: **la secuencia de elementos, los anclajes de fragmento y el texto**. Las clases, los estilos y los atributos se comparan semánticamente, así que el orden de las clases y el formato del style son libres.

### Generarlo

La salida SSR de Vue marca un `v-for` con `<!--[-->` / `<!--]-->` y un `v-if` falso con `<!---->`, porque un fragmento no posee ningún elemento propio y la hidratación necesita saber dónde empieza y termina. Nadie debería transcribir eso a mano, así que el engine renderiza el componente por ti:

```bash
mage-obsidian:island-ssr --component path/to/BuyBox.vue --state ./state.mjs
```

- `--state` es un `.mjs` (o `.json`) con los valores que lee la plantilla. Un `.mjs` puede llevar los métodos que la plantilla invoca y un mapa `components` para componentes hijos; ejecútalo desde el harness de Vite para que sus imports resuelvan.
- `--props` pasa las props de la isla como JSON.

Solo se usa el `<template>` del componente —su `<script setup>` nunca se ejecuta—, así que no hace falta bundler ni navegador. Nada de esto llega a una tienda.

### Los anclajes

Pega el markup generado, reemplaza los valores por variables de plantilla y expresa los anclajes con los helpers en lugar de escribir comentarios HTML a mano:

{% raw %}
```twig
{% apply island_list %}
    {% for option in group.options %}<button …>{{ option.label }}</button>{% endfor %}
{% endapply %}

{% apply island_if(oldPrice) %}<span class="regular">{{ oldPrice }}</span>{% endapply %}
```
{% endraw %}

| Helper | Refleja | Emite |
|---|---|---|
| `island_list` | `v-for` | `<!--[-->` … `<!--]-->` |
| `island_if(cond)` | `v-if` sin `v-else` | el markup, o `<!---->` |

Un `v-if`/`v-else` no necesita helper: Vue renderiza la rama tomada sin ningún anclaje, así que un {% raw %}`{% if %}`{% endraw %} normal coincide. En `.phtml`, los equivalentes son `$block->islandList()` y `$block->islandIf()`.

De la indentación se encarga el framework: `renderVueComponent` elimina el whitespace entre etiquetas, que el compilador de Vue no espera y que de otro modo haría fallar la hidratación en todas las islas.

---

## Cómo Funciona

### 1. El marcador (lado servidor)

```html
<div data-mage-island
     data-component="/static/.../generated/Vendor_Module/components/NavBar.js"
     data-props="{&quot;title&quot;:&quot;Welcome&quot;}"
     data-strategy="visible"
     data-hydrate>…markup del servidor…</div>
```

| Atributo | Significado |
|---|---|
| `data-mage-island` | Marca el elemento para que el bootstrap pueda descubrirlo. |
| `data-component` | URL del módulo compilado del componente a importar. |
| `data-props` | JSON seguro para atributos con las props. El navegador decodifica las entidades antes de `JSON.parse`. |
| `data-strategy` | `visible` (lazy) o `eager`. |
| `data-hydrate` | Presente cuando el contenido es el estado inicial del componente, no un placeholder. |

Las props las codifica el servicio `PropsEncoder`: hace `json_encode` y escapa como entidades `<`, `>`, `&`, `"` y `'` para que el valor no pueda salirse del atributo. Un valor no codificable (UTF-8 mal formado, un recurso, `NAN`/`INF`) lanza una excepción en lugar de emitir un marcador roto.

### 2. El bootstrap de página (lado navegador)

Un único script de módulo se inyecta una vez por página, justo antes de `</body>`, mediante el bloque `IslandsRuntime`. Al cargar:

1. Consulta el documento por `[data-mage-island]`. **Si no hay ninguno, se detiene ahí** — Vue nunca se importa.
2. Si los hay, importa de forma diferida el runtime de Vue y el plugin de i18n (una sola vez).
3. Entrega los marcadores al runtime de hidratación del framework, aportando el comportamiento concreto del navegador: import dinámico del componente, creación de la app, cableado de i18n y un `IntersectionObserver` para la estrategia `visible`.

Las apps se crean con `createSSRApp`, así que un marcador con `data-hydrate` se adopta y uno sin él se limpia y se monta. Vue elige el camino a partir del propio contenedor, por eso nada de esto necesita un flag.

### 3. Estrategias de hidratación

La estrategia viene del argumento `$eager`:

- **`visible` (por defecto)** — el marcador se registra en un `IntersectionObserver`; el módulo se descarga y la isla se monta la primera vez que entra en el viewport.
- **`eager`** — la isla se monta de inmediato al cargar la página. Úsala para componentes por encima del pliegue, y dales markup del servidor para hidratar.

La hidratación es **idempotente**: el primer montaje reclama el elemento, así que una segunda llamada del observer para el mismo marcador no hace nada.

---

## Cómo Verificarlo

### El detector de drift

El markup del servidor reformula lo que renderiza el `<template>` del componente, y nada impide que los dos diverjan — peor: una clase que sólo existe del lado cliente Vue la reporta y luego la descarta, así que falla de forma invisible. Para eso está el chequeo en runtime.

Una hidratación que coincidió no toca el DOM: Vue compara `class` como conjunto y `style` como mapa, y una diferencia ahí sólo se loguea. Todo lo que no puede adoptar pasa por `handleMismatch`, que remueve el nodo del servidor y parchea el correcto. Entonces que el markup haya cambiado **es** el mismatch, exactamente, sin fixtures que mantener. En una build de desarrollo el bootstrap fotografía cada objetivo de hidratación, monta, compara y reporta el primer byte que difiere:

```
[MageObsidian] Island "MageObsidian_Catalog::catalog/ProductForm" hydrated with a mismatch — Vue replaced the server markup.
server: <button class="pdp__swatch pdp__swatch--text">
client: <button class="pdp__swatch">
                       ^ first difference at offset 412
```

Un subárbol marcado con el `data-allow-mismatch` de Vue se recorta de ambos lados, así que un valor que el servidor no puede predecir queda exceptuado en vez de reportado en cada carga.

La misma pasada reporta una **isla eager que cambió de tamaño al montar**, que es el salto que todo este mecanismo existe para evitar. El tamaño es la prueba honesta: un contenedor vacío que no ocupa espacio —un drawer, un host de toasts— no mueve nada y no es un defecto.

Ambos son sólo de desarrollo. Están condicionados a `__MAGE_OBSIDIAN_DEV__`, que la config de Vite define a partir de `NODE_ENV` — **no** a `import.meta.env.DEV`, que es falso en cualquier `vite build` porque Vite siempre construye en modo producción.

### Desde la línea de comandos

**`bin/magento mage-obsidian:frontend:doctor`** reporta las islas eager que todavía reemplazan su contenedor, tanto en plantillas de módulos como en overrides del tema.

### No uses CLS como criterio

Un buy box que aparece 200 ms después de que la página pinta puede puntuar 0.02 —cómodamente "bueno"— mientras muestra una página visiblemente rota, porque la métrica pesa la fracción del viewport que se movió. Mide lo que importa: si alguna isla cambia de tamaño después del primer pintado.

---

## Lógica Compartida en el Engine

La lógica de descubrimiento/hidratación vive en el engine de build JS (`mage-obsidian/runtime/islands.ts`) y está completamente inyectada por dependencias —sin referencias directas al DOM, a un bundler ni a Vue—, así que se testea unitariamente en Node. El cableado concreto (el `import` dinámico real, `createSSRApp`, `app.use(i18n)` y el observer) vive en el `web/js/islands.ts` del módulo.

---

## Notas Clave

- Una página sin islas no carga Vue — tenlo en cuenta al decidir entre una isla y el [patrón Vue inline](0100-phtml-vue-integration.md).
- Usa `visible` por defecto; reserva `eager` para componentes por encima del pliegue, e hidrátalos.
- Las props deben ser codificables como JSON. Pasa datos planos (escalares, arrays, mapas), no objetos con recursos o cadenas no UTF-8.
- El diccionario de i18n es el `js-translation.json` nativo por locale de Magento, así que las islas comparten las mismas traducciones que el resto de la tienda.
- Un valor que el servidor no puede predecir (un id generado, un número formateado por locale) se puede exceptuar con `data-allow-mismatch` de Vue en lugar de perseguirlo.
- **Los iconos deben salir de la misma fuente en ambos lados.** `hero_icon()` emite `<svg><use href>`; un componente que importa `@heroicons/vue` emite un `<path>` en línea. Nunca pueden coincidir, así que un componente que hidrata usa el componente `Icon` del engine, que emite el mismo `<use>`. Pasa también las clases al cuarto argumento de `hero_icon` — una clase que sólo el cliente pondría se reporta y se descarta, así que nunca llegaría a aplicarse.

---

## Próximos Pasos

- Una isla también se puede colocar desde contenido CMS — por un merchant con un widget, o a mano con la directiva `{% raw %}{{island}}{% endraw %}`. Consulta [Contenido CMS](0157-cms.es.md).
- Consulta [Uso de JavaScript y Componentes Vue en Plantillas `.phtml`](0090-phtml-configuration.md) para la referencia completa de `renderVueComponent`.
- La misma isla se puede montar desde una plantilla `.twig` mediante el helper `render_vue` — consulta el [Motor Twig](../../twig/index.md).
