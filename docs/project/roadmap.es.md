---
description: "Dónde ha estado MageObsidian y hacia dónde va, con hitos enlazados al registro de cambios."
---
# Hoja de ruta

Dónde ha estado MageObsidian y hacia dónde va. Cada hito enlaza con su entrada del changelog; lo planificado no lleva fecha hasta que se está construyendo.

{{ timeline() }}

## Ahora, siguiente, después

{{ roadmap_lanes() }}

## Qué se ha verificado

Medido contra **Magento Open Source 2.4.9** con el
arnés de verificación privado, sobre el par
`theme-default` / `theme-base`. Cada fila lleva la fecha en que se midió:

| Registro | Cifra | Medido |
|---|---|---|
| Entradas de paridad | 486 — 247 cubiertas, 71 parciales, 138 fuera de alcance, 27 resueltas, 3 bloqueadas | 2026-10-06 |
| Layouts de página | 15 entradas, 13 cubiertas por una prueba ejecutada, 2 fuera de alcance | 2026-09-22 |
| Pruebas unitarias del motor de build | 321 | 2026-09-22 |
| Pruebas unitarias del arnés | 268 | 2026-09-22 |

Una entrada "cubierta" significa que una prueba se ejecutó y observó el comportamiento en esa plataforma; una
declaración en un tema nunca cuenta como cobertura por sí sola. Lo que estas cifras dejan fuera está en
[Alcance conocido](known-scope.md).

Nada de esta página es una promesa de entrega; la [política de versionado](versioning.md) sí lo es.
