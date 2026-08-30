# UI Optimista y Movimiento

Un storefront se siente lento mucho antes de *serlo*. Hacer clic en `+` sobre una fila del carrito y ver el número quieto durante 400 ms mientras viaja un request es la diferencia entre una interfaz que responde y una que espera — y ningún ajuste del servidor elimina el viaje de ida y vuelta.

**{{ config.extra.components_name }}** lo resuelve al revés: aplica el cambio en pantalla de inmediato, envía el request y reconcilia cuando el servidor contesta. La capa de estado y el [bus de eventos](0155-storefront-events.md) ya aportan todo lo que hace falta — una copia local reactiva, un snapshot al que volver y una fase de la que colgar el spinner.

---

## El flag

```
Stores → Configuration → MageObsidian → Storefront → Optimistic UI
```

`mage_obsidian/storefront/optimistic_ui`, por defecto **Yes**, con alcance por website y por store view. Apagado, cantidad y eliminación esperan al servidor antes de tocar la pantalla — las animaciones siguen corriendo, sólo que cuando llega la respuesta.

El flag llega al navegador como `window.__MAGE_OBSIDIAN_UX__`, emitido en línea a través de `SecureHtmlRenderer` para que lleve el nonce de CSP, y se lee así:

```ts
import { readUxRuntimeConfig } from 'mage-obsidian/runtime/uxConfig.ts';

const ux = readUxRuntimeConfig(); // { optimistic, summaryCountsQty }
```

**Agregar al carrito es optimista sin importar el flag.** Que el badge suba es el acuse de recibo del clic, y no hay estado que corromper: el contador se proyecta hacia adelante y la recarga obligatoria de secciones lo reemplaza con el número del servidor un instante después.

---

## Cómo funciona la reconciliación

Tres piezas del section store, todas en `useCustomerData`:

| Miembro | Para qué |
|---|---|
| `patch(name, partial)` | mezcla una sección parcial en el mapa reactivo |
| `snapshot()` | el mapa actual, para poder volver |
| `restore(snapshot)` | lo devuelve |

`patch` es **sólo en memoria** — nunca escribe en `mage-cache-storage`. El `customer-data.js` de Magento sigue siendo el dueño de la caché canónica, así que una proyección que resulte equivocada muere con la página en vez de sobrevivirle en local storage.

De ahí salen dos flujos:

**Agregar** no necesita rollback. `post()` ya recarga las secciones `cart` y `messages` al terminar, y esa recarga *es* la reconciliación: sobrescribe la proyección con la verdad, haya funcionado el add o no.

```ts
customerData.patch('cart', {
    summary_count: count.value + (ux.summaryCountsQty ? qty : 1),
});
```

**Cantidad y eliminación** en el minicart toman un snapshot primero, proyectan, y lo devuelven si el servidor rechaza:

```ts
const rollback = customerData.snapshot();
if (ux.optimistic) {
    project();
}

const { ok, message } = await mutate();
if (!ok) {
    customerData.restore(rollback);
    notify(message ?? 'Could not update your bag', NotificationTone.Warning);
}
```

La fila eliminada vuelve a entrar por la misma transición por la que se fue, y la advertencia dice por qué.

### Contar unidades o líneas

Magento decide qué significa el badge del bag: `checkout/cart_link/use_qty` hace que `summary_count` sean **unidades**; apagado, cuenta **líneas**. La proyección tiene que coincidir, o agregar dos de algo mueve el badge en la cantidad equivocada y la recarga lo corrige a la vista.

Esa configuración viaja en el mismo global como `summaryCountsQty`, y por eso la proyección la lee en vez de suponerla.

---

## Estado de carga

Ningún componente es dueño de un flag de carga. Tanto el botón como el badge derivan el suyo del bus:

```ts
const activity = useActivity();
const syncing = computed(() => activity.isBusy('cart'));
```

**El badge del bag** gana un anillo fino girando alrededor del ícono y atenúa el número al 45% mientras haya algo de carrito en vuelo. Como el add es optimista, el número *ya* es el nuevo — el anillo dice "sincronizando", no "todavía no sé".

**El botón** conserva su etiqueta dentro de la caja y la esconde con `visibility`, y centra el spinner por encima en absoluto:

```html
<button :class="{ 'is-loading': adding }">
    <span class="obsidian-button__label">Add to cart</span>
    <span v-if="adding" class="obsidian-button__spinner"></span>
</button>
```

Cambiar la etiqueta por un spinner es la implementación obvia y la equivocada: el spinner es más bajo y más angosto que el texto, así que el botón encoge en el momento en que lo tocas y todo a su alrededor se mueve. Conservar la etiqueta reserva exactamente la caja que ya tenía. Nada salta, y no hay que adivinar ningún `min-width`.

