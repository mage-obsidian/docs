---
description: "Qué no cubre MageObsidian y por qué, con el registro de paridad con Luma leído el 2026-10-07."
---
# Alcance conocido

Lo que MageObsidian no cubre, y por qué. Cada punto aquí es una decisión o un límite medido, no algo dejado fuera de vista.

## Paridad con Luma

El registro de paridad se leyó el 2026-10-07 contra **Magento Open Source 2.4.9**. Lista 529 entradas: 262 cubiertas, 56 parciales, 22 sin cubrir, 44 resueltas, 142 fuera de alcance y 3 bloqueadas. Una entrada cubierta tiene una prueba que observó el comportamiento, y todos los bloques que el core aporta a esa pantalla están contemplados. Una entrada parcial tiene la prueba, pero a uno o más de esos bloques le falta su equivalente; los cuatro grupos siguientes son los que no están cubiertos.

Hasta el 2026-10-06 el registro solo comparaba pantallas, así que una pantalla que MageObsidian volvía a declarar contaba como cubierta aunque faltara un bloque que otro módulo del core le agregaba. Ahora también compara los 832 bloques que el core declara en esas pantallas. Las 71 entradas parciales que encontró al principio salían de esa comparación, y antes se contaban todas como cubiertas; quedan 59.

### Parciales

86 bloques en 56 pantallas no tienen equivalente. Cada uno figura en el registro con lo que pierde el cliente. Por área:

| Área | Qué falta |
|---|---|
| Cuenta y sesión | La página de éxito no ofrece crear una cuenta a un invitado que acaba de pagar. |
| Catálogo y búsqueda | Videos de producto, mensajes de precios por cantidad, aviso de incrementos de cantidad, imagen de categoría, swatches en las tarjetas del listado, barra lateral de comparación, productos vistos recientemente, sugerencias de búsqueda y términos relacionados, y enlaces para saltar la galería. Las vistas de producto y los términos de búsqueda ya no se registran para los reportes del admin. |
| Pedidos y emails | Las selecciones de los bundles y los títulos de los enlaces descargables en los emails de pedido, factura y nota de crédito, y el Fixed Product Tax en sus totales. Los comentarios de pedidos, facturas, envíos y notas de crédito. Volver a pedir e Imprimir pedido en las páginas de documentos, el enlace Rastrear pedido, la barra lateral de Pedidos recientes, el estado en los documentos impresos, y los enlaces de impresión y de productos descargables en la página de éxito. Las opciones de los ítems en los pasos del checkout multidirección. |
| Lista de deseos | Actualizar cantidades, comentarios por ítem, editar las opciones de un ítem guardado, ver qué variante se guardó, los resúmenes de reseñas y la barra lateral. |
| Marketing y feeds | Seguimiento de conversiones de Google Ads, tanto con gtag como con la etiqueta antigua (Google Analytics 4 sí está portado). Enlaces RSS en el head, el footer, las categorías, la lista de deseos y los pedidos. |
| Plataforma | Hashes de Subresource Integrity en los scripts del checkout (requisito 6.4.3 de PCI DSS 4.0). Un selector entre grupos de tiendas. La página para darse de baja de las alertas de stock. |

### Hallazgos de la auditoría funcional

La comparación de pantallas y bloques no puede ver un ajuste de la tienda que Magento respeta dentro de un bloque que sí existe, ni un comportamiento de script sin equivalente. Una auditoría funcional de esos casos dio al registro un origen propio: cada entrada nombra el ajuste, la plantilla o el script del core que define el comportamiento y el valor que lo dispara, y solo se resuelve con una prueba que fije ese valor. Añadió 36 entradas, y el inventario de los formularios con reCAPTCHA y el trabajo de sesión añadieron 7 más: 17 resueltas, 22 abiertas y 4 fuera de alcance.

