// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import lighthouse from "lighthouse";
import { chromium } from "playwright";
import { LIGHTHOUSE_PAGES } from "./lib/pages.mjs";
import { failingScores } from "./lib/thresholds.mjs";

const base = process.argv[2] ?? "http://127.0.0.1:8000/";
const browser = await chromium.launch({ args: ["--remote-debugging-port=9222"] });
const results = [];
for (const path of LIGHTHOUSE_PAGES) {
  const run = await lighthouse(base + path, { port: 9222, onlyCategories: ["performance", "accessibility"], formFactor: "mobile", screenEmulation: { mobile: true, width: 412, height: 823, deviceScaleFactor: 1.75, disabled: false }, throttlingMethod: "simulate" });
  results.push({ url: "/" + path, performance: run.lhr.categories.performance.score, accessibility: run.lhr.categories.accessibility.score, lcp: run.lhr.audits["largest-contentful-paint"].numericValue });
}
await browser.close();
results.forEach((r) => console.log(`${r.url} perf ${Math.round(r.performance * 100)} a11y ${Math.round(r.accessibility * 100)} lcp ${Math.round(r.lcp)}ms`));
const failures = [
  ...failingScores(results, { performance: 0.9, accessibility: 0.95 }),
  ...results.filter((r) => r.lcp >= 2500).map((r) => `${r.url} lcp ${Math.round(r.lcp)}ms >= 2500ms`),
];
failures.forEach((f) => console.log("FAIL " + f));
process.exit(failures.length ? 1 : 0);
