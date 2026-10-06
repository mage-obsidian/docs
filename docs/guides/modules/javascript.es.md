# JavaScript e imports

## Configuración de JavaScript

En **{{ config.extra.components_name }}**, todos los archivos JavaScript deben colocarse en los siguientes directorios:  
```
view/frontend/web/js
```
o  
```
view/frontend/web/components
```

#### **Recomendación Importante**

Aunque es posible utilizar el directorio `components` para scripts específicos, **recomendamos encarecidamente usar el directorio `js` para scripts personalizados**. Esto asegura una mejor organización y separación de conceptos, manteniendo una estructura de desarrollo clara y modular.

> El directorio `components` debe reservarse únicamente para lógica estrechamente vinculada a componentes específicos del frontend.

---

### Modificación de Scripts en los Temas

Los archivos JavaScript pueden ser sobrescritos en los temas para proporcionar funcionalidades o adaptaciones personalizadas específicas de un proyecto. Esta funcionalidad permite flexibilidad mientras se mantiene la estructura original del módulo.

> Más detalles sobre cómo sobrescribir scripts se explicarán en la sección dedicada a los temas.

---

### Mejores Prácticas

- **Estructura y Organización**: Usa el directorio `js` como la ubicación principal para todos tus scripts y lógica personalizada. Esto fomenta el mantenimiento y asegura una estructura de proyecto clara.
- **Integración con Paquetes de Node.js**: Puedes integrar paquetes de Node.js en tus scripts para ampliar funcionalidades o escribir JavaScript puro si no necesitas dependencias externas.
- **Formato Predeterminado de JavaScript**: Todos los scripts deben usar **ESM (ECMAScript Modules)** de forma predeterminada. Esto asegura compatibilidad con navegadores modernos y promueve una arquitectura modular.

---

### ¿Cómo Funciona?

1. **Proceso de Compilación con Vite**  
    Todos los archivos JavaScript son procesados y compilados por **Vite**, lo que resulta en una salida optimizada. Esto garantiza:
    - Rendimiento mejorado a través de técnicas modernas de empaquetado.
    - Tree-shaking para incluir solo el código necesario en el paquete final.
    - Compilaciones más rápidas y reemplazo en caliente de módulos (HMR) durante el desarrollo.

2. **Descargas Optimizadas**  
    **{{ config.extra.components_name }}** adopta un enfoque centrado en el rendimiento:
    - Solo se descargan los archivos JavaScript explícitamente utilizados en el frontend.
    - El código no utilizado se excluye del paquete final, reduciendo los tiempos de carga y mejorando la eficiencia.

3. **Integración con Vistas**  
    Los archivos JavaScript pueden ser incluidos en tus vistas o plantillas `.phtml` según sea necesario. Ejemplos específicos sobre cómo integrar scripts se proporcionarán más adelante en esta documentación.

---

### Ejemplo de Estructura de Directorios

Aquí tienes una estructura sugerida para tus archivos JavaScript:

```
view/
└── frontend/
    └── web/
        ├── js/
        │   ├── main.js         // Punto de entrada para lógica personalizada
        │   ├── utils.js        // Funciones utilitarias reutilizables
        │   └── services/
        │       └── api.js      // Lógica de integración con API
        └── components/
            ├── navbar.vue      // Componente Vue para la barra de navegación
            └── modal.vue       // Componente Vue para un modal
```

Esta estructura asegura que el directorio `js` sea la ubicación principal para scripts personalizados, mientras que el directorio `components` puede usarse para lógica específica de componentes si es absolutamente necesario.

---

### Beneficios

- **Modularidad**: Mantener los scripts en directorios dedicados asegura un código limpio y fácil de mantener.
- **Flexibilidad**: Los scripts pueden ser sobrescritos en los temas para adaptarse a requisitos específicos.
- **Rendimiento**: Gracias al proceso de compilación de Vite, solo se incluye el JavaScript necesario en el paquete final, reduciendo los tiempos de carga.
- **Escalabilidad**: La capacidad de integrar paquetes de Node.js y escribir JavaScript modular asegura que tu base de código pueda crecer según las necesidades del proyecto.

---

### Notas Clave

