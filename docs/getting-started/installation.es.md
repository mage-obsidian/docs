
# Instalación

La instalación de **{{ config.site_name }}** consta de dos partes principales: los **componentes**, que ya están disponibles, y el **tema**, que aún se encuentra en desarrollo.

## {{ config.extra.components_name }}

Los componentes son el núcleo de **{{ config.site_name }}**, diseñados para proporcionar un frontend moderno y eficiente para Magento. Sigue estos pasos para instalarlos:

### 1. Instalación vía Composer

Utiliza Composer para agregar los componentes a tu proyecto:

```bash
composer require mage-obsidian/component-modern-frontend
```

### 2. Instalar dependencias con npm

Asegúrate de que todas las dependencias necesarias estén configuradas correctamente. Ejecuta:

```bash
npm --prefix vite install
```

### 3. Configurar Magento

Actualiza la configuración de Magento para registrar los componentes:

```bash
bin/magento setup:upgrade
```

### 4. Generar configuración inicial

Ejecuta el siguiente comando para generar la configuración inicial de los componentes de frontend:

```bash
bin/magento obsidian:frontend:config --generate
```

### 5. Todo listo para desarrollar

¡Los componentes están configurados y listos para ser utilizados en tu proyecto! Ahora puedes comenzar a desarrollar tu tema con las herramientas modernas que ofrece **{{ config.extra.components_name }}**.

---

## Más información

Para obtener más detalles sobre la personalización de los componentes, iniciar el desarrollo de un tema y conocer todos los beneficios y ventajas, consulta la sección [Documentación detallada de los componentes](../../components).

---

## {{ config.extra.theme_name }}

El tema basado en **{{ config.extra.components_name }}** aún está en desarrollo y no está disponible para su instalación. Una vez completado, proporcionará un diseño moderno, SEO-friendly y altamente personalizable para tiendas Magento.

### Estado actual
- El diseño está en progreso y estará disponible próximamente.
- Mientras tanto, puedes explorar los componentes para empezar a construir soluciones personalizadas.

---

## Más información

Para más información sobre el tema, visita la sección [Tema](../../theme).