Resueltas: el monto mínimo de pedido, una cantidad reducida, un cambio de precio y una línea sin stock se anuncian en el carrito y dejan inoperante Proceder al checkout; un carrito con un producto de precio mínimo anunciado dice que el total llegará después; las tarjetas de cross-sell se añaden a la bolsa, a la lista de deseos y a la comparación como una tarjeta del listado; un alta sigue la redirección al carrito cuando la tienda la pide; la bolsa lateral respeta su interruptor de visualización, su máximo de líneas con el enlace «N de M» y el enlace de edición; el carrito pagina sus líneas; el limitador «todos» ya no rompe la página de categoría; el código postal es opcional en los países que la tienda declara y el teléfono sigue su ajuste; el prefijo, el segundo nombre, el sufijo, la fecha de nacimiento, el género, la identificación fiscal, la empresa, el fax y el número de IVA siguen su configuración en los formularios de la cuenta y en el checkout, igual que el número de líneas de calle; la longitud mínima y las clases de caracteres de la contraseña se anuncian, se exigen y se miden; el cheque, la transferencia y el pago contra entrega muestran las instrucciones del comerciante; una orden de compra pide su número y lo registra; un cliente identificado puede facturar a una dirección guardada; y el captcha de imagen que espera a los intentos fallidos ya aparece en el inicio de sesión en segundo plano cuando falla el tercero; el inicio de sesión envía el token de reCAPTCHA, así que funciona con el desafío activo; la configuración de cookies del navegador (dominio, ruta, Secure, sitio web) se publica y se aplica a toda cookie que escribe el storefront; un navegador que rechaza cookies lo sabe en lugar de fallar en silencio; Recordarme y el contexto del checkout viajan con el inicio de sesión en segundo plano y el registro, así que el carrito persistente sobrevive; un visitante reconocido recibe su nombre con «¿No eres tú?»; y el menú del teléfono ofrece Iniciar sesión, Crear una cuenta, Mi cuenta y Cerrar sesión.

Se inventariaron los formularios que protegen los módulos de reCAPTCHA contra 2.4.9. El cupón del carrito, compartir la lista de deseos, la reseña, enviar a un amigo, el registro, el restablecimiento de contraseña, la información de la cuenta, el contacto, el boletín y confirmar el pedido muestran cada uno el desafío y aceptan la respuesta, y la revisión del checkout multidirección muestra ahora también los términos y condiciones. Dos ajustes no tienen un formulario del storefront que proteger y quedan fuera de alcance: PayPal Payflow Pro, que el checkout no ofrece, y el reenvío de la confirmación, que el core protege solo en su operación REST y GraphQL.

Abiertas, por área:

| Área | Qué configura la tienda y el storefront ignora |
|---|---|
| Impuestos | Líneas del carrito que mezclan un precio sin impuestos con un total con impuestos, el resumen completo de impuestos y ocultar un impuesto en cero, tarifas de envío y precio de un configurable con un solo importe cuando se configuran ambos, y el Fixed Product Tax en el carrito. |
| Checkout | La recogida en tienda de MSI no tiene interfaz aunque sus módulos están habilitados. |
| Catálogo y búsqueda | El conteo de productos en la navegación por capas, el máximo de destinatarios de «enviar a un amigo», la longitud máxima de la búsqueda avanzada, la comparación que salta el renderizador de precio (lo que puede revelar un precio mínimo anunciado) y falla al añadir un configurable a la bolsa, la disponibilidad y «solo quedan» en la página de producto, y el precio de un descargable que no sigue a los enlaces elegidos. |
| Reseñas | El formulario ofrecido a invitados cuando la tienda no lo permite, la falta de paginación y la falta de valoración en las tarjetas. |
| Cromo de página | Los enlaces al boletín, la lista de deseos, las reseñas y el contacto siguen visibles con la función desactivada, el logo, el mensaje de bienvenida y el copyright configurados en el admin no se muestran, y los textos fijos del pie no son traducibles. |
| Widgets | Solo el widget de lista de productos está portado, y los contenedores que reciben widgets desde el admin no existen. |

### Bloqueadas

Tres entradas están bloqueadas. Ninguna es una función faltante que nadie haya mirado; cada una espera una decisión.

