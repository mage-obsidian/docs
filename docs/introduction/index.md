> **Note:** This project is developed in my free time, which may result in slower progress than expected. If you'd like to support its development and accelerate progress, consider contributing financially. More details can be found in the [Project Support](../support/project) section.

The **{{ config.site_name }}** project emerges as a disruptive proposal to revolutionize the frontend development experience in Magento. For years, Magento's frontend has been constrained by tools and practices that, while useful in their time, have added unnecessary complexity to the ecosystem. Technologies such as Less, Knockout, and RequireJS have turned development into a challenging process that overwhelms even experienced developers.

<div style="display: grid; justify-content: center; grid-template-columns: repeat(auto-fit, minmax(40px, 100px)); gap: 40px; justify-items: center; align-items: center; margin-top: 20px;">
  <a href="https://magento.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/magento-logo.png" alt="Magento" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://vitejs.dev" target="_blank" rel="noopener noreferrer">
     <img src="/assets/vite-logo.png" alt="Vite" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://vuejs.org" target="_blank" rel="noopener noreferrer">
     <img src="/assets/vuejs-logo.png" alt="Vue.js" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://tailwindcss.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/tailwind-logo.png" alt="TailwindCSS" style="max-width: 100%; height: auto;" />
  </a>
  <a href="https://twig.symfony.com" target="_blank" rel="noopener noreferrer">
     <img src="/assets/twig-logo.png" alt="Twig" style="max-width: 100%; height: auto;" />
  </a>
</div>

**{{ config.extra.components_name }}** aims to simplify and modernize Magento's frontend development with an innovative and open-source alternative. This project introduces two key aspects:

1. **{{ config.extra.components_name }}:**  
    Already available and open source, these tools have been created to implement a completely new approach to Magento theme development. They enable the integration of modern technologies like **Vite**, **TailwindCSS**, **Vue.js**, and **ESM** (native JavaScript modules), providing a more accessible, efficient, and developer-friendly experience.  
    [Learn more about {{ config.extra.components_name }}](../components).

2. **{{ config.extra.theme_name }}:**  
    The base theme is built entirely on the mentioned tools and is already functional. It does not inherit anything from traditional themes like **Blank** or **Luma**, enabling a completely new design aligned with modern practices and free from the historical constraints of Magento's frontend. It targets Magento Open Source today, with Adobe Commerce and Mage-OS support planned for the future.  
    [Learn more about {{ config.extra.theme_name }}](../theme) — or see it running in the [live demo]({{ config.extra.demo_url }}){target=_blank rel=noopener}.

One of the main strengths of **{{ config.extra.components_name }}** is that **it does not follow a PWA approach**. Instead, it leverages Magento's existing system of layouts, blocks, and templates, preserving its native architecture. This approach allows developers to take advantage of modern tools and current standards without compromising compatibility with existing modules and functionalities, offering a smoother and more efficient development experience.

On top of that native foundation, **{{ config.extra.components_name }}** layers in modern building blocks: Vue components mount as **lazy-hydrated [islands](../components/modules/0105-vue-islands.md)**, a built-in **[i18n](../components/modules/0107-i18n.md)** layer translates them with Magento's native dictionaries, and an optional **[Twig engine](../twig/index.md)** — included by default and fully compatible with `.phtml` — is available for those who want HTML auto-escaping and clean template inheritance.

Additionally, although the use of **NPM** packages has always been possible in Magento, **{{ config.extra.components_name }}** makes it simpler and more straightforward. Developers can now elegantly leverage the vast ecosystem of tools and libraries available, aligning Magento's frontend with global web development best practices.

In summary, while the base theme is still in progress, the tools developed by **{{ config.extra.components_name }}** are already available and provide a revolutionary solution for redefining frontend development in Magento. This approach combines flexibility, efficiency, and modernity, contributing significantly to the Magento ecosystem.
