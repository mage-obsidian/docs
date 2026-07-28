# Eventos del Storefront

**{{ config.extra.components_name }}** porta al navegador los dos puntos de extensión de Magento. Responden preguntas distintas, y la diferencia es la misma que en PHP:

| | Envuelve | Puede cambiar lo que pasa | Se cablea |
|---|---|---|---|
| **Interceptores** | una función concreta | sí | en build, por módulo |
| **Eventos** | nada — algo ya ocurrió | sólo a través de los datos que lleva | en runtime, por cualquiera |

Extender un flujo desde otro módulo no debería exigir saber qué función envolver. Así que el flujo anuncia lo que hizo, y cualquiera escucha.

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

Los observers corren en `sortOrder` (por defecto `10`, menor primero) y se esperan, así que uno asíncrono termina antes de que corra el siguiente. `observe` devuelve una función que lo quita.

Un observer que lanza se reporta y se salta — un hook de analítica que falla nunca debe tumbar un add-to-cart.

```js
events.observe('cart_add_before', (data) => { … }, { name: 'my_module', sortOrder: 5 });
```

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

---

## El flujo de carrito

Todas las mutaciones de carrito pasan por una única función, así que los eventos se anuncian ahí y no en cada llamador — `addFromForm`, `addProduct`, `addRaw`, `updateItemQty` y `removeItem` los emiten todos.

| Evento | Cuándo |
|---|---|
| `cart_add_before` | tras rellenar el form key, antes de enviar nada |
| `cart_add_after` | tras la respuesta y la recarga de las secciones `cart`/`messages` |
| `cart_add_failed` | además, cuando la mutación no tuvo éxito |

`update_qty` y `remove_item` tienen los mismos tres.

El payload:

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

Un observer de `_before` puede reescribir `action` o `body` — el request es lo que él deje:

```js
events.observe('cart_add_before', (data) => {
    data.body.set('qty', String(Number(data.body.get('qty')) * 2));
});
```

…o cortarlo del todo, en cuyo caso no se envía nada y no le sigue ningún `_after` ni `_failed`:

```js
events.observe('cart_add_before', (data) => {
    if (isRestricted(data.body.get('product'))) {
        data.cancelled = true;
        data.message = 'No disponible en tu región';
    }
});
```

El llamador recibe `{ ok: false, message }`, así que el toast dice qué pasó.

---

## Notas Clave

- El manager se publica como `window.__MAGE_OBSIDIAN_EVENTS__`, que es lo que usan el puente de `CustomEvent` y el código fuera del bundle. Dentro del bundle, impórtalo.
- Los nombres de evento van en `snake_case`, siguiendo la convención de Magento.
- La lógica de despacho vive en el engine (`mage-obsidian/runtime/eventManager.ts`) sin dependencias del DOM ni de un framework, así que se testea en Node; el singleton y el puente de `CustomEvent` son el `web/js/events.ts` del módulo.

---

## Próximos Pasos

- [Islas Vue](0105-vue-islands.md) — cómo se montan los componentes que despachan estos eventos.
- [Gestión de Estado](0150-state-management.md) — el estado reactivo del carrito con el que estos eventos conviven.
