// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";
import { KEY_PAGES } from "./lib/pages.mjs";

const base = process.argv[2] ?? "http://127.0.0.1:8000/";
const schemes = [
  { name: "light", colorScheme: "light", palette: { index: 1, color: { scheme: "default", primary: "custom", accent: "custom" } } },
  { name: "dark", colorScheme: "dark", palette: { index: 2, color: { scheme: "slate", primary: "custom", accent: "custom" } } },
  { name: "dark-system", colorScheme: "dark", palette: null },
];
const browser = await chromium.launch();
const findings = [];
for (const scheme of schemes) {
  const context = await browser.newContext({ colorScheme: scheme.colorScheme });
  if (scheme.palette) {
    await context.addInitScript((p) => localStorage.setItem("/.__palette", JSON.stringify(p)), scheme.palette);
  }
  const page = await context.newPage();
  for (const path of KEY_PAGES) {
    await page.goto(base + path, { waitUntil: "networkidle" });
    const result = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
    for (const v of result.violations) {
      findings.push(`${scheme.name} /${path} ${v.id} (${v.nodes.length}) ${v.nodes[0]?.target?.join(" ")}`);
    }
  }
  await context.close();
}
await browser.close();
findings.forEach((f) => console.log(f));
process.exit(findings.length ? 1 : 0);
