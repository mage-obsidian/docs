# Continuidad de navegación

Pasar de una página del escaparate a la siguiente debería sentirse como una sola aplicación, no como
una serie de páginas que se desarman y se vuelven a armar. En un teléfono lento eso no es lo que el
navegador hace por defecto, y MageObsidian cierra esa brecha con dos piezas pequeñas de
`mage-obsidian/module-storefront`.

## Qué hace el navegador por su cuenta

Cuando el comprador sigue un enlace, Chrome mantiene la página anterior en pantalla hasta que el
documento nuevo pinta algo ("paint holding"). Lo primero que pinta un escaparate es su cabecera, así
que con una CPU lenta el comprador ve la página anterior, luego una cabecera sobre un cuerpo vacío y
después la página armándose por partes. Medido sobre la demo con la CPU limitada a 6×, siete de cada
nueve navegaciones mostraron al menos un frame completamente en blanco, aun con los documentos ya
precargados.

## Retener la página anterior

El escaparate mantiene la página anterior en pantalla hasta que la siguiente analizó su contenido
principal:

- Un guion inline mínimo en el `<head>` añade `<link rel="expect" href="#obsidian-main-end"
  blocking="render">`. El navegador no muestra el documento nuevo hasta que ese elemento existe.
- El elemento es un `<div id="obsidian-main-end">` vacío y oculto: el último hijo del contenedor
  `main.content`, así que llega después de la miga de pan, el título y el listado, y antes del pie.
- El guion solo lo hace cuando el comprador **llega desde otra página de la misma tienda**
  (`navigation.activation.from` tiene valor). Una primera visita, una llegada desde un buscador y una
  recarga pintan de forma progresiva como antes, así que las métricas de primera carga y Lighthouse
  no cambian.
- Las imágenes siguen llegando después del cambio, en el espacio que ya tienen reservado.

El enlace se emite con el `SecureHtmlRenderer` de Magento, así que lleva el nonce de la CSP y
funciona con una política estricta.

=== "CLI"

    ```bash
    bin/magento config:set mage_obsidian/navigation/retain 0   # 1 para volver a activarlo
    bin/magento cache:flush
    ```

=== "Admin"

    **Stores → Configuration → MageObsidian → Frontend → Speculative Loading → Hold the Previous
    Page Until the Next Is Ready**

Viene **activado**. Desactivarlo devuelve la pintura progresiva entre páginas; nada más depende de
ello.

!!! note "Un layout sin `main.content`"

    El marcador vive en el contenedor `main.content`. Un page layout que elimina ese contenedor no
    tiene marcador, y el navegador libera la pintura cuando terminó de analizar todo el documento:
    la página aparece igual, solo que más tarde. Los navegadores sin `rel="expect"` o sin la
    Navigation API ignoran la retención y pintan de forma progresiva.

## Respuesta inmediata al clic

Mientras la página anterior está retenida, el clic tiene que notarse. Una barra fina en la parte
superior de la ventana arranca en el acto cuando el comprador sigue un enlace o envía un formulario
hacia otra página de la tienda, y una región `role="status"` anuncia "Cargando la página" a las
tecnologías de asistencia sin robar el foco.

- La dispara el evento `navigate` de la Navigation API, así que ignora las pestañas nuevas, las
  descargas, las anclas de la misma página y los enlaces a otros sitios.
- Desaparece cuando la navegación falla o se detiene, y cuando la página vuelve desde la caché de ida
  y vuelta.
- Con `prefers-reduced-motion: reduce` la barra se queda quieta en lugar de animarse.
- Nunca recibe eventos de puntero ni mueve el layout; su color es `--color-accent`.

## Prerender: viable, con condiciones

El grupo Speculative Loading ya ofrece `prerender` como modo. Se midió el 2026-09-29 contra una
tienda de desarrollo, con un Chrome sin ningún cliente de automatización conectado. Con uno
conectado —Playwright, DevTools— Chrome se niega a prerenderizar y reporta
`PrerenderingDisabledByDevTools`, así que ninguna suite automática puede observarlo.

| Pregunta | Hallazgo |
|---|---|
| ¿Se activa? | Sí. La página preparada se mostró con `activationStart` en 5 s, ya pintada. |
| Datos privados preparados antes | La página prerenderizada carga las secciones del cliente mientras se prepara. Cuando el carrito cambió en el medio, las recargó al activarse y mostró el conteo correcto unos **130 ms** después. El valor viejo queda en pantalla ese tiempo. |
| Analítica | Segura tal como está. La cola de gtag se llena, pero la librería espera la primera interacción del comprador, que solo puede ocurrir después de la activación. |
| Carga en el servidor | Un `customer/section/load` extra que no se puede cachear (PHP) por página preparada, además del documento que ya cuesta un prefetch, más las imágenes de su viewport. Con eagerness `moderate` eso ocurre con cada enlace sobre el que el puntero se detiene 200 ms. |
| Con la retención | Sin conflicto. Una página prerenderizada ya está pintada cuando se activa, así que no hay nada que retener. |

**Decisión:** mantener `prefetch` por defecto. Prerender vale la pena cuando se cumplan tres
condiciones, y eso corresponde a un cambio propio:

1. El almacén de secciones del cliente espera `prerenderingchange` antes de pintar datos privados,
   para que una página activada nunca muestre un valor viejo.
2. El prerender se limita a los enlaces con más probabilidad de seguirse (las tarjetas de producto)
   o corre con eagerness `conservative`, para que recorrer un listado con el puntero no cueste una
   petición PHP por tarjeta.
3. Su verificación corre fuera de la suite automática, porque un Chrome bajo automatización nunca
   prerenderiza.

## Cómo se verifica

`storefront-verification` recorre el escaparate haciendo clic —portada, un listado desde el menú, una
tarjeta de producto, otro listado, el logo, una búsqueda, el carrito— en escritorio y con un perfil
Pixel 7, con la CPU limitada a 6×, y graba la pantalla mientras tanto
(`specs/navigation-continuity.paint.spec.ts`). Cada frame entre un clic y la página terminada se
clasifica; la prueba falla ante un frame en blanco o una página a medio construir (una cabecera
sobre un cuerpo vacío) y adjunta el frame culpable. Cargar páginas directamente con `page.goto` no
cuenta como cobertura de este comportamiento.
