# Cómo Contribuir

¡Gracias por tu interés en contribuir a **{{ config.site_name }}**! Este es un proyecto Open Source que busca revolucionar el desarrollo frontend en Magento. Tus aportes son fundamentales para mejorar la experiencia y expandir las capacidades del tema.

Reporta errores, propone mejoras, envía código, mejora la documentación o ayuda a otros usuarios en las discusiones. Para conversar con otros colaboradores en tiempo real, únete al [servidor de Discord]({{ config.extra.discord_link }}).

---

## Dónde contribuir

El código vive en dos monorepos, uno por tren de versiones. Abre los issues y los pull requests en el repositorio que posee el código, y usa sus Discussions para preguntas e ideas.

| Repositorio | Qué va ahí | Issues y PRs | Discussions |
|---|---|---|---|
| [`framework`]({{ config.extra.gh_framework_url }}) | El motor, el módulo núcleo, el CLI, el módulo Twig y el harness de Vite | [Issues]({{ config.extra.gh_framework_url }}/issues) · [Pull requests]({{ config.extra.gh_framework_url }}/pulls) | [Discussions]({{ config.extra.gh_discussions_framework }}) |
| [`storefront`]({{ config.extra.gh_storefront_monorepo_url }}) | Los módulos de dominio, `theme-base` y la UI | [Issues]({{ config.extra.gh_storefront_monorepo_url }}/issues) · [Pull requests]({{ config.extra.gh_storefront_monorepo_url }}/pulls) | [Discussions]({{ config.extra.gh_discussions_storefront }}) |

Dos cosas viven en sus propios repositorios:

- La piel OBSIDIAN, `theme-default`, en [su repositorio]({{ config.extra.gh_theme_default_url }}).
- Esta documentación, en el [repositorio de documentación]({{ config.extra.gh_docs_url }}).

---

## Los repositorios de paquetes son espejos

Cada paquete también se publica como su propio repositorio, por ejemplo `mage-obsidian/module-modern-frontend`, para que Composer y npm puedan resolverlo. Estos 24 repositorios son espejos de solo lectura de los monorepos: tienen los issues desactivados y no aceptan pull requests. Abre el issue o el pull request en `framework` o en `storefront`.

---

## Ejecutar las verificaciones

Ejecuta las verificaciones de la parte que cambiaste antes de abrir un pull request.

En los monorepos `framework` y `storefront`:

```bash
vendor/bin/phpunit
```

En `packages/js-package-utils`:

```bash
npm test
```

En este repositorio de documentación:

```bash
pytest scripts/tests
mkdocs build --strict
```

---

## Reconocimientos

Todas las contribuciones son valiosas y serán reconocidas en las notas de la versión correspondiente. ¡Gracias por ser parte de esta comunidad y por ayudar a mejorar **{{ config.site_name }}**!
