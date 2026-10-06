# Roadmap

Where MageObsidian has been, and where it goes next. Every milestone links to its changelog entry; what is planned carries no date until it is being built.

{{ timeline() }}

## Now, next, later

{{ roadmap_lanes() }}

## What has been verified

Measured on 2026-09-22 against **Magento Open Source 2.4.9** with the
private verification harness, on the
`theme-default` / `theme-base` pair:

| Register | Figure |
|---|---|
| Parity entries | 485 — 317 covered, 138 out of scope, 27 resolved, 3 blocked |
| Page layouts | 15 entries, 13 covered by an executed test, 2 out of scope |
| Build engine unit tests | 321 |
| Harness unit tests | 268 |

A "covered" entry means a test ran and observed the behaviour on that platform; a
declaration in a theme never counts as coverage on its own. What these figures leave out is on
[Known scope](known-scope.md).

Nothing on this page is a delivery promise; the [versioning policy](versioning.md) is.
