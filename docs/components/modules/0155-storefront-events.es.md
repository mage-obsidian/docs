# Eventos del Storefront

**{{ config.extra.components_name }}** porta al navegador los dos puntos de extensión de Magento. Responden preguntas distintas, y la diferencia es la misma que en PHP:

| | Envuelve | Puede cambiar lo que pasa | Se cablea |
|---|---|---|---|
| **Interceptores** | una función concreta | sí | en build, por módulo |
| **Eventos** | nada — algo ya ocurrió | sólo a través de los datos que lleva | en runtime, por cualquiera |

Extender un flujo desde otro módulo no debería exigir saber qué función envolver. Así que el flujo anuncia lo que hizo, y cualquiera escucha.

---

## La convención

Cada mutación del storefront se anuncia tres veces, bajo un nombre construido con tres partes:

```
<dominio>_<operación>_<fase>
```

En `snake_case`, como los eventos de Magento. Las fases:

| Fase | Significado | Payload |
|---|---|---|
| `_before` | está por pasar; un observer puede modificarlo o cancelarlo | `{ …, cancelled: boolean, message?: string }` |
| `_after` | pasó | `{ …, result }` |
| `_failed` | además, no salió bien | `{ …, result }` |

Una mutación fallida despacha **ambos**, `_after` y `_failed`: `_after` significa "el flujo terminó", no "el flujo funcionó". Un observer al que sólo le interesa el éxito mira `result`.