- **Usa el directorio `js` como la ubicación principal para scripts personalizados.**
- Todos los archivos JavaScript deben usar **ESM (ECMAScript Modules)** como formato predeterminado.
- Los archivos ubicados en `view/frontend/web/js` y `view/frontend/web/components` son rastreados y procesados automáticamente.
- Los archivos JavaScript pueden ser sobrescritos en los temas. Los detalles sobre esto se explicarán en la sección sobre temas.
- El sistema asegura que solo los scripts explícitamente incluidos en el frontend sean descargados, siguiendo un enfoque centrado en el rendimiento.
- Ejemplos de cómo incluir archivos JavaScript en plantillas `.phtml` se proporcionarán en secciones posteriores.

## Importaciones Entre Módulos de Magento

En **{{ config.extra.components_name }}**, las importaciones de archivos JavaScript y componentes Vue siguen convenciones flexibles que aplican específicamente a los archivos dentro de las carpetas `js` y `components`. Este enfoque asegura compatibilidad, modularidad y una integración fluida con los temas.

---

### Métodos de Importación Soportados

1. **Módulos de NPM**  
   Los paquetes de NPM se pueden importar de manera normal sin necesidad de configuraciones especiales:
   ```javascript
   import _ from 'lodash';
   import axios from 'axios';
   ```

2. **Importaciones Relativas y Absolutas**  
   Los archivos en las carpetas `js` y `components` pueden importarse usando rutas relativas o absolutas:
   ```javascript
   import Button from './components/Button.vue';  // Relativa
   import Navbar from '/view/frontend/web/components/Navbar.vue';  // Absoluta
   ```

3. **Importaciones Basadas en Módulos**  
   La característica más poderosa es la capacidad de importar archivos desde otros módulos de Magento utilizando la siguiente notación:
   ```javascript
   import Demo from 'Vendor_ModuleA::components/demo.vue';
   import Main from 'Vendor_ModuleF::js/main.js';
   ```

   - Si no se especifica el directorio raíz (por ejemplo, `components` o `js`), se usará `components` por defecto:
     ```javascript
     import Demo from 'Vendor_ModuleA::demo.vue';  // Equivalente a Vendor_ModuleA::components/demo.vue
     ```

4. **Importaciones Basadas en Temas**  
   También es posible importar archivos desde el tema utilizando una notación similar:
   ```javascript
   import Navbar from 'Theme::nav.vue';
   ```

   Esto sigue las mismas reglas de resolución que las importaciones basadas en módulos, permitiendo que los temas sobrescriban componentes o scripts sin complicaciones.

---

### Aplicación en `js` y `components`

Este sistema de importación está diseñado exclusivamente para los archivos ubicados en las carpetas `js` y `components`:
- **Archivos JavaScript**: Rastreados en `view/frontend/web/js`.
- **Componentes Vue**: Rastreados en `view/frontend/web/components`.

Por ejemplo:
- `Vendor_ModuleF::js/main.js` referencia un archivo en la carpeta `js`.
- `Vendor_ModuleA::components/demo.vue` referencia un archivo en la carpeta `components`.

Cualquier importación fuera de estas carpetas debe realizarse utilizando rutas relativas o absolutas estándar.

---

### Por Qué Esto Es Importante

#### Resolviendo Componentes Sobrescritos
Cuando los archivos son sobrescritos en los temas, **las importaciones relativas o absolutas no reflejan estos cambios**, lo que puede llevar a comportamientos inesperados.

Por ejemplo:
```javascript
import Bar from '../../bar.vue';
```
Si el componente `bar.vue` es sobrescrito en el tema, esta ruta relativa seguirá apuntando al componente original del módulo, ignorando la sobrescritura del tema.

En cambio:
```javascript
import Bar from 'Vendor_Module::bar.vue';
```
Al usar la notación `Vendor_Module::`, **Vite resuelve automáticamente el archivo apropiado**, respetando la jerarquía de sobrescritura (módulo -> tema). Esto garantiza que siempre se cargue el recurso correcto.

---

### Mejores Prácticas para Importaciones

1. **Usa Siempre Importaciones Basadas en Módulos**  
   Utiliza la notación `Vendor_Module::` para importar recursos desde módulos de Magento. Esto asegura:
   - Resolución adecuada de componentes o scripts sobrescritos en los temas.
   - Un código modular y fácil de mantener.

   Ejemplo:
   ```javascript
   import Button from 'Vendor_Module::button.vue';
   ```

