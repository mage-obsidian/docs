# Política de seguridad de contenido

Bajo un tema Obsidian, `script-src` y `style-src` no llevan `'unsafe-inline'`. Un `<script>` inyectado no se ejecuta si la política no lo autoriza, y eso convierte a la política en la barrera principal contra un XSS almacenado. Esta página explica cómo el storefront mantiene esa barrera en pie en las páginas que sirve la caché de página.

---

## Cómo se autoriza el código en línea

Una política puede autorizar un `<script>` en línea de dos maneras:

- **Nonce:** un valor aleatorio que la respuesta declara en su cabecera y repite en cada script. Protege solo mientras es secreto y distinto en cada respuesta.
- **Hash:** el sha256 del contenido exacto del script, listado en la cabecera. No es un secreto, así que una caché puede guardarlo y repartirlo.

Una página en la caché de página es la misma respuesta para todos los visitantes. Con Varnish o Fastly, un nonce guardado con la página lo comparten todos hasta que vence el TTL, y quien lo lea en su propia respuesta lo conoce para todos. Con la caché de página integrada de Magento, un HIT vuelve a armar la cabecera sin el nonce, y los scripts de la propia página quedan bloqueados.

Por eso MageObsidian elige el método en cada respuesta:

| Respuesta | Los scripts en línea se autorizan con |
|---|---|
| Puede guardarse en la caché de página (lo normal en catálogo, CMS y búsqueda) | el sha256 de su contenido |
| Seguro que no se guarda: caché de página desactivada, un layout declarado no cacheable (carrito, checkout, cuenta) o una petición que no es GET ni HEAD | un nonce generado para esa respuesta |
| Se renderiza dentro de la caché de bloques | el sha256 de su contenido, sea cual sea la respuesta, porque ese HTML puede servirse después en una página cacheable |

Ante la duda gana el hash: un hash en una respuesta que nunca se cachea no cuesta nada, mientras que un nonce en una respuesta cacheada lo comparten todos los visitantes.

Los bloques ESI siguen a la página que los incluye. Magento renderiza un bloque con TTL durante la petición principal antes de reemplazarlo por `<esi:include>`, así que sus hashes ya están en la cabecera que recibe el visitante.

La configuración que el servidor entrega al storefront (traducciones, datos de secciones, flags de UX, base de iconos, pre-pintado) viaja en bloques de datos JSON, `<script type="application/json" data-mage-obsidian-config="…">`. El navegador no los ejecuta, así que la política no tiene nada que autorizar, y el código en línea que queda tiene el mismo hash en todas las store views de un despliegue.

## La caché de página integrada de Magento

Varnish y Fastly guardan la cabecera de la política junto con la página. La caché de página integrada de Magento no: guarda la página antes de que exista la cabecera y la vuelve a armar en cada HIT. Por eso MageObsidian guarda, con cada entrada de la caché integrada, todas las autorizaciones que la página juntó al renderizarse: hashes, nonces, hosts, esquemas y permisos de manejadores de eventos. Un HIT las repone antes de que Magento escriba la cabecera, así que la cabecera que recibe el visitante coincide con la de la respuesta que se guardó. La copia viaja en una cabecera privada de la entrada de caché y nunca llega al navegador.

Una entrada guardada antes de este comportamiento no trae esa copia. MageObsidian la trata como ausente y renderiza la página una vez más, así que la tienda nunca sirve una página cuya cabecera bloquearía sus propios scripts, aunque nadie limpie la caché después de actualizar.

### Al actualizar

- Recompila el tema. El static content deploy lo hace.
- Ejecuta `bin/magento cache:clean full_page block_html`. Los bloques cacheados antes de actualizar pueden llevar un nonce viejo en su HTML.
- Purga Varnish o Fastly. Las páginas cacheadas antes de actualizar llevan el nonce que comparten todos los visitantes hasta que vence su TTL.

### Si vuelves atrás

Vuelve a la versión anterior y ejecuta `bin/magento cache:clean full_page`. Sin esa limpieza, el código anterior sirve la cabecera privada guardada en las entradas nuevas. Es inocuo, porque solo lista hashes y hosts que la cabecera de la política ya publica, pero ensucia la respuesta.

## La política recomendada

Bajo un tema MageObsidian, MageObsidian aplica una política recomendada sobre la política final de cada respuesta del storefront. Viene activa por defecto, en una instalación nueva y en una tienda que actualiza:

