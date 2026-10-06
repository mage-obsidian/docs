# JS interceptors

Interceptors let one module change the behaviour of another module's JavaScript functions without editing its source. They are the JavaScript counterpart of Magento's PHP plugins: the same `before`, `around` and `after` hooks, ordered by `sortOrder`.

The build swaps the target module for a generated wrapper, so every importer of the target gets the intercepted version. The target file on disk is never modified.

## Declare an interceptor

A declaration has two parts: a **config entry** that says what to intercept, and an **interceptor module** that holds the hooks.

### The config entry

Declare it under the `interceptors` key of the `module.config.ts` of the module that ships the interceptor (`view/frontend/web/module.config.ts`). The key is the interceptor's name:

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

| Field | Meaning |
|---|---|
| `name` | Unique id of the interceptor. It is the name used in warnings and errors. |
| `target` | The module to intercept, as `Vendor_Module::path`. Required: an entry without it is ignored. |
| `interceptor` | The module that exports the hooks, as `Vendor_Module::path`. |
| `sortOrder` | Execution order, lowest first. Defaults to `10`. |
| `active` | Set it to `false` to switch the interceptor off. |

Both paths use the `Vendor_Module::path` form, so theme inheritance applies: if a theme overrides the target or the interceptor file, the override is the one the build uses.

If two `module.config.ts` files declare the same interceptor name, their entries are merged and the later one wins field by field. That is how a module or theme changes the `sortOrder` of, or deactivates (`active: false`), an interceptor it does not own.

### The interceptor module

The interceptor module exports one function per hook. The export name is the hook type followed by the name of the target's export, with its first letter in capitals:

| Export | Hooks into | Signature |
|---|---|---|
| `beforeFormatPrice` | `formatPrice` | `(subject, ...args)` |
| `aroundFormatPrice` | `formatPrice` | `(subject, proceed, ...args)` |
| `afterFormatPrice` | `formatPrice` | `(subject, result, ...args)` |

`subject` is the target module's exports. `this` is bound to the same object, but arrow functions cannot see `this`, so prefer `subject`.

- **`before`** may return an array to replace the arguments the next hooks and the original function receive. The array holds the arguments only, without `subject`. Any other return value leaves the arguments unchanged.
- **`around`** decides whether and how the original runs: call `proceed(...args)` to continue the chain, or return a value without calling it to short-circuit.
- **`after`** receives the result and must return the result to hand on, even if it did not change it.

To hook the target's default export, name the hook `beforeDefault`, `aroundDefault` or `afterDefault`.

Hooks run in this order: all `before` hooks, then the `around` hooks wrapped around the original function, then all `after` hooks. Within each type, the lowest `sortOrder` runs first. For `around`, that means the lowest `sortOrder` is the outermost wrapper.

## A complete example

`Vendor_Promo` adjusts how `Vendor_Catalog` formats prices.

The target, in `Vendor_Catalog`:

```javascript
export function formatPrice(amount, currency) {
    return `${currency} ${amount.toFixed(2)}`;
}
```

The interceptor, in `Vendor_Promo` at `view/frontend/web/js/interceptors/price.js`:

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

And the config entry shown above, in `Vendor_Promo`'s `module.config.ts`.

With it in place, callers of `formatPrice` get:

| Call | Result |
|---|---|
| `formatPrice(10.005, "USD")` | `"USD 10.01"` |
| `formatPrice(0, "USD")` | `"Free"` |
| `formatPrice(250, "USD")` | `"USD 250.00 *"` |

This example was run against the engine's own test harness (`generateInterceptors` and the interceptor manager, with the same module layout) and produced the three results above.

## Verify it in the build

The `mage-obsidian:interceptors` Vite plugin generates the interceptors when the build starts. It replaces every import of an intercepted target with a **virtual module** whose id is `\0interceptor:<absolute path of the target>`. The generated module imports the original file under the query `?originalIntercepted`, imports your interceptor modules, registers each hook and re-exports every export of the target through a proxy.

Things to check when an interceptor does not seem to apply:

- Restart the build or the dev server after you change a declaration: the interceptors are generated once per theme, at build start.
- Read the build output. The engine prints `Target module not found for identifier: …` or `Interceptor module not found: …` when a `Vendor_Module::path` does not resolve, and `Failed to import target module …` or `Failed to import interceptor module …` when Node cannot load the file.
- A hook whose name does not match an export of the target stops the generation with `Interceptor <name> (…) exports '<hook>' but target … does not export '<method>'`. The plugin reports that as `[mage-obsidian:interceptors] Failed to generate interceptors` and the build carries on **without any interceptor** for that theme, so treat that line as a failure.
- `[mage-obsidian:interceptors] themeName option is missing` means the plugin was configured without a theme, and no interceptor is generated.

## Limits

- **Every exported function of an intercepted target becomes asynchronous, including the ones no hook touches.** The generated wrapper runs the chain with `await`, so a call returns a `Promise` even if the original is synchronous. Callers must `await` it.
- **A target that exports a class or constructor cannot be intercepted.** The proxy replaces it with a function, so `new` fails. Move the function you want to intercept into its own module.
- **Only exported functions can be intercepted.** If the target export is not a function, the engine warns and skips that hook. Other exports are passed through untouched.
- **Anything that starts with `before`, `around` or `after` is read as a hook.** Do not export helpers from an interceptor module with those prefixes. Other exports are ignored.
- **The target and the interceptor module can only use imports that Node resolves on its own.** The engine imports both at build time to read their exports. A module that imports `Vendor_Module::path`, a `.vue` component, or a package not found from its folder is skipped, and only one console line is logged. Top-level code that needs the browser (`window`, `document`) can also make the import fail.
- **Exports are read once.** The wrapper covers the exports the target has at build start; interception does not follow functions that the target adds or replaces at runtime.
- **Hooks are per function, not per call site.** Every importer of the target is affected, with no way to opt a single caller out.