Esa convención no es cosmética: es el mecanismo del que [se derivan los estados de carga](#el-rastreador-de-actividad). Un flujo que la respeta obtiene spinners sincronizados en toda la página sin escribir una línea para ellos.

Construye los nombres con el helper, no a mano, para que un typo sea un error de compilación en vez de un evento que nadie recibe:

```ts
import { MutationPhase, mutationEvent } from 'mage-obsidian/runtime/mutationEvent.ts';

mutationEvent('cart', 'add', MutationPhase.Before); // 'cart_add_before'
```

---

## Observar

```js
import events from 'MageObsidian_ModernFrontend::js/events';

events.observe('cart_add_after', (data) => {
    if (data.result.ok) {
        analytics.track('add_to_cart', { product: data.body.get('product') });
    }
});
```

Los observers corren en `sortOrder` (por defecto `10`, menor primero) y se esperan, así que uno asíncrono termina antes de que corra el siguiente. `observe` devuelve una función que lo quita; `observeOnce` se quita solo tras la primera llamada.

Un observer que lanza se reporta y se salta — un hook de analítica que falla nunca debe tumbar un add-to-cart.

```js
events.observe('cart_add_before', (data) => { … }, { name: 'my_module', sortOrder: 5 });
```

### Modificar y cancelar

Un observer de `_before` recibe el request que está por salir, y el request es lo que él deje:

```js
events.observe('cart_add_before', (data) => {
    data.body.set('qty', String(Number(data.body.get('qty')) * 2));
});
```

Poner `cancelled` lo corta del todo. No se envía nada, y no le sigue ningún `_after` ni `_failed`:

```js
events.observe('cart_add_before', (data) => {
    if (isRestricted(data.body.get('product'))) {
        data.cancelled = true;
        data.message = 'No disponible en tu región';
    }
});
```

El llamador recibe `{ ok: false, message }`, así que el toast dice qué pasó.

### Eventos sticky

Un evento que ocurre una vez por página — `page_ready` sobre todo — se recuerda. Un observer registrado *después* de que se despachó se invoca de inmediato con el payload que se perdió:

```js
events.observe('page_ready', (data) => {
    console.log(`${data.islands} islas en ${data.url}`);
});
```

Eso es lo que hace viable un snippet diferido de tag manager: no controla si carga antes o después del bootstrap, y con eventos sticky no le hace falta. `events.sticky(nombre)` lee el payload recordado directamente.

Marca como sticky sólo eventos de una-vez-por-página. Un `cart_add_after` sticky dispararía en cada observer futuro con un add viejo.

---

## Desde fuera del bundle

Cada dispatch se refleja como un `CustomEvent` sobre `window`, llamado `obsidian:<evento>`, así que un tag manager o un snippet en línea no necesita importar nada:

```html
<script>
    window.addEventListener('obsidian:cart_add_after', (event) => {
        dataLayer.push({ event: 'add_to_cart', ok: event.detail.result.ok });
    });
</script>
```

Un listener del DOM **no puede modificar los datos**: corre después de los observers, sobre el resultado. Un módulo que quiera cambiar lo que pasa registra un observer de verdad.

El espejo se puede saltar por dispatch para eventos de alta frecuencia, donde asignar un `CustomEvent` por tecla no compra nada:

```ts
events.dispatch(SEARCH_QUERY_CHANGE_EVENT, { query }, { mirror: false });
```

El espejo del DOM tampoco es sticky: un listener de `window` registrado después de un dispatch sticky no lo recibe. El código fuera del bundle que necesite el replay lee `window.__MAGE_OBSIDIAN_EVENTS__.sticky('page_ready')`.

---

## Ciclo de vida del runtime

El runtime mismo anuncia lo que hace, así que perfilar o integrar algo de terceros no exige parchear internals.

| Evento | Payload | Cuándo |
|---|---|---|
| `island_mount_before` | `{ component, strategy, element }` | antes de importar el módulo de la isla |
| `island_mount_after` | `+ durationMs` | tras montarla |
| `island_mount_failed` | `+ error` | su import o su montaje lanzó |
| `page_ready` *(sticky)* | `{ url, islands }` | el bootstrap terminó de descubrir marcadores |
| `page_hidden` / `page_visible` | `{ url }` | `visibilitychange` — la señal para pausar polling y timers |
| `page_leave` | `{ url, persisted }` | `pagehide`; `persisted` significa que se fue al bfcache |
| `section_reload_before` | `{ names }` | antes de pegarle a `/customer/section/load/` |
| `section_reload_after` | `{ names, changed }` | tras el merge; `changed` es lo que realmente cambió |
| `section_reload_failed` | `{ names }` | el request falló; se conservan los datos previos |

`durationMs` es el perfilador de islas más barato que hay — sin flag de build, sin extensión:

```js
events.observe('island_mount_after', ({ component, durationMs }) => {
    if (durationMs > 50) console.warn(component, durationMs);
});
```

---

## El catálogo

Cada dominio embudea sus mutaciones en una sola función, así que los eventos se anuncian ahí y no en cada llamador.

### Carrito — `MageObsidian_Storefront::js/useCart`

| Operación | Eventos | Los emite |
|---|---|---|
| `add` | `cart_add_before` / `_after` / `_failed` | `addFromForm`, `addProduct`, `addRaw` |
| `update_qty` | `cart_update_qty_*` | `updateItemQty` |
| `remove_item` | `cart_remove_item_*` | `removeItem` |
| `coupon` | `cart_coupon_*` | el formulario de cupón de la página del bag |

```ts
interface CartEvent {
    operation: 'add' | 'update_qty' | 'remove_item';
    action: string;      // el endpoint al que está por postear
    body: FormData;      // el cuerpo del request, form key incluido
    cancelled: boolean;
    message?: string;
    result?: CartResult; // sólo en _after / _failed
}
```

`_after` dispara cuando aterrizaron la respuesta **y** la recarga de las secciones `cart`/`messages`, así que un observer que lea `section('cart')` ve el estado nuevo.

#### Reclamar el aviso

`CartResult` es el objeto que `addFromForm` / `addProduct` / `addRaw` devuelven a quien los llamó, y `_after` lleva **ese mismo objeto**, no una copia:

```ts
interface CartResult {
    ok: boolean;
    message?: string;    // el texto de Magento cuando explica un rechazo
    announced?: boolean; // lo pone un observer que ya avisó al cliente
}
```

Así, un observer de `_after` que muestre el resultado por su cuenta puede marcar `announced` y quien llamó se saltará su propio toast:

```ts
events.observe('cart_add_after', (data) => {
    if (!data.result.ok) {
        return;
    }
    openMyOwnConfirmation();
    data.result.announced = true;
});
```

Es el único campo que un observer de `_after` está pensado para escribir — todo lo demás en `result` es el veredicto del servidor. El minicart lo usa: un alta correcta abre el cajón del bag, así que un toast diciendo lo mismo sería ruido. Nadie reclama un **fallo**, de modo que un alta rechazada siempre llega a un toast.

Un observer que reclame sin mostrar nada deja el resultado en silencio. Si el tuyo puede fallar al renderizar, reclama después de haberlo hecho.

### Wishlist y comparar

`wishlist_add_*`, `wishlist_remove_*`, `compare_add_*`, `compare_remove_*` — la misma forma `MutationEvent`, con `result: boolean`.

### Búsqueda — `MageObsidian_Storefront::js/search-events`

| Evento | Payload |
|---|---|
| `search_query_change` | `{ query }` — en cada tecla, **sin espejo en el DOM** |
| `search_suggest_before` / `_after` / `_failed` | `{ query, url, cancelled, result?: Suggestion[] }` |

### Catálogo — `MageObsidian_Catalog::js/catalog-events`

Describen una selección que cambia, no un request, así que no tienen fases.

| Evento | Payload |
|---|---|
| `product_variant_change` | `{ productId }` — `null` cuando la selección está incompleta |
| `bundle_selection_change` | `{ selections }` |
| `product_gallery_change` | `{ reset?, large?, label?, tiles? }` |

### Checkout — `MageObsidian_Checkout::js/checkout-events`

| Evento | Payload |
|---|---|
| `checkout_step_change` | `{ from, to }` — sólo en un cambio real |
| `checkout_estimate_shipping_*` | `CheckoutEvent` |
| `checkout_save_shipping_*` | `CheckoutEvent` |
| `checkout_apply_coupon_*` / `checkout_remove_coupon_*` | `CheckoutEvent` |
| `checkout_place_order_*` | `CheckoutEvent` |

```ts
interface CheckoutEvent {
    operation: CheckoutOperation;
    payload?: Record<string, unknown>;
    cancelled: boolean;
    message?: string;
    result?: unknown;
}
```

### UI

| Evento | Payload | Notas |
|---|---|---|
| `notification_add` | `{ message, tone }` | `tone` es `success`, `error` o `warning`; el host de toasts lo observa |
| `navigation_start` | `{ from, to, kind, trigger }` | está arrancando una view transition entre documentos |

`navigation_start` se anuncia, no se negocia: el `pageswap` del navegador no puede esperar, así que ponerle `cancelled` no hace nada.

Dos nombres heredados de `CustomEvent` se siguen despachando junto a sus eventos del bus — `obsidian:toast` y `obsidian:variant-image` — para que los snippets escritos contra ellos sigan funcionando.

---

## El rastreador de actividad

Un estado de carga no debería ser un `ref` local del componente que lanzó la petición. El botón que envía y el badge que refleja el resultado son islas distintas que nunca se importan entre sí, y ambas necesitan saber lo mismo.

Se lo preguntan al bus. El rastreador se engancha a cada dispatch y lee la fase del nombre: un `_before` abre los scopes `cart` y `cart_add`, un `_after` o un `_failed` los cierra.

```vue
<script setup>
import { computed } from 'vue';
import { useActivity } from 'MageObsidian_ModernFrontend::js/activity';

const activity = useActivity();
const syncing = computed(() => activity.isBusy('cart'));
</script>
```

| Miembro | Para qué |
|---|---|
| `isBusy(scope)` | si hay algo pendiente en ese scope |
| `pending(scope)` | cuántos |
| `busy(scope)` | lo mismo como `ComputedRef`, para un template |

Los scopes anidan por convención. `cart` está ocupado ante cualquier mutación de carrito; `cart_remove_item` sólo ante eliminaciones — suficiente para girar el ícono del bag con todo mientras una fila concreta muestra su propio estado.

El contador es derivado, así que cubre los casos que un flag escrito a mano equivoca: un `_before` cancelado cierra su scope de inmediato (no va a llegar ningún `_after`), mutaciones concurrentes del mismo dominio anidan en vez de pisarse, y un scope abierto más de 15 segundos se libera con una advertencia en lugar de dejar un spinner girando para siempre.

**Un dominio nuevo hereda todo esto gratis.** Respeta la convención de nombres y los spinners funcionan, sin importar nada y sin registrar nada.

---

## Tipar tus propios eventos

El catálogo es una interfaz TypeScript que el engine declara vacía y que cada módulo extiende, así que `observe` y `dispatch` conocen cada evento de la página y su payload:

```ts
import {
    MutationPhase,
    mutationEvent,
    type MutationEvent,
    type MutationEventName,
} from 'mage-obsidian/runtime/mutationEvent.ts';

export const RETURNS_DOMAIN = 'returns';

export const ReturnsOperation = { Request: 'request' } as const;
export type ReturnsOperation = (typeof ReturnsOperation)[keyof typeof ReturnsOperation];

export type ReturnsEvent = MutationEvent<ReturnsOperation, boolean>;
export type ReturnsEventName = MutationEventName<typeof RETURNS_DOMAIN, ReturnsOperation>;

declare module 'mage-obsidian/runtime/eventManager.ts' {
    interface StorefrontEventMap extends Record<ReturnsEventName, ReturnsEvent> {}
}

export const returnsEvent = <Phase extends MutationPhase>(phase: Phase) =>
    mutationEvent(RETURNS_DOMAIN, ReturnsOperation.Request, phase);
```

Eso declara `returns_request_before`, `_after` y `_failed` de una vez, cada uno con su payload. Observar alguno con la forma equivocada ahora falla el chequeo de tipos, y el editor completa los nombres de evento.

Lo que activa la extensión es importar el módulo. Un módulo que sólo observa eventos de otro importa su archivo de eventos para tener los tipos.

Un evento cuyo nombre no esté en el mapa sigue funcionando: cae a `Record<string, unknown>`. Nada de lo existente se rompe; simplemente no recibe ayuda.

---

## Depurar y rendimiento

En un build de desarrollo el manager se traza solo. Cada dispatch se loguea con su payload, y un observer que tarde más de 16 ms — un frame perdido — se nombra:

```
[MageObsidian] Observer "gtm_add_to_cart" of "cart_add_after" took 41.3ms
and delayed the interaction that dispatched it.
```

`events.debug()` enciende esa misma traza en un build de producción desde la consola, y `events.observersOf('cart_add_before')` lista quién está registrado. Ambos están en `window.__MAGE_OBSIDIAN_EVENTS__`, así que la consola no necesita importar nada.

El costo de un evento que nadie observa es el bucle de hooks y el `CustomEvent` espejo. El espejo es lo que se apaga (`{ mirror: false }`) en cualquier cosa despachada por tecla o por frame.

Los observers se esperan en secuencia: uno lento retrasa el flujo que lo despachó, y en `cart_add_before` ese retraso va por delante del request. La analítica va en `_after`.

---

## Notas Clave

- El manager se publica como `window.__MAGE_OBSIDIAN_EVENTS__`, que es lo que usan el puente de `CustomEvent` y el código fuera del bundle. Dentro del bundle, impórtalo.
- Los nombres de evento van en `snake_case`, siguiendo la convención de Magento, y siempre `<dominio>_<operación>_<fase>` para una mutación.
- `_after` significa que el flujo terminó, no que funcionó. Mira `result`.
- La lógica de despacho, el rastreador de actividad y las definiciones de ciclo de vida viven en el engine (`mage-obsidian/runtime/`) sin dependencias del DOM ni de un framework, así que se testean en Node; los singletons, el envoltorio reactivo y el puente de `CustomEvent` son el `web/js/` del módulo.

---

## Próximos Pasos

- [UI Optimista y Movimiento](0158-optimistic-ui-motion.md) — qué hace el storefront con estos eventos en pantalla.
- [Islas Vue](0105-vue-islands.md) — cómo se montan los componentes que despachan estos eventos.
- [Gestión de Estado](0150-state-management.md) — el estado reactivo del carrito con el que estos eventos conviven.