2. **Evita Rutas Relativas o Absolutas**  
   A menos que sea absolutamente necesario, no utilices rutas relativas o absolutas para recursos en `js` o `components`. Estas rutas omiten el mecanismo de resolución de Vite, lo que puede provocar comportamientos inesperados si los recursos son sobrescritos.

3. **Usa Importaciones Desde el Tema para Sobrescrituras**  
   Si necesitas utilizar explícitamente un recurso desde el tema, utiliza la notación `Theme::`:
   ```javascript
   import Navbar from 'Theme::navbar.vue';
   ```

4. **Consistencia en la Notación de Importaciones**  
   Mantén un uso consistente de las notaciones `Vendor_Module::` y `Theme::` en todo tu proyecto para evitar confusiones y garantizar compatibilidad.

---

### Ejemplos

#### Importando Desde un Módulo
```javascript
import Card from 'Vendor_ModuleA::components/Card.vue';
import ApiService from 'Vendor_ModuleB::js/api-service.js';
```

#### Importando Desde el Tema
```javascript
import Header from 'Theme::header.vue';
```

#### Importación Incorrecta
```javascript
// Evita esto
import Footer from './Footer.vue'; // Esto no reflejará sobrescrituras en los temas
```

---

### Beneficios de las Importaciones Basadas en Módulos y Temas

1. **Sobrescrituras de Temas Sin Problemas**  
   Asegura que se cargue el componente o script correcto, respetando la jerarquía de sobrescrituras.

2. **Modularidad**  
   Fomenta un enfoque modular, haciendo que el código sea más mantenible y escalable.

3. **Flexibilidad**  
   Soporta personalizaciones sin romper la estructura original de los módulos.

4. **Prevención de Errores**  
   Evita comportamientos inesperados causados por rutas relativas o absolutas codificadas.

---

### Notas Clave

- Este sistema aplica únicamente a los archivos en las carpetas `js` y `components`.
- Usa la notación `Vendor_Module::` para todas las importaciones dentro de los módulos de Magento.
- Usa la notación `Theme::` para recursos específicamente desde los temas.
- Evita rutas relativas o absolutas a menos que sea necesario.
- Vite se encarga de resolver los componentes o scripts sobrescritos en los temas de forma automática.

Siguiendo estas recomendaciones, **{{ config.extra.components_name }}** proporciona un flujo de trabajo limpio, flexible y confiable para gestionar JavaScript y componentes Vue entre módulos y temas.

## Tooling de Importaciones

La [notación `Vendor_Module::`](javascript.md) es parte de primera clase del flujo de **{{ config.extra.components_name }}**, no solo una comodidad en tiempo de build. Tres piezas de tooling la vuelven cómoda y segura de usar: **autocompletado en el editor**, un **watcher en vivo de desarrollo** y un **guard fail-loud**.

No configuras nada de esto —lo prepara el build. Esta página explica qué hace para que el comportamiento no te sorprenda.

---

### Autocompletado en el Editor (`jsconfig.json`)

En cada build (y en vivo durante el desarrollo) el engine escribe un `jsconfig.json` en la raíz de las fuentes del tema que le enseña al editor a resolver los especificadores `Vendor_Module::`. Cada especificador se mapea al **archivo fuente real** al que resuelve, derivado del mismísimo mapa de herencia que usa el build —así que lo que ve el editor siempre coincide con lo que produce el build.

Lo que obtienes en VS Code (con la extensión Vue/Volar) o PhpStorm:

- **Autocompletado** de las rutas de import `Vendor_Module::`.
- **Ir a la definición** (Ctrl/Cmd+clic) salta directo al archivo `.vue`/`.js` real, incluso cuando vive en otro módulo o en un tema padre.
- Resuelven tanto la forma completa (`Vendor_Module::components/Card`) como el atajo (`Vendor_Module::Card`).
- Un comodín `"*"` también apunta los paquetes npm (`vue`, `@heroicons/...`, `pinia`, …) al `node_modules` del harness de build, para que resuelvan en el editor también.

> **Importante:** El `jsconfig.json` generado está **gestionado por el build** —lleva un marcador `// Generated by mage-obsidian` en la primera línea, está en el git-ignore y se reescribe en cada build. No lo edites. Si ya existe un `jsconfig.json` escrito a mano (sin el marcador), el build lo deja intacto y te avisa; elimínalo para que el build tome el control.

