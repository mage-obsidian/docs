// This file is part of the MageObsidian - Documentation project.
//
// SPDX-FileCopyrightText: 2024 Jeanmarcos Juarez
// SPDX-License-Identifier: MIT
const isEs = () => document.documentElement.lang === "es";

const drawerToggle = document.querySelector("label.md-header__button[for='__drawer']");
const drawerInput = document.getElementById("__drawer");
const drawer = document.querySelector(".md-sidebar--primary");

const syncDrawer = () => {
  if (!drawerToggle || !drawerInput || !drawer) return;
  const narrow = window.matchMedia("(max-width: 76.234375em)").matches;
  drawerToggle.setAttribute("aria-expanded", String(drawerInput.checked));
  drawer.inert = narrow && !drawerInput.checked;
};

if (drawerToggle && drawerInput) {
  drawerToggle.setAttribute("role", "button");
  drawerToggle.setAttribute("tabindex", "0");
  drawerToggle.setAttribute("aria-label", isEs() ? "Abrir navegación" : "Open navigation");
  drawerToggle.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      event.stopImmediatePropagation();
      drawerToggle.click();
    }
  });
  drawerInput.addEventListener("change", syncDrawer);
  window.addEventListener("resize", syncDrawer);
  syncDrawer();
}

const patch = () => {
  document.querySelectorAll(".md-code__content, pre > code").forEach((block) => {
    if (block.scrollWidth > block.clientWidth) {
      block.setAttribute("tabindex", "0");
      block.setAttribute("role", "region");
      block.setAttribute("aria-label", isEs() ? "Bloque de código desplazable" : "Scrollable code block");
    }
  });

  document.querySelectorAll(".md-sidebar__scrollwrap").forEach((wrap) => {
    if (wrap.scrollHeight > wrap.clientHeight && !wrap.querySelector(".md-nav__link")) {
      wrap.setAttribute("tabindex", "0");
    }
  });

  const search = document.querySelector(".md-search");
  if (search) {
    search.setAttribute("role", "dialog");
    search.setAttribute("aria-label", isEs() ? "Buscar" : "Search");
  }
  const results = document.querySelector(".md-search-result__meta");
  if (results) results.setAttribute("aria-live", "polite");

  document.querySelectorAll("a[target='_blank']:not([data-mo-hint])").forEach((link) => {
    link.dataset.moHint = "";
    const hint = document.createElement("span");
    hint.className = "md-visually-hidden";
    hint.textContent = isEs() ? " (se abre en una pestaña nueva)" : " (opens in a new tab)";
    link.append(hint);
  });
};

document$.subscribe(patch);
document.fonts.ready.then(patch);
