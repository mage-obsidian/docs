---
description: "Where MageObsidian has been and where it goes next, with milestones linked to the changelog."
---
# Roadmap

Where MageObsidian has been, and where it goes next. Every milestone links to its changelog entry; what is planned carries no date until it is being built.

{{ timeline() }}

## Now, next, later

{{ roadmap_lanes() }}

## What has been verified

Measured with the private verification harness, on the
`theme-default` / `theme-base` pair. The registers are measured against **Magento Open Source 2.4.9**;
the end-to-end rows name their platform. Each row carries the date it was measured:

| Register | Figure | Measured |
|---|---|---|
| Parity register | 529 entries in total: 318 covered, 67 resolved, 2 blocked and 142 out of scope | 2026-10-12 |
| Page layouts | 15 entries, 13 covered by an executed test, 2 out of scope | 2026-09-22 |
| End-to-end suite, Magento Open Source 2.4.9 | 682 passed, every failure with a known cause | 2026-10-13 |
| End-to-end suite, Mage-OS 3.1.0 | 672 passed, every failure with a known cause | 2026-10-13 |
| End-to-end suite, Adobe Commerce 2.4.9 | 659 passed, every failure with a known cause | 2026-10-13 |
| Build engine unit tests | 403 | 2026-10-13 |
| Harness unit tests | 383 | 2026-10-13 |

The parity register lists every Luma screen and behaviour, and every gap an audit found. Each entry is in one of four states:

- **Covered** — a test ran and observed the behaviour on that platform. A declaration in a theme never counts as coverage on its own.
- **Resolved** — a gap an audit found (functional, competitive, security or performance) that has since been closed.
- **Blocked** — kept open on purpose, by the owner's decision; [Known scope](known-scope.md#blocked) says why.
- **Out of scope** — not a screen to replace, or one decided against, each with its reason: item renderers that feed another screen, screens consolidated into one, the PayPal and Payment Services screens; [Known scope](known-scope.md#out-of-scope) lists them by family.

What these figures leave out is on [Known scope](known-scope.md).

Nothing on this page is a delivery promise; the [versioning policy](versioning.md) is.
