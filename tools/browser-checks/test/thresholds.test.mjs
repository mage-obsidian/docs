// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import { test } from "node:test";
import assert from "node:assert/strict";
import { failingScores } from "../lib/thresholds.mjs";

test("pages under a threshold are reported with the score", () => {
  const results = [
    { url: "/", performance: 0.93, accessibility: 0.97 },
    { url: "/getting-started/", performance: 0.84, accessibility: 0.99 },
    { url: "/es/", performance: 0.95, accessibility: 0.9 },
  ];
  assert.deepEqual(failingScores(results, { performance: 0.9, accessibility: 0.95 }), [
    "/getting-started/ performance 84 < 90",
    "/es/ accessibility 90 < 95",
  ]);
});