El spinner mide `1em`, así que escala con el botón en el que caiga.

---

## Movimiento

### Eliminar una fila

La fila se desliza a la derecha desvaneciéndose mientras las de abajo suben suave para cerrar el hueco:

```css
.minicart-item-move,
.minicart-item-enter-active,
.minicart-item-leave-active {
    transition:
        transform 0.32s var(--ease-obsidian),
        opacity 0.24s var(--ease-obsidian);
}

.minicart-item-enter-from,
.minicart-item-leave-to {
    opacity: 0;
    transform: translateX(1.5rem);
}

.minicart-item-leave-active {
    position: absolute;
    left: 0;
    right: 0;
}
```

El `position: absolute` de la fila que sale es todo el truco. El `TransitionGroup` de Vue calcula los desplazamientos FLIP de `-move` a partir de dónde aterrizan los elementos restantes; mientras la fila que se va siga ocupando su espacio, no aterrizan en ningún lado. Sacarla del flujo les permite subir de inmediato, y la transición anima la diferencia.

Sólo se animan `transform` y `opacity` — ambas compuestas, ninguna dispara layout. Colapsar la fila animando `height` haría lo mismo a la vista, al costo de un pase de layout por frame.

!!! warning "El contenedor con scroll necesita `overflow-x: hidden`"
    La fila que sale se traslada 24 px más allá del borde derecho de una lista que es `overflow-y: auto`. CSS resuelve el otro eje de un contenedor con scroll también como `auto`, así que al drawer le sale una barra horizontal durante toda la eliminación. Fijar `overflow-x: hidden` en la lista lo arregla.

### Cambiar la cantidad

Pasan tres cosas a la vez, y cada una dice algo distinto:

- **El número cambia de inmediato.** Los controles nunca se deshabilitan, así que clicar `+` tres veces seguidas funciona; los requests se encolan y gana el último.
- **El stepper da un salto** (`scale(1.08)`, 250 ms) — el acuse de recibo de que el clic entró.
- **El precio de línea se atenúa y pulsa** mientras su request está en vuelo, y **el subtotal destella** en `--color-accent-soft` cuando su valor cambia de verdad.

El destello es un composable, así que la página del bag y el checkout lo obtienen igual:

```ts
import { useValueFlash } from 'MageObsidian_Storefront::js/useValueFlash';

const subtotalFlashing = useValueFlash(() => subtotal.value);
```

El shimmer va **sólo sobre el precio**, no sobre la fila. Atenuar la fila entera para decir "un número se está actualizando" se lee como "este ítem está deshabilitado".

### La página del bag intercambia filas, no las re-renderiza

La página del bag se renderiza en el servidor, así que se re-solicita a sí misma y reemplaza la región del carrito entera. Cada fila lleva su propio `view-transition-name`, y la fila que se va se desvanece y desliza mientras las de abajo cierran el hueco — la misma idea que en el cajón, pero a través del navegador en vez de Vue.

Las animaciones tienen que acotarse a las filas que realmente entran o salen:

```css
::view-transition-old(.obsidian-cart-line):only-child { /* la fila que se fue */ }
::view-transition-new(.obsidian-cart-line):only-child { /* la fila que llegó */ }
```

`:only-child` es como un snapshot dice que no tiene contraparte — una fila que sólo sale no tiene `-new`, una que sólo llega no tiene `-old`. Una fila que *sobrevive* al intercambio tiene ambas, y debe quedarse en el cross-fade por defecto. Sin la guarda, un paso de cantidad desvanece la fila superviviente durante 140 ms mientras la reaparece desde los 60 ms: las dos curvas dejan la fila en torno al 40% de opacidad durante ~60 ms, y eso se lee como un parpadeo. Es la versión a nivel de fila del error que el flash evita — atenuar la fila entera para decir que cambió un número.

Reemplazar la región también destruye aquello que el visitante estaba operando, así que el enhancer registra el control enfocado antes del intercambio y lo restaura después. Sin eso, la segunda pulsación de `+` cae sobre nada.

### Vaciarse

Cuando sale la última fila, la lista hace cross-fade hacia el panel vacío en vez de colapsar a él — un `<Transition mode="out-in">` alrededor de los dos estados.

### Acciones destructivas

Los controles de eliminar usan `--color-danger` (`#a4322b`, un rojo mineral apagado que convive con la paleta OBSIDIAN), al 72% de opacidad, llegando a opacidad plena y `scale(1.1)` en hover. Es un token del tema, no una constante del minicart, así que cualquier acción destructiva del storefront usa el mismo rojo.

El ícono sale del sprite compartido a través del componente `Icon`, nunca SVG en línea — la misma fuente que usa `hero_icon()`, así que un componente que hidrata coincide con su marcado del servidor.

---

## Dónde aterriza el feedback