> **Consejo:** Tras el primer build (o si la resolución se ve desactualizada), ejecuta **Restart TS Server** en tu editor para que vuelva a leer el `jsconfig.json` regenerado.

#### Contenedores y mounts

Cuando el build corre dentro de un contenedor pero editas los archivos en una ruta de host distinta (un bind-mount), las rutas absolutas grabadas en `jsconfig.json` apuntarían a rutas del contenedor que el editor no puede abrir. Define `MAGE_OBSIDIAN_TYPES_PATH_MAP` para remapearlas:

```dotenv
# from=>to[,from2=>to2]; gana el prefijo más largo
MAGE_OBSIDIAN_TYPES_PATH_MAP=/var/www/html/vite=>/home/yo/proyecto/component-modern-frontend/vite,/var/www/html=>/home/yo/proyecto/magento-root
```

Cuando el build y el editor comparten sistema de archivos, déjalo sin definir —el mapeo identidad es lo correcto.

---

### Watcher en Vivo de Desarrollo

El mapa de herencia se calcula una vez al arrancar el dev server y se cachea. Agregar o eliminar una fuente `.vue`/`.js` sería normalmente invisible hasta un reinicio —tanto para el resolver de runtime como para el `jsconfig.json` del editor.

Un watcher solo de desarrollo lo soluciona. Cuando **creas o eliminas** un componente o fuente JS bajo un directorio vigilado (el dir `web` de cada módulo adherido, más el tema y su cadena de padres), este:

1. Invalida el mapa de herencia cacheado del tema.
2. Invalida el conjunto de interceptores compilado, para que un plugin agregado o reapuntado con el servidor levantado tenga efecto en el build siguiente.
3. Reescribe el mapa de resolución persistido (para que `Vendor_Module::` resuelva el archivo nuevo en runtime).
4. Regenera el `jsconfig.json` del tema (para que el editor también lo vea).

Los plugins de resolución leen ese mapa **en cada petición** en vez de capturarlo al arrancar el servidor, que es lo que hace visible el refresco sin reiniciar.

Registra `sources changed — refreshed <theme> import resolution`. Los cambios tienen debounce y las escrituras son idempotentes, así que editar el *contenido* de un archivo (a diferencia de agregar/eliminar archivos) no lo dispara —de eso se encarga el HMR propio de Vite.

---

### Guard Fail-Loud

Un especificador `Vendor_Module::` que no resolvía antes era **externalizado en silencio** por el bundler, solo para romperse en runtime sin causa clara. Ahora un guard corre el **último** en la cadena de resolvers: si un especificador `::` llega hasta él, ninguno de los resolvers reales pudo manejarlo —un typo o un archivo faltante— así que lanza un error de build/dev en su lugar.

El error nombra el especificador no resuelto, el importador y las alternativas válidas más cercanas:

```text
[mage-obsidian] Unresolved import "Acme_Catalog::ProductsCard".
  imported by: .../components/Page.vue
  Did you mean:
    - Acme_Catalog::ProductCard
    - Acme_Catalog::products/Card
```

Para una ruta de asset, te dice exactamente dónde se esperaba el archivo:

```text
[mage-obsidian] Unresolved import "Acme_Catalog::assets/logo.svg".
  imported by: .../components/Header.vue
  Asset not found. Expected a theme override at <theme>/Acme_Catalog/web/assets/logo.svg
  or the module at <module>/view/frontend/web/assets/logo.svg.
```

Y cuando no hay nada registrado bajo el namespace, te recuerda habilitar el módulo/tema y regenerar el contrato:

```text
  Nothing is registered under "Acme_Catalog". Is the module/theme enabled and
  compatible, and the contract regenerated (bin/magento mage-obsidian:frontend:config --generate)?
```

---

### Notas Clave

- El `jsconfig.json` es generado, está en el git-ignore y no debe editarse a mano.
- Usa `Restart TS Server` tras el primer build para activar el autocompletado.
- Un import `::` roto rompe el build con sugerencias —nunca se publica en silencio.
- El watcher de desarrollo mantiene sincronizados el autocompletado y la resolución de runtime a medida que agregas/eliminas archivos, sin reinicios.
