/*
 * This file is part of the MageObsidian - Documentation project.
 *
 * SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
 * SPDX-License-Identifier: MIT
 */
document.addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
    const toggle = document.querySelector("label[for='__search']");
    if (toggle) {
      event.preventDefault();
      toggle.click();
    }
  }
});

document$.subscribe(() => {
  document.querySelectorAll(".mo-code [role='tablist']").forEach((list) => {
    const tabs = [...list.querySelectorAll("[role='tab']")];
    const select = (tab) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => select(tab));
      tab.addEventListener("keydown", (event) => {
        if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
          const next = tabs[(index + (event.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
          select(next);
          next.focus();
        }
      });
    });
  });
});