- modo enforce, aunque la configuración de la tienda pida report-only;
- sin `'unsafe-eval'` en ninguna directiva;
- sin `'unsafe-inline'` en `script-src`, `style-src` ni `default-src`, salvo en `style-src` de una página que un módulo declaró con estilos en línea (ver [Páginas de pago](#paginas-de-pago));
- `base-uri 'self'` y `object-src 'none'`, en lugar de lo que se haya recogido para ellas.

Se aplica después de todos los collectors, incluidas las autorizaciones que añaden los módulos mientras se renderiza la página, así que una plantilla que añade `'unsafe-inline'` a `script-src` durante el render no consigue que llegue a la cabecera. Hosts, esquemas, hashes y nonces se conservan.

Mientras el servidor de desarrollo de Vite está activo, la política sigue en report-only, para que el cliente en línea y los recursos del servidor de desarrollo sigan funcionando. En modo producción el servidor de desarrollo siempre está apagado.

### Actualizar una tienda en report-only

Magento envía la política del storefront en report-only por defecto, así que la mayoría de las tiendas hoy no bloquean nada. Con esta versión, el navegador empieza a bloquear lo que la política no autoriza: un `<script>` en línea escrito a mano en una plantilla, un atributo `on*=` escrito en el marcado y cualquier `eval`. Antes de actualizar producción, abre las páginas importantes en una copia de staging con la consola del navegador abierta: ahí aparece cada script o estilo bloqueado. Pasa lo bloqueado al renderer seguro, como [debe hacerlo un módulo de terceros](#que-debe-hacer-un-modulo-de-terceros).

### Desactivarla

Ningún ajuste del panel la desactiva: relajar la seguridad del storefront pasa por una revisión de código. Un módulo la desactiva en su `etc/frontend/di.xml`:

```xml
<type name="MageObsidian\ModernFrontend\Service\Csp\RecommendedPolicy">
    <arguments>
        <argument name="enabled" xsi:type="boolean">false</argument>
    </arguments>
</type>
```

Después ejecuta `bin/magento setup:di:compile` y `bin/magento cache:clean full_page`. La política vuelve a ser la que resulta de la configuración de Magento y de la tienda, con el endurecimiento de scripts y estilos en línea de MageObsidian todavía aplicado.

### Por qué `form-action` queda como lo declara Magento

Magento y los módulos de pago declaran `form-action` como `'self'` más los hosts de los proveedores de pago. La política recomendada no lo reduce a `'self'`: Chrome también aplica `form-action` a las redirecciones que siguen al envío de un formulario, y PayPal Express y 3-D Secure redirigen al proveedor después de un POST. Una tienda que probó todos sus flujos de pago puede endurecerlo con la configuración propia de Magento, `csp/policies/storefront/forms`.

### Varnish y el tamaño de la cabecera

Cada script en línea distinto suma unos 55 bytes a la cabecera de la política. Varnish rechaza una respuesta del backend con una cabecera más larga que `http_resp_hdr_len`, 8 KB por defecto, y el visitante recibe un 503. Las páginas del propio storefront envían unos 5 KB de política, y la suite de verificación hace fallar cualquier página que pase de 8192 bytes. Si tus módulos llevan una página por encima del límite, súbelo en los parámetros de arranque de Varnish, junto con el total en el que tiene que caber:

```
-p http_resp_hdr_len=16k -p http_resp_size=64k
```

## Páginas de pago

La configuración propia de Magento deja pasar cualquier estilo en línea en el checkout y en el paso de facturación del checkout multidirección. MageObsidian no: las dos páginas prohíben los estilos en línea no autorizados, como el resto del storefront, y los estilos que el storefront emite en ellas se autorizan por hash. Un pedido se completa con cheque o giro postal, transferencia bancaria y orden de compra, y con reCAPTCHA en el paso de pago, sin una sola violación.

Un medio de pago que inyecta su propio elemento `<style>` queda bloqueado. Antes de actualizar una tienda que cobra, haz un pedido de prueba con cada medio de pago que usa. Si alguno necesita estilos en línea, es preferible autorizar por su hash el contenido exacto que inyecta, en un `csp_whitelist.xml`. Cuando ese contenido cambia en cada carga, el módulo que integra el medio de pago puede declarar la página en su `etc/frontend/di.xml`:

```xml
<type name="MageObsidian\ModernFrontend\Plugin\Csp\ApplyStrictInlinePolicy">
    <arguments>
        <argument name="inlineStylePages" xsi:type="array">
            <item name="checkout" xsi:type="string">checkout_index_index</item>
        </argument>
    </arguments>
</type>
```

Esa página recupera `'unsafe-inline'` en `style-src`, la política recomendada lo conserva, y el resto de las páginas sigue siendo estricto. En una página declarada, MageObsidian deja de calcular el hash de sus propios estilos, porque el navegador ignora `'unsafe-inline'` en cuanto la directiva lista un hash. En esa página sigue mandando el valor de `csp/policies/storefront_<acción>/styles` que la tienda haya fijado por su cuenta, en `config.xml` o en `env.php`.

No hay un ajuste del panel para esto, a propósito: permitir estilos en línea deja que un marcado inyectado cambie el aspecto de la página, y esa decisión pasa por una revisión de código. Ninguna configuración de la tienda permite estilos en línea en una página que el código no declaró.

## Qué debe hacer un módulo de terceros

Emitir los scripts y estilos en línea con el `SecureHtmlRenderer` de Magento:

```php
echo $secureRenderer->renderTag('script', [], $javascript, false);
```

MageObsidian intercepta el mismo `InlineUtil` que usa el renderer, así que el módulo no necesita cambios para quedar autorizado por hash en las páginas cacheables. Un `<script>` escrito a mano en una plantilla no queda autorizado y sigue bloqueado.

Dos prácticas mantienen la cabecera chica y estable:

- Dejar fuera del código en línea los valores que cambian de una página a otra. Ponlos en un atributo de datos o en un bloque de datos JSON y léelos desde el script.
- No poner nunca datos del visitante en un script en línea de una página cacheable. Eso ya era una fuga antes de esta política y lo sigue siendo.

## El nonce que algunos componentes todavía piden

Un componente puede pedirle el nonce a Magento directamente en lugar de pasar por el renderer. Los SDK de PayPal y Payment Services lo hacen para inyectar sus propios scripts. MageObsidian no les quita ese nonce, porque el botón dejaría de funcionar. En una página cacheable como la ficha de producto, ese nonce lo siguen compartiendo todos los visitantes, igual que antes. La suite de verificación del storefront lista las páginas cacheables cuya cabecera lleva un nonce, para que ese riesgo residual quede a la vista.
