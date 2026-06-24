# Key Features

## Components

- **Independence from traditional themes:** **{{ config.extra.components_name }}** completely eliminates dependency on themes like **Blank** and **Luma**, enabling a modern and flexible design free from the historical constraints that have complicated Magento's frontend.

- **Integration with modern tools:** Leverages cutting-edge technologies such as **Vite**, **TailwindCSS**, **Vue.js**, and **ESM** (native JavaScript modules), providing an agile development experience aligned with global best practices.

- **Instant updates with Hot Module Replacement (HMR):** Delivers a seamless development experience by eliminating waiting times and enabling immediate updates during development.

- **Simplified access to the NPM ecosystem:** Streamlines the integration of modern tools and libraries through optimized **NPM** access, aligning Magento's frontend with current web development standards.

- **Centralized control over visual representation:** Introduces an approach where the primary control of visual representation resides in the theme, while modules can still make specific modifications. This ensures a clear separation of responsibilities, fostering more modular, organized, and flexible development.

- **Modernization leveraging native foundations:** Builds upon Magento's native system of Layouts, Blocks, and Templates to modernize the frontend, integrating the best of Magento's frontend ecosystem with modern tools.

- **Interactive Vue islands:** Vue components mount as independent, **lazy-hydrated islands** — below-the-fold components cost nothing until they enter the viewport, and a page with no islands ships no Vue at all. See [Vue Islands](../components/modules/0105-vue-islands.md).

- **Built-in internationalization:** Translate phrases in components with `$t('…')` against Magento's native `js-translation.json`, with a collector command for the `.vue` sources. See [Internationalization](../components/modules/0107-i18n.md).

- **Built-in structured data (JSON-LD):** Auto-emits schema.org markup (Organization, WebSite, Breadcrumb, Product) for rich results — cacheable, no extra JavaScript, with a `json_ld` helper for custom types. See [Structured Data](../components/modules/0130-structured-data.md).

- **Core-Web-Vitals image helper:** An `image` helper renders `<img>`/`<picture>` with `width`/`height` (auto-detected for assets) to kill CLS, plus `loading`/`fetchpriority` to prioritize the LCP image. See [Responsive Images](../components/modules/0140-images.md).

- **Opt-in shared state (Pinia):** Islands can share reactive state through one page-wide Pinia — loaded only by components that import a store (none for the rest) — with a ready `useCustomerData` bridge mirroring Magento's cart/customer sections, FPC-safe. See [Shared State](../components/modules/0150-state-management.md).

- **Optional Twig engine, included by default:** A [Twig](../twig/index.md) template engine ships alongside the native `.phtml` — fully compatible, never mandatory (disable it with one command). Adds HTML auto-escaping and clean template inheritance for those who want them.

- **Scaffolding generators:** `bin/magento mage-obsidian:generate:{module,theme,component}` create modules, themes, and Vue components already wired for the frontend. See [Scaffolding](../getting-started/scaffolding.md).

- **Developer-friendly experience:** Designed to be intuitive and enjoyable, **{{ config.extra.components_name }}** promotes creativity and simplifies the use of widely adopted industry tools, making frontend development a much more pleasant task.

- **Multi-theme support:** Compatible with a structure that allows managing multiple derivative themes, avoiding code and logic duplication. This simplifies the maintenance of diverse designs tailored to each store or brand within the same ecosystem.

- **Theme inheritance:** Implements a hierarchy that enables extending and reusing existing themes. This means that themes compatible with this new structure can share common functionalities and styles, reducing development and maintenance efforts.

## Theme

- **SEO-friendly foundation:** Designed to ensure fast load times, clean URLs, and a structure that maximizes search engine performance. The theme leverages optimized components to deliver a fast and well-structured frontend.

- **Exceptional performance:** Thanks to the underlying components, the theme is optimized to load only what is necessary, resulting in ultra-fast load times. This improves both user experience and performance metrics such as Google's Core Web Vitals.

[![Lighthouse report: 100 across Performance, Accessibility, Best Practices and SEO](/assets/lighthouse-100.png)]({{ config.extra.demo_url }}){ .lighthouse-shot target=_blank rel=noopener }

- **Modern and customizable design:** Built with the latest standards, the theme allows complete customization to meet any business's needs. Its flexibility ensures developers can create unique experiences without compromising performance.

- **Easy and fast updates:** The theme's design facilitates maintenance, ensuring improvements and updates can be implemented without affecting site stability.

- **Modular design:** The theme allows extending and modifying specific parts without affecting the overall structure, making it easy to create unique variations for each brand or product line.

- **Future-proof:** Developed with a focus on the future, the theme adapts easily to advances in frontend technology and the evolving needs of businesses.
