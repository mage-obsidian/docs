// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
import { chromium } from "playwright";
import { UI_PAGES } from "./lib/pages.mjs";

const base = process.argv[2] ?? "http://127.0.0.1:8000/";
const browser = await chromium.launch();
const page = await browser.newPage();
const findings = [];
for (const path of UI_PAGES) {
  for (const lang of ["", "es/"]) {
    await page.goto(base + lang + path, { waitUntil: "load" });
    await page.waitForFunction(() => document.querySelectorAll(".md-code__nav").length > 0, null, { timeout: 5000 }).catch(() => {});
    const missing = await page.evaluate(() =>
      [...document.querySelectorAll(".md-content pre > code")].filter((code) => !code.closest("pre").querySelector('.md-code__button[data-md-type="copy"]')).length,
    );
    if (missing) findings.push(`/${lang}${path} ${missing} code block(s) without a copy button`);
  }
}
for (const lang of ["", "es/"]) {
  await page.goto(base + lang + "guides/", { waitUntil: "load" });
  const dead = await page.evaluate(() =>
    [...document.querySelectorAll(".grid.cards > ul > li")].filter((card) => {
      const box = card.getBoundingClientRect();
      const hit = document.elementFromPoint(box.right - 12, box.bottom - 12);
      return !hit || !hit.closest("a");
    }).length,
  );
  if (dead) findings.push(`/${lang}guides/ ${dead} card(s) not clickable outside their title`);
}
for (const lang of ["", "es/"]) {
  await page.goto(base + lang, { waitUntil: "load" });
  await page.locator("input[data-md-component='search-query']").fill("islands");
  const found = await page.locator(".md-search-result__item").first().waitFor({ timeout: 10000 }).then(() => true, () => false);
  if (!found) findings.push(`/${lang} search for "islands" returned no results`);
}
await browser.close();
findings.forEach((f) => console.log(f));
process.exit(findings.length ? 1 : 0);
