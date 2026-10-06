# How to Contribute

Thank you for your interest in contributing to **{{ config.site_name }}**! This is an Open Source project aimed at revolutionizing frontend development in Magento. Your contributions are essential to improving the experience and expanding the theme's capabilities.

Report bugs, propose improvements, send code, improve the documentation or help other users in the discussions. To talk with other contributors in real time, join the [Discord server]({{ config.extra.discord_link }}).

---

## Where to contribute

The code lives in two monorepos, one per release train. Open issues and pull requests in the repository that owns the code, and use its Discussions for questions and ideas.

| Repository | What goes there | Issues and PRs | Discussions |
|---|---|---|---|
| [`framework`]({{ config.extra.gh_framework_url }}) | The engine, the core module, the CLI, the Twig module and the Vite harness | [Issues]({{ config.extra.gh_framework_url }}/issues) · [Pull requests]({{ config.extra.gh_framework_url }}/pulls) | [Discussions]({{ config.extra.gh_discussions_framework }}) |
| [`storefront`]({{ config.extra.gh_storefront_monorepo_url }}) | The domain modules, `theme-base` and the UI | [Issues]({{ config.extra.gh_storefront_monorepo_url }}/issues) · [Pull requests]({{ config.extra.gh_storefront_monorepo_url }}/pulls) | [Discussions]({{ config.extra.gh_discussions_storefront }}) |

Two things live in their own repositories:

- The OBSIDIAN skin, `theme-default`, in [its repository]({{ config.extra.gh_theme_default_url }}).
- This documentation, in the [docs repository]({{ config.extra.gh_docs_url }}).

---

## The package repositories are mirrors

Every package is also published as its own repository, such as `mage-obsidian/module-modern-frontend`, so that Composer and npm can resolve it. These 24 repositories are read-only mirrors of the monorepos: they have issues disabled and accept no pull requests. Open the issue or the pull request in `framework` or `storefront` instead.

---

## Running the checks

Run the checks of the part you changed before you open a pull request.

In the `framework` and `storefront` monorepos:

```bash
vendor/bin/phpunit
```

In `packages/js-package-utils`:

```bash
npm test
```

In this documentation repository:

```bash
pytest scripts/tests
mkdocs build --strict
```

---

## Recognition

All contributions are valuable and will be acknowledged in the release notes of the corresponding version. Thank you for being part of this community and for helping improve **{{ config.site_name }}**!
