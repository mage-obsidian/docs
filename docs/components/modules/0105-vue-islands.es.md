# Islas Vue

En **{{ config.extra.components_name }}**, cada componente Vue renderizado desde una plantilla `.phtml` (o `.twig`) se monta como una **isla**: una app Vue autocontenida adosada a un único marcador en la página, hidratada de forma independiente del resto del documento.

El método puente de `.phtml` [`renderVueComponent`](0090-phtml-configuration.md#2-renderizacion-de-componentes-vue) ya no emite un script de montaje en línea. Emite un marcador inerte que un único bootstrap a nivel de página descubre y monta —por defecto solo cuando el marcador entra en el viewport.

---

## Por Qué Islas

- **Un bootstrap por página, no uno por componente.** El runtime de Vue y el plugin de i18n se importan **una sola vez** y los comparten todas las islas, en lugar de que cada llamada a `renderVueComponent` los reimporte.
- **Coste cero cuando no hay islas.** El bootstrap revisa primero si la página tiene marcadores; si no hay ninguno, retorna antes de importar Vue o el diccionario. Una página sin islas no envía Vue en absoluto.
- **Perezosa por defecto.** Los componentes por debajo del pliegue no se hidratan —ni siquiera se descarga su módulo— hasta que entran en el viewport.
- **Se preserva el aislamiento.** Cada isla sigue siendo su propia app Vue, así que un componente que falla o se vuelve a renderizar nunca afecta a otro.

---

## Cómo Funciona

### 1. El marcador (lado servidor)

`renderVueComponent` emite un único `<div>` que lleva todo lo que el navegador necesita en atributos de datos:

```html
<div data-mage-island
     data-component="/static/.../generated/Vendor_Module/components/NavBar.js"
     data-props="{&quot;title&quot;:&quot;Bienvenido&quot;}"
     data-strategy="visible"></div>
```

| Atributo | Significado |
|---|---|
| `data-mage-island` | Marca el elemento para que el bootstrap pueda descubrirlo. |
| `data-component` | URL del módulo del componente compilado que se importará. |
| `data-props` | JSON seguro para atributo de las props. El navegador decodifica las entidades de vuelta a JSON antes de `JSON.parse`. |
| `data-strategy` | `visible` (perezosa) o `eager`. |

Las props las codifica para el atributo el servicio `PropsEncoder`: hace `json_encode` de las props y escapa como entidades `<`, `>`, `&`, `"` y `'` para que el valor no pueda salirse del atributo. Un valor no codificable (UTF-8 mal formado, un recurso, `NAN`/`INF`) lanza una excepción en lugar de emitir un marcador roto.

### 2. El bootstrap de página (lado navegador)

Un único script de módulo se inyecta una vez por página, justo antes de `</body>`, mediante el bloque `IslandsRuntime` (cableado en el layout `default.xml` del módulo). Al cargar:

1. Consulta el documento por `[data-mage-island]`. **Si no hay ninguno, se detiene aquí** — Vue nunca se importa.
2. En caso contrario, importa de forma perezosa el runtime de Vue y el plugin de i18n (una sola vez).
3. Entrega los marcadores al runtime de hidratación del framework, proporcionando el comportamiento concreto del navegador: import dinámico del componente, creación de la app, cableado de i18n y un `IntersectionObserver` para la estrategia `visible`.

### 3. Estrategias de hidratación

La estrategia viene directamente del argumento `$eager` de `renderVueComponent`:

- **`visible` (por defecto)** — el marcador se registra en un `IntersectionObserver`; el módulo del componente se descarga y la isla se monta la primera vez que entra en el viewport. Ideal para contenido por debajo del pliegue.
- **`eager`** — la isla se monta de inmediato al cargar la página, sin esperar al viewport. Úsala para componentes por encima del pliegue donde cualquier retraso sería visible.

```php
<?= $block->renderVueComponent('Vendor_Module::Hero', $props, true) ?>  // eager
<?= $block->renderVueComponent('Vendor_Module::Reviews', $props) ?>     // visible (por defecto)
```

La hidratación es **idempotente**: el primer montaje reclama el elemento, así que una segunda llamada del observer para el mismo marcador no hace nada y nunca monta dos veces.

---

## Lógica Compartida en el Engine

La lógica de descubrimiento/hidratación vive en el engine de build de JS (`mage-obsidian/runtime/islands.ts`) y está totalmente inyectada por dependencias —sin referencia directa al DOM, a un bundler ni a Vue— por lo que se prueba con tests unitarios en Node. El cableado concreto (el `import` dinámico real, `createApp`, `app.use(i18n)` y el observer) vive en el `web/js/islands.js` del módulo. Normalmente no tocas ninguno de los dos: llamas a `renderVueComponent` y la maquinaria de islas hace el resto.

---

## Notas Clave

- Una página sin islas no carga Vue —ten presente esa propiedad al decidir entre una isla y el [patrón de Vue en línea](0100-phtml-vue-integration.md).
- Usa `visible` por defecto; reserva `eager` para componentes por encima del pliegue.
- Las props deben ser codificables a JSON. Pasa datos planos (escalares, arrays, mapas), no objetos con recursos o cadenas no UTF-8.
- El diccionario de i18n es el `js-translation.json` nativo de Magento por locale, así que las islas comparten las mismas traducciones que el resto de la tienda.

---

## Próximos Pasos

- Consulta [Uso de Archivos JavaScript y Componentes Vue en Plantillas `.phtml`](0090-phtml-configuration.md) para la referencia completa de `renderVueComponent`.
- La misma isla puede montarse desde una plantilla `.twig` mediante el helper `render_vue` — consulta el [Motor Twig](../../twig/index.md).
