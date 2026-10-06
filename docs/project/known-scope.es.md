---
description: "Qué no cubre MageObsidian y por qué, con el registro de paridad con Luma leído el 2026-10-06."
---
# Alcance conocido

Lo que MageObsidian no cubre, y por qué. Cada punto aquí es una decisión o un límite medido, no algo dejado fuera de vista.

## Paridad con Luma

El registro de paridad se leyó el 2026-10-06 contra **Magento Open Source 2.4.9**. Lista 486 entradas: 247 cubiertas, 71 parciales, 27 resueltas, 138 fuera de alcance y 3 bloqueadas. Una entrada cubierta tiene una prueba que observó el comportamiento, y todos los bloques que el core aporta a esa pantalla están contemplados. Una entrada parcial tiene la prueba, pero a uno o más de esos bloques le falta su equivalente; los tres grupos siguientes son los que no están cubiertos.

Hasta el 2026-10-06 el registro solo comparaba pantallas, así que una pantalla que MageObsidian volvía a declarar contaba como cubierta aunque faltara un bloque que otro módulo del core le agregaba. Ahora también compara los 832 bloques que el core declara en esas pantallas. Las 71 entradas parciales salen de esa comparación, y antes se contaban todas como cubiertas.

### Parciales

108 bloques en 71 pantallas no tienen equivalente. Cada uno figura en el registro con lo que pierde el cliente. Por área:

| Área | Qué falta |
|---|---|
| Bloquea una acción cuando un ajuste de la tienda está activo | Con reCAPTCHA activado para cupones, no se puede aplicar un cupón desde el carrito. Con reCAPTCHA activado para la lista de deseos, no se puede compartir la lista. Con los términos y condiciones activados, la revisión del checkout multidirección no muestra los acuerdos para aceptar. El core sigue validando los tres en el servidor. |
| Carrito | No se muestran los avisos de monto mínimo de pedido, de cantidad reducida ni de cambio de precio, y estos no deshabilitan el checkout. Un carrito con un producto de precio mínimo anunciado (MAP) muestra su total. Las tarjetas de cross-sell no permiten agregar a la lista de deseos ni a comparar. |
| Cuenta y sesión | En el teléfono no hay enlace de Iniciar sesión ni de Mi cuenta en la cabecera ni en el menú lateral. "Recordarme" se pierde en el inicio de sesión por defecto. Un inicio de sesión o un registro iniciado desde el checkout pierde el contexto del checkout. No hay enlace de Crear una cuenta en la cabecera ni oferta de cuenta en la página de éxito. A un cliente con las cookies desactivadas no se le avisa. El dominio de cookies y el ajuste Secure no se publican al navegador, así que la cookie `form_key` los ignora. |
| Catálogo y búsqueda | Videos de producto, mensajes de precios por cantidad, aviso de incrementos de cantidad, imagen de categoría, swatches en las tarjetas del listado, barra lateral de comparación, productos vistos recientemente, sugerencias de búsqueda y términos relacionados, y enlaces para saltar la galería. Las vistas de producto y los términos de búsqueda ya no se registran para los reportes del admin. |
| Pedidos y emails | Las selecciones de los bundles y los títulos de los enlaces descargables en los emails de pedido, factura y nota de crédito, y el Fixed Product Tax en sus totales. Los comentarios de pedidos, facturas, envíos y notas de crédito. Volver a pedir e Imprimir pedido en las páginas de documentos, el enlace Rastrear pedido, la barra lateral de Pedidos recientes, el estado en los documentos impresos, y los enlaces de impresión y de productos descargables en la página de éxito. Las opciones de los ítems en los pasos del checkout multidirección. |
| Lista de deseos | Actualizar cantidades, comentarios por ítem, editar las opciones de un ítem guardado, ver qué variante se guardó, los resúmenes de reseñas y la barra lateral. |
| Marketing y feeds | Seguimiento de conversiones de Google Ads, tanto con gtag como con la etiqueta antigua (Google Analytics 4 sí está portado). Enlaces RSS en el head, el footer, las categorías, la lista de deseos y los pedidos. |
| Plataforma | Hashes de Subresource Integrity en los scripts del checkout (requisito 6.4.3 de PCI DSS 4.0). Un selector entre grupos de tiendas. La página para darse de baja de las alertas de stock. La invalidación de datos del cliente entre websites que comparten origen. |

### Bloqueadas

Tres entradas están bloqueadas. Ninguna es una función faltante que nadie haya mirado; cada una espera una decisión.

| Entrada | Por qué está bloqueada |
|---|---|
| Fondo de video de Page Builder desde YouTube o Vimeo | Un fondo de video autoalojado se reproduce. Uno alojado por un proveedor necesita el reproductor del proveedor en un marco, lo que es una petición de terceros durante la carga y una decisión de privacidad. Las URL de proveedores se rechazan en lugar de cargarse en silencio. Se desbloquea cuando el storefront defina cómo se obtienen los embebidos de proveedores. |
| Fila de Page Builder a ancho completo del borde (full-bleed) | Las filas contenidas y de ancho completo están corregidas. El borde a borde real necesita un ancho relativo al viewport que desborda horizontalmente por el ancho de la barra de desplazamiento salvo que un ancestro recorte, así que espera una decisión sobre dónde corresponde el recorte en el shell del tema. |
| Estado inicial renderizado en servidor de los tipos de contenido de mapa y banner | Guardan un marcador de isla sin estado inicial dentro, así que lo que muestran aparece cuando la isla se hidrata. Ninguno mueve la página, pero ninguno se lee sin script. Necesita un renderizador de islas por petición. |

### Fuera de alcance

138 entradas están fuera de alcance, cada una con su motivo en el registro. Por familia:

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
| 7 | Reemplazos individuales | La ruta de la galería de producto, el layout de página del checkout del core, un handle del carrito que la plataforma no enruta, un handle que ningún controlador del core carga, una plantilla de descripción de categoría de Page Builder, el endpoint del listado de reseñas, y la primera búsqueda no cacheable, que es comportamiento del core. |

## Pasarelas de pago

Ninguna pasarela de pago comercial ha sido verificada. El punto de extensión sí: un método de pago puede renderizar su propia interfaz dentro del checkout, pedir sus propios campos y entregar al comprador a una pasarela y recuperarlo, y ese mecanismo se ejercita con un método de sonda construido para ello. Una pasarela real necesita su propia verificación.

## Adobe Commerce

Adobe Commerce es detectado e inventariado por `mage-obsidian:frontend:doctor`, que informa qué familias del storefront exclusivas de Commerce tiene habilitadas una tienda. No está en la matriz de compatibilidad. El storefront se recorrió una vez sobre Adobe Commerce 2.4.9 el 2026-10-06; Adobe Commerce Cloud, las pasarelas de pago y las funciones exclusivas de Commerce no están verificadas. Consulta [Adobe Commerce](../getting-started/adobe-commerce.md).
