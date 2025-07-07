{% raw %}
# Motor Twig

**MageObsidian** incluye un motor de plantillas [Twig](https://twig.symfony.com/) que corre **junto** al `.phtml` nativo de Magento. Viene **incluido por defecto** con la instalación de los componentes —no tienes que activarlo. Se entrega como su propio módulo, así que puedes apagarlo sin afectar nada más.

> **Incluido por defecto, nunca obligatorio, totalmente retrocompatible.** Twig viene con la instalación pero nada te obliga —ni a ti ni a módulos/temas de terceros— a usarlo: `.phtml` sigue funcionando intacto, y adoptar Twig nunca es una migración. `.twig` y `.phtml` coexisten en el mismo tema, el fallback de temas funciona idéntico para ambos. Puedes escribir `.twig` una plantilla a la vez, solo `.phtml`, o [deshabilitar el motor por completo](#deshabilitar-twig).

---

## Por Qué Twig

Twig se posiciona con honestidad como una mejora de **experiencia de desarrollo** para el shell de plantilla del lado servidor —no como una feature de rendimiento de front. La página que llega al navegador es idéntica tanto si el shell fue un `.phtml` como un `.twig`; ambos compilan a PHP y corren en el servidor.

Lo que te aporta Twig sobre el `.phtml` crudo:

- **Auto-escaping de HTML por defecto** —la principal ganancia de seguridad. La salida se escapa salvo que la marques explícitamente como segura.
- **Herencia de plantillas limpia** (`{% extends %}`, `{% block %}`, `{% include %}`) con la sintaxis familiar de Twig.
- **Una superficie restringida** —las plantillas expresan presentación, no PHP arbitrario.
- **Soporte de IDE de primera clase** para el lenguaje Twig.

El rendimiento de front sigue viniendo de la arquitectura de [islas Vue](../components/modules/0105-vue-islands.md), que una plantilla `.twig` dirige exactamente igual que un `.phtml` (mediante el helper `render_vue`).

---

## Cómo Coexiste Con phtml

Magento despacha una plantilla a un motor **según su extensión de archivo** (`Magento\Framework\View\Element\Template::fetchView`). El motor nativo está registrado para `phtml`; este módulo registra una entrada más para `twig`:

- Un bloque cuyo `template="…​.twig"` lo renderiza Twig.
- Un bloque cuyo `template="…​.phtml"` sigue usando el motor PHP nativo.
- El mapa `engines` es un argumento de tipo array que **se fusiona entre módulos**, así que esto solo *añade* `twig` —nunca reemplaza `phtml`.

El fallback de temas no cambia: Magento resuelve una plantilla por ruta, agnóstico a su extensión, así que un tema hijo sobrescribe el `.twig` de un padre exactamente como sobrescribe un `.phtml`.

---

## Instalación

Nada que instalar. El módulo `mage-obsidian/module-modern-frontend-twig` es una dependencia de `mage-obsidian/component-modern-frontend`, así que `composer require mage-obsidian/component-modern-frontend` (la [instalación](../getting-started/installation.md) estándar) ya lo incluye. Arrastra consigo `twig/twig ^3.12`.

## Deshabilitar Twig

Twig es un módulo normal de Magento, así que deshabilitarlo es una sola línea —`.phtml` sigue funcionando exactamente igual:

```bash
bin/magento module:disable MageObsidian_ModernFrontendTwig
bin/magento setup:upgrade
```

Tras esto, la extensión `.twig` deja de estar registrada como motor. Vuélvelo a activar cuando quieras con `bin/magento module:enable MageObsidian_ModernFrontendTwig`. No hay feature flag —el estado habilitado del módulo *es* el interruptor.

---

## Una Primera Plantilla

Una plantilla `.twig` se renderiza dentro del contexto de su bloque de Magento. A diferencia de `.phtml`, no hay un `$this` implícito; el bloque se expone como la variable `block`:

```twig
{# view/frontend/templates/example.twig #}
<section class="example">
    <h1>{{ block.getTitle() }}</h1>

    {# Monta una isla Vue, exactamente como el renderVueComponent de phtml #}
    {{ render_vue('Acme_Catalog::ProductCard', { id: block.getProductId() }) }}
</section>
```

Cablealo desde el layout con cualquier bloque —para los helpers de MageObsidian (`render_vue`, `hero_icon`, …) usa un bloque que extienda `MageObsidian\ModernFrontend\Block\Template`:

```xml
<referenceContainer name="content">
    <block class="MageObsidian\ModernFrontend\Block\Template"
           name="acme.example"
           template="Acme_Catalog::example.twig"/>
</referenceContainer>
```

---

## Caché

Las plantillas Twig compiladas se cachean bajo `var/cache/twig`. En **modo developer**, `auto_reload` recompila una plantilla cada vez que su fuente cambia, `{{ dump() }}` está disponible y una variable indefinida lanza un error (`strict_variables`) en lugar de renderizarse como cadena vacía. En **modo producción** se usa el caché compilado tal cual. El auto-escaping de HTML siempre está activo.

---

## Próximos Pasos

- [Helpers y Filtros](helpers.md) — la referencia completa de funciones Twig de MageObsidian y filtros de escape.
- [Islas Vue](../components/modules/0105-vue-islands.md) — cómo `render_vue` monta componentes.
{% endraw %}
