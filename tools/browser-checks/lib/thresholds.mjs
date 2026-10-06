// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
export function failingScores(results, min) {
  const failures = [];
  for (const r of results) {
    for (const metric of ["performance", "accessibility"]) {
      if (r[metric] < min[metric]) {
        failures.push(`${r.url} ${metric} ${Math.round(r[metric] * 100)} < ${Math.round(min[metric] * 100)}`);
      }
    }
  }
  return failures;
}