| Entrada | Por qué está bloqueada |
|---|---|
| Fondo de video de Page Builder desde YouTube o Vimeo | Un fondo de video autoalojado se reproduce. Uno alojado por un proveedor necesita el reproductor del proveedor en un marco, lo que es una petición de terceros durante la carga y una decisión de privacidad. Las URL de proveedores se rechazan en lugar de cargarse en silencio. Se desbloquea cuando el storefront defina cómo se obtienen los embebidos de proveedores. |
| Fila de Page Builder a ancho completo del borde (full-bleed) | Las filas contenidas y de ancho completo están corregidas. El borde a borde real necesita un ancho relativo al viewport que desborda horizontalmente por el ancho de la barra de desplazamiento salvo que un ancestro recorte, así que espera una decisión sobre dónde corresponde el recorte en el shell del tema. |
| Estado inicial renderizado en servidor de los tipos de contenido de mapa y banner | Guardan un marcador de isla sin estado inicial dentro, así que lo que muestran aparece cuando la isla se hidrata. Ninguno mueve la página, pero ninguno se lee sin script. Necesita un renderizador de islas por petición. |

### Fuera de alcance

142 entradas están fuera de alcance, cada una con su motivo en el registro. Por familia:

| Entradas | Familia | Motivo |
|---|---|---|
| 53 | Declaraciones de renderizadores | No son una pantalla: aportan renderizadores de ítems a otro handle. |
| 24 | Pantallas consolidadas | Equivalentes por otra vía: MageObsidian consolida lo que el core separa por tipo de producto. |
| 17 | PayPal y Payment Services | El 2026-08-27 se decidió no construir esas pantallas en este proyecto. |
| 15 | Fragmentos y handles base | No son una pantalla del storefront: un fragmento, un handle base que cada uno concreto vuelve a declarar, o un endpoint de Knockout que el stack reemplazó. |
| 7 | Ítems de wishlist con opciones | Deliberadamente sin usar: el ítem enlaza a la página del producto. |
| 4 | Handles sin ruta | El handle no tiene ruta en esta versión de la plataforma. |
| 4 | Comportamiento reexpresado | MAP como un desplegable nativo sin JavaScript, remember-me gestionado de forma central. |
| 3 | Herramientas Swagger | Herramientas de desarrollo servidas solo fuera del modo producción, con su propio JavaScript heredado. |
| 2 | Flujos de pago fuera del sitio | Llegar a ellos necesita un método de pago que coloque el pedido y envíe al comprador fuera del sitio. |
| 2 | Productos declinados | Un checkout vendido por separado y una biblioteca de componentes de copiar y pegar: decisiones tomadas, no brechas abiertas. |
| 2 | Comportamientos declinados | La vista de lista del catálogo, que el tema descarta a propósito, y la traducción en línea, una herramienta de desarrollo. |
| 2 | Ajustes sin formulario en el storefront | reCAPTCHA para PayPal Payflow Pro, que el checkout no ofrece, y para el reenvío de la confirmación, que el core protege solo mediante su API. |
| 7 | Reemplazos individuales | La ruta de la galería de producto, el layout de página del checkout del core, un handle del carrito que la plataforma no enruta, un handle que ningún controlador del core carga, una plantilla de descripción de categoría de Page Builder, el endpoint del listado de reseñas, y la primera búsqueda no cacheable, que es comportamiento del core. |

## Pasarelas de pago

Ninguna pasarela de pago comercial ha sido verificada. El punto de extensión sí: un método de pago puede renderizar su propia interfaz dentro del checkout, pedir sus propios campos y entregar al comprador a una pasarela y recuperarlo, y ese mecanismo se ejercita con un método de sonda construido para ello. Una pasarela real necesita su propia verificación.

## Adobe Commerce

Adobe Commerce es detectado e inventariado por `mage-obsidian:frontend:doctor`, que informa qué familias del storefront exclusivas de Commerce tiene habilitadas una tienda. No está en la matriz de compatibilidad. El storefront se recorrió una vez sobre Adobe Commerce 2.4.9 el 2026-10-06; Adobe Commerce Cloud, las pasarelas de pago y las funciones exclusivas de Commerce no están verificadas. Consulta [Adobe Commerce](../getting-started/adobe-commerce.md).
