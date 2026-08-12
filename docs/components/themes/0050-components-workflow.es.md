# Crear Scripts y Componentes

En **{{ config.extra.components_name }}**, los temas llevan su propio JavaScript y sus componentes Vue, bajo el directorio del tema:

```
app/design/frontend/Vendor/Theme/web/js          # scripts sueltos (.ts / .js)
app/design/frontend/Vendor/Theme/web/components  # componentes Vue de un solo archivo
```

Los archivos de un módulo van en `view/frontend/web/`. Todo lo de abajo funciona igual en ambos casos — lo único que cambia es el espacio de nombres con el que los referencias: `Theme::` para los archivos propios del tema, `Vendor_Module::` para los de un módulo.

---

## Flujo de trabajo

### 1. Scripts en `web/js`

Un script es un módulo, no una entrada de bundle. Se carga una vez, hace su trabajo y exporta lo que el resto necesite.

```ts
// app/design/frontend/Vendor/Theme/web/js/greeting.ts
export function greetUser(name: string): void {
    console.log(`¡Hola, ${name}!`);
}
```

Cárgalo desde una plantilla con el helper `script()`, que emite un `<script type="module">` apuntando al archivo construido:

{% raw %}
```twig
{{ script('Theme::js/greeting') }}
```
{% endraw %}

Impórtalo desde otro JS con el especificador del framework — **nunca con una ruta relativa**:

```ts
import { greetUser } from "Theme::js/greeting";
```

El especificador es lo que hace funcionar la herencia de temas: un tema hijo que traiga `web/js/greeting.ts` reemplaza de forma transparente el del padre para todo el que lo importe. Una ruta relativa resuelve a un archivo concreto del disco y se salta esa herencia por completo. Un typo rompe el build con sugerencias en vez de llegar a producción.

### 2. Componentes Vue en `web/components`

Los componentes son archivos únicos con **`<script setup>`**. TypeScript es el default (`lang="ts"`).

{% raw %}
```vue
<!-- app/design/frontend/Vendor/Theme/web/components/CartSummary.vue -->
<script setup lang="ts">
import { computed } from "vue";

interface Item {
    price: number;
}

const props = defineProps<{ items: Item[] }>();

const total = computed(() => props.items.reduce((sum, item) => sum + item.price, 0));
</script>

<template>
    <div>
        <h2>Total: {{ total }}</h2>
    </div>
</template>
```
{% endraw %}

Móntalo desde una plantilla como **isla** — un marcador que el runtime hidrata, no una app que abarque toda la página:

{% raw %}
```twig
{{ render_vue('Theme::components/CartSummary', { items: items }) }}
```
{% endraw %}

`render_vue(name, props, eager, serverHtml, hydrate)`:

| Argumento | Significado |
|---|---|
| `name` | `Theme::components/X` o `Vendor_Module::components/X` |
| `props` | Se pasan al componente como sus props |
| `eager` | `true` monta de inmediato; por defecto espera a que la isla entre en pantalla |
| `serverHtml` | Markup del estado inicial del componente, para que la isla muestre algo antes de que llegue Vue |
| `hydrate` | Junto con `serverHtml`, adopta ese markup en vez de reemplazarlo — sin salto de layout |

Genera el `serverHtml` con el bin `mage-obsidian:island-ssr` (ver [Islas Vue](../modules/0105-vue-islands.es.md)). Una isla eager que reemplaza su contenedor mueve la página al montarse; `bin/magento mage-obsidian:frontend:doctor` reporta todas las que lo hacen.

---

## Plantillas: Twig o phtml

Con el módulo opcional de Twig instalado, las plantillas son `.twig` y los helpers de arriba son funciones Twig. Están declaradas `is_safe => html`, así que **nunca necesitan `|raw`**.

Sin él, las mismas capacidades son llamadas al ViewModel desde `.phtml`:

```php
<?= $block->renderVueComponent('Theme::components/CartSummary', ['items' => $items]) ?>
<script type="module" src="<?= $escaper->escapeUrl($block->getViteFileUrl('Theme::js/greeting')) ?>"></script>
```

Se espera que los temas nuevos se escriban en Twig; `.phtml` sigue soportado por compatibilidad y para el bloque puntual cuyo PHP el tema necesita conservar.

---

## Recomendaciones

1. **Ubicación.** Scripts en `web/js`, componentes en `web/components`. En un módulo, esos mismos dos directorios dentro de `view/frontend/web/`.
2. **Nombres.** kebab-case para `web/js`, PascalCase para los componentes.
3. **Imports.** Siempre `Theme::` / `Vendor_Module::`. Una ruta relativa que cruce el límite de un módulo o un tema rompe la herencia.
4. **Solo Composition API.** `<script setup>`; la Options API no se usa en ninguna parte del storefront que se distribuye.
5. **Los imports dinámicos** funcionan con los mismos especificadores, y son la forma de mantener el código de una isla fuera de la ruta crítica:
   ```ts
   const { greetUser } = await import("Theme::js/greeting");
   ```
6. **Vite procesa ambos directorios** — empaquetado, tree-shaking y huella digital en `web/generated`.

---

## Añadir algo a una página existente

Un componente que tiene que aparecer dentro de un bloque ajeno no obliga a editar ese bloque. Declara un bloque hijo en el layout XML y se renderiza donde la plantilla padre llama a `child_html`:

```xml
<referenceBlock name="product.info.main">
    <block class="MageObsidian\ModernFrontend\Block\Template"
           name="vendor.cart.summary" as="cart_summary"
           template="Vendor_Module::cart/summary.twig"/>
</referenceBlock>
```

Si la plantilla padre no tiene un hook para eso, un **interceptor** puede envolver el JS en su lugar, sin editar el módulo que lo posee.
