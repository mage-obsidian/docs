// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import { chromium } from "playwright";
import { OVERFLOW_PAGES } from "./lib/pages.mjs";

const base = process.argv[2] ?? "http://127.0.0.1:8000/";
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 360, height: 780 } });
const findings = [];
for (const path of OVERFLOW_PAGES) {
  for (const lang of ["", "es/"]) {
    await page.goto(base + lang + path, { waitUntil: "networkidle" });
    const width = await page.evaluate(() => document.documentElement.scrollWidth);
    if (width > 360) findings.push(`/${lang}${path} scrollWidth ${width} > 360`);
  }
}
await browser.close();
findings.forEach((f) => console.log(f));
process.exit(findings.length ? 1 : 0);
