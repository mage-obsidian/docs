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
| Pantallas y handles de Luma | 457: las 322 que aplican están hechas (312 cubiertas por una prueba, 10 resueltas); 135 fuera de alcance | 2026-10-12 |
| Ajustes de tienda que Luma respeta (auditoría funcional) | 43: 39 resueltas, 4 fuera de alcance | 2026-10-12 |
| Brechas frente a otros frontends (auditoría competitiva) | 14: 10 resueltas, 2 fuera de alcance, 2 bloqueadas por decisión | 2026-10-12 |
| Auditoría de seguridad | 9: 4 cubiertas, 5 resueltas | 2026-10-12 |
| Auditoría de rendimiento | 6: 2 cubiertas, 3 resueltas, 1 fuera de alcance | 2026-10-12 |
| Layouts de página | 15 entradas, 13 cubiertas por una prueba ejecutada, 2 fuera de alcance | 2026-09-22 |
| Suite de extremo a extremo, Magento Open Source 2.4.9 | 682 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Suite de extremo a extremo, Mage-OS 3.1.0 | 672 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Suite de extremo a extremo, Adobe Commerce 2.4.9 | 659 aprobadas, cada fallo con causa conocida | 2026-10-13 |
| Pruebas unitarias del motor de build | 403 | 2026-10-13 |
| Pruebas unitarias del arnés | 383 | 2026-10-13 |

Las cinco primeras filas son el registro de paridad, 529 entradas en total, separadas según de dónde salió cada una. Cada entrada está en uno de cuatro estados:

- **Cubierta** — una prueba se ejecutó y observó el comportamiento en esa plataforma. Una declaración en un tema nunca cuenta como cobertura por sí sola.
- **Resuelta** — una brecha que encontró una auditoría (funcional, competitiva, de seguridad o de rendimiento) y que ya se cerró.
- **Bloqueada** — se mantiene abierta a propósito, por decisión del propietario; [Alcance conocido](known-scope.md#bloqueadas) explica por qué.
- **Fuera de alcance** — no es una pantalla que reemplazar, o se decidió no hacerla, cada una con su razón: renderizadores de ítems que alimentan otra pantalla, pantallas consolidadas en una, las pantallas de PayPal y Payment Services; [Alcance conocido](known-scope.md#fuera-de-alcance) las lista por familia.

Lo que estas cifras dejan fuera está en [Alcance conocido](known-scope.md).

Nada de esta página es una promesa de entrega; la [política de versionado](versioning.md) sí lo es.