Una confirmación que tapa la navegación es peor que ninguna confirmación, así que el storefront toma dos decisiones separadas: **quién** anuncia un resultado y **dónde** se coloca ese anuncio.

### Agregar al bag abre el bag

Un alta correcta abre el cajón del minicart y reclama el aviso vía `result.announced` (ver [Eventos del Storefront](0155-storefront-events.md#reclamar-el-aviso)), así que no se emite ningún toast de éxito. El bag *es* la confirmación: la línea está ahí, el subtotal está ahí, y el checkout queda a un clic. La fila cuya cantidad creció se tiñe con `--color-accent-soft` durante 1.8s, siguiendo la cantidad y no la llegada de un id nuevo — volver a agregar algo que ya estaba en el bag hace crecer una línea en vez de crear una.

Un alta **rechazada** nunca se reclama. Sigue llegando a un toast, con el texto propio de Magento, y el cajón se queda cerrado.

El cajón también se aparta cuando la *página* del bag está en pantalla — se estaría tapando a sí mismo. Ahí tampoco reclama nadie el aviso, así que el alta llega a un toast. La detección usa el marcador raíz de esa página, no la URL, de modo que códigos de tienda y sufijos dan igual.

El cajón mueve el foco, así que un lector de pantalla escucha el diálogo. El alta en sí la anuncia por separado una live region que vive **fuera** del cajón y por lo tanto ya está en el DOM cuando llega el mensaje — una live region insertada ya rellena no se anuncia de forma confiable.

### La pila de toasts está anclada abajo

Los toasts van abajo: abajo a la derecha desde `sm`, centrados por debajo. La esquina superior derecha es donde viven los controles de cuenta, búsqueda y bag, y un toast que aterriza ahí tapa justamente el control del que habla — lo que además incumple el SC 2.4.11 *Focus Not Obscured* de WCAG 2.2, porque un usuario de teclado puede enfocar un control sobre el que el toast está pintado.

Todo lo que esté anclado al borde inferior hay que despejarlo, y cada contribuyente declara su propia custom property:

| Propiedad | La declara | Significa |
|---|---|---|
| `--obsidian-bottom-inset` | el dock móvil del checkout | mobiliario que toda capa flotante debe despejar |
| `--obsidian-cookie-notice-height` | el banner de consentimiento, medido en runtime | el alto del banner mientras está en pantalla |
| `--obsidian-toast-inset` | cualquier módulo con cromo propio en la esquina inferior | despeje extra que sólo necesita la pila de toasts |

`.toast-host` suma las tres a su propio padding, más `env(safe-area-inset-bottom)`. Un módulo que estacione algo en la esquina inferior declara `--obsidian-toast-inset` acotado a la página que realmente lo renderiza — `:root:has(.mi-widget)`, no un `:root` pelado — para que las páginas sin él no paguen el hueco.

Dentro de la pila, la región assertive se renderiza **última**, más cerca de la esquina anclada, porque ahí es donde cae la vista.

## Movimiento reducido

Cada transición y animación de este documento se apaga bajo `prefers-reduced-motion: reduce`, incluidos los spinners:

```css
@media (prefers-reduced-motion: reduce) {
    .minicart-item-move,
    .minicart-item-enter-active,
    .minicart-item-leave-active,
    .minicart-value,
    .minicart-qty {
        transition: none;
    }

    .cart-count__ring,
    .obsidian-button__spinner {
        animation: none;
    }
}
```

El resultado sigue siendo plenamente funcional: las filas desaparecen, los números cambian, los estados se siguen leyendo — simplemente llegan al instante. La UI optimista es *por qué* eso funciona, porque sin la animación no queda nada que esperar.

---

## Notas Clave

- Los nombres de clase del movimiento se escriben como selectores CSS planos en `module.extend.css`, no como utilidades de Tailwind. Nada los referencia estáticamente, así que el tree-shaker los tiraría.
- Ese archivo vive en `view/frontend/web/css/`, no en `view/frontend/web/` — en cualquier otro lado el tema no lo construye.
- `patch` nunca persiste. La caché canónica de customer-data sigue siendo de Magento.
- Proyecta sólo lo que el servidor pueda confirmar. El minicart proyecta `items` y `summary_count`; no recalcula el subtotal, porque impuestos, descuentos y reglas de totales son una respuesta que da el servidor.
- Optimista no significa silencioso. Una mutación rechazada siempre se revierte *y* lo dice.

---

## Próximos Pasos

- [Eventos del Storefront](0155-storefront-events.md) — la convención de la que se deriva el estado de carga.
- [Gestión de Estado](0150-state-management.md) — `patch`, `snapshot` y `restore` en contexto.
- [Rendimiento](0160-performance.md) — el presupuesto dentro del que este movimiento tiene que vivir.
