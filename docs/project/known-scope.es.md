---
description: "Qué no cubre MageObsidian y por qué, con el registro de paridad con Luma leído el 2026-09-22."
---
# Alcance conocido

Lo que MageObsidian no cubre, y por qué. Cada punto aquí es una decisión o un límite medido, no algo dejado fuera de vista.

## Paridad con Luma

El registro de paridad se leyó el 2026-09-22 contra **Magento Open Source 2.4.9**. Lista 485 entradas: 317 cubiertas, 27 resueltas, 138 fuera de alcance y 3 bloqueadas. Una entrada cubierta tiene una prueba que observó el comportamiento; los dos grupos siguientes son los que no lo están.

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

Adobe Commerce es detectado e inventariado por `mage-obsidian:frontend:doctor`, que informa qué familias del storefront exclusivas de Commerce tiene habilitadas una tienda. No está verificado: el inventario informa lo que está instalado y no afirma nada más. Consulta [Adobe Commerce](../getting-started/adobe-commerce.md).
