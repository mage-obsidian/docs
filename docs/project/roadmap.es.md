---
description: "Dónde ha estado MageObsidian y hacia dónde va, con hitos enlazados al registro de cambios."
---
# Hoja de ruta

Dónde ha estado MageObsidian y hacia dónde va. Cada hito enlaza con su entrada del changelog; lo planificado no lleva fecha hasta que se está construyendo.

{{ timeline() }}

## Ahora, siguiente, después

{{ roadmap_lanes() }}

## Qué se ha verificado

Medido con el arnés de verificación privado, sobre el par
`theme-default` / `theme-base`. Los registros se miden contra **Magento Open Source 2.4.9**;
las filas de extremo a extremo nombran su plataforma. Cada fila lleva la fecha en que se midió:

| Registro | Cifra | Medido |
|---|---|---|
| Entradas de paridad | 529 — 318 cubiertas, 0 parciales, 142 fuera de alcance, 67 resueltas, 2 bloqueadas | 2026-10-12 |
| Layouts de página | 15 entradas, 13 cubiertas por una prueba ejecutada, 2 fuera de alcance | 2026-09-22 |
| Suite de extremo a extremo, Magento Open Source 2.4.9 | 682 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Suite de extremo a extremo, Mage-OS 3.1.0 | 672 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Suite de extremo a extremo, Adobe Commerce 2.4.9 | 659 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Pruebas unitarias del motor de build | 403 | 2026-10-13 |
| Pruebas unitarias del arnés | 383 | 2026-10-13 |

Una entrada "cubierta" significa que una prueba se ejecutó y observó el comportamiento en esa plataforma; una
declaración en un tema nunca cuenta como cobertura por sí sola. Lo que estas cifras dejan fuera está en
[Alcance conocido](known-scope.md).

Nada de esta página es una promesa de entrega; la [política de versionado](versioning.md) sí lo es.
