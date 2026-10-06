# Interceptores JS

Los interceptores permiten que un módulo cambie el comportamiento de las funciones JavaScript de otro módulo sin editar su código fuente. Son el equivalente JavaScript de los plugins PHP de Magento: los mismos hooks `before`, `around` y `after`, ordenados por `sortOrder`.

El build sustituye el módulo objetivo por un envoltorio generado, de modo que todo el que importe el objetivo recibe la versión interceptada. El archivo objetivo en disco nunca se modifica.

## Declarar un interceptor

Una declaración tiene dos partes: una **entrada de configuración** que indica qué interceptar y un **módulo interceptor** que contiene los hooks.

### La entrada de configuración

Se declara bajo la clave `interceptors` del `module.config.ts` del módulo que incluye el interceptor (`view/frontend/web/module.config.ts`). La clave es el nombre del interceptor:

```javascript
export default {
    interceptors: {
        PromoPriceInterceptor: {
            name: "PromoPriceInterceptor",
            target: "Vendor_Catalog::js/price.js",
            interceptor: "Vendor_Promo::js/interceptors/price.js",
            sortOrder: 20,
        },
    },
};
```

| Campo | Significado |
|---|---|
| `name` | Identificador único del interceptor. Es el nombre que aparece en advertencias y errores. |
| `target` | El módulo a interceptar, como `Vendor_Module::path`. Obligatorio: una entrada sin él se ignora. |
| `interceptor` | El módulo que exporta los hooks, como `Vendor_Module::path`. |
| `sortOrder` | Orden de ejecución, de menor a mayor. Por defecto `10`. |
| `active` | Ponlo en `false` para desactivar el interceptor. |

Ambas rutas usan la forma `Vendor_Module::path`, así que la herencia de temas aplica: si un tema sobrescribe el archivo objetivo o el del interceptor, el build usa la sobrescritura.

Si dos archivos `module.config.ts` declaran el mismo nombre de interceptor, sus entradas se fusionan y la posterior gana campo a campo. Así un módulo o un tema cambia el `sortOrder` de un interceptor ajeno, o lo desactiva (`active: false`).

### El módulo interceptor

El módulo interceptor exporta una función por hook. El nombre de la exportación es el tipo de hook seguido del nombre de la exportación del objetivo, con su primera letra en mayúscula:

| Exportación | Intercepta | Firma |
|---|---|---|
| `beforeFormatPrice` | `formatPrice` | `(subject, ...args)` |
| `aroundFormatPrice` | `formatPrice` | `(subject, proceed, ...args)` |
| `afterFormatPrice` | `formatPrice` | `(subject, result, ...args)` |

`subject` son las exportaciones del módulo objetivo. `this` apunta al mismo objeto, pero las funciones flecha no ven `this`, así que prefiere `subject`.

- **`before`** puede devolver un arreglo para reemplazar los argumentos que reciben los siguientes hooks y la función original. El arreglo contiene solo los argumentos, sin `subject`. Cualquier otro valor de retorno deja los argumentos intactos.
- **`around`** decide si la función original se ejecuta y cómo: llama a `proceed(...args)` para continuar la cadena, o devuelve un valor sin llamarla para cortocircuitar.
- **`after`** recibe el resultado y debe devolver el resultado que se pasa adelante, aunque no lo haya cambiado.

Para interceptar la exportación por defecto del objetivo, nombra el hook `beforeDefault`, `aroundDefault` o `afterDefault`.

Los hooks se ejecutan en este orden: todos los `before`, luego los `around` envolviendo la función original y por último todos los `after`. Dentro de cada tipo, el `sortOrder` más bajo va primero. En `around`, eso significa que el `sortOrder` más bajo es el envoltorio más externo.

## Un ejemplo completo

`Vendor_Promo` ajusta cómo `Vendor_Catalog` formatea los precios.

El objetivo, en `Vendor_Catalog`:

```javascript
export function formatPrice(amount, currency) {
    return `${currency} ${amount.toFixed(2)}`;
}
```

El interceptor, en `Vendor_Promo`, en `view/frontend/web/js/interceptors/price.js`:

```javascript
export function beforeFormatPrice(subject, amount, currency) {
    return [Math.round(amount * 100) / 100, currency];
}

export async function aroundFormatPrice(subject, proceed, amount, currency) {
    if (amount === 0) {
        return "Free";
    }
    return proceed(amount, currency);
}

export function afterFormatPrice(subject, result, amount, currency) {
    return amount > 100 ? `${result} *` : result;
}
```

Y la entrada de configuración mostrada arriba, en el `module.config.ts` de `Vendor_Promo`.

Con esto en su lugar, quien llame a `formatPrice` obtiene:

| Llamada | Resultado |
|---|---|
| `formatPrice(10.005, "USD")` | `"USD 10.01"` |
| `formatPrice(0, "USD")` | `"Free"` |
| `formatPrice(250, "USD")` | `"USD 250.00 *"` |

Este ejemplo se ejecutó contra el arnés de pruebas del propio motor (`generateInterceptors` y el gestor de interceptores, con la misma disposición de módulos) y produjo los tres resultados anteriores.

## Verificarlo en el build

El plugin de Vite `mage-obsidian:interceptors` genera los interceptores cuando arranca el build. Reemplaza cada importación de un objetivo interceptado por un **módulo virtual** cuyo id es `\0interceptor:<ruta absoluta del objetivo>`. El módulo generado importa el archivo original con la query `?originalIntercepted`, importa tus módulos interceptores, registra cada hook y reexporta todas las exportaciones del objetivo a través de un proxy.

Qué revisar cuando un interceptor no parece aplicarse:

- Reinicia el build o el servidor de desarrollo tras cambiar una declaración: los interceptores se generan una vez por tema, al iniciar el build.
- Lee la salida del build. El motor imprime `Target module not found for identifier: …` o `Interceptor module not found: …` cuando un `Vendor_Module::path` no se resuelve, y `Failed to import target module …` o `Failed to import interceptor module …` cuando Node no puede cargar el archivo.
- Un hook cuyo nombre no coincide con ninguna exportación del objetivo detiene la generación con `Interceptor <name> (…) exports '<hook>' but target … does not export '<method>'`. El plugin lo reporta como `[mage-obsidian:interceptors] Failed to generate interceptors` y el build continúa **sin ningún interceptor** para ese tema, así que trata esa línea como un fallo.
- `[mage-obsidian:interceptors] themeName option is missing` indica que el plugin se configuró sin tema y no se genera ningún interceptor.

## Límites

- **Toda función exportada por un objetivo interceptado pasa a ser asíncrona, incluso las que ningún hook toca.** El envoltorio generado ejecuta la cadena con `await`, así que la llamada devuelve una `Promise` aunque la original sea síncrona. Quien la llame debe usar `await`.
- **Un objetivo que exporta una clase o un constructor no se puede interceptar.** El proxy lo reemplaza por una función, así que `new` falla. Mueve la función que quieres interceptar a su propio módulo.
- **Solo se pueden interceptar funciones exportadas.** Si la exportación del objetivo no es una función, el motor avisa y omite ese hook. Las demás exportaciones pasan sin tocar.
- **Todo lo que empiece por `before`, `around` o `after` se lee como un hook.** No exportes funciones auxiliares desde un módulo interceptor con esos prefijos. Las demás exportaciones se ignoran.
- **El objetivo y el módulo interceptor solo pueden usar imports que Node resuelva por sí mismo.** El motor importa ambos durante el build para leer sus exportaciones. Un módulo que importe `Vendor_Module::path`, un componente `.vue` o un paquete que no se encuentra desde su carpeta se omite, y solo se registra una línea en la consola. El código de nivel superior que necesite el navegador (`window`, `document`) también puede hacer fallar la importación.
- **Las exportaciones se leen una sola vez.** El envoltorio cubre las exportaciones que el objetivo tiene al iniciar el build; la interceptación no sigue a funciones que el objetivo añada o reemplace en tiempo de ejecución.
- **Los hooks son por función, no por punto de llamada.** Todo el que importe el objetivo se ve afectado, sin forma de excluir a un solo llamador.
