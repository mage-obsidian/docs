from docs_checks.reference import commands, config_paths, env_vars, undocumented


def test_commands_are_read_from_console_classes(docs_tree):
    root = docs_tree({
        "pkg/src/Console/Command/A.php": "<?php $this->setName('mage-obsidian:frontend:config');",
        "pkg/src/Console/Command/B.php": "<?php #[AsCommand(name: 'mage-obsidian:cms:jit')] class B {}",
        "pkg/src/Console/Command/C.php": "<?php protected static $defaultName = 'mage-obsidian:i18n:collect';",
    })
    assert commands([root / "pkg"]) == ["mage-obsidian:cms:jit", "mage-obsidian:frontend:config", "mage-obsidian:i18n:collect"]


def test_config_paths_join_section_group_field(docs_tree):
    root = docs_tree({"pkg/src/etc/adminhtml/system.xml": """<config><system>
<section id="mage_obsidian"><group id="navigation"><field id="retain"/><field id="progress"/></group></section>
</system></config>"""})
    assert config_paths([root / "pkg"]) == ["mage_obsidian/navigation/progress", "mage_obsidian/navigation/retain"]


def test_config_paths_prefer_explicit_config_path(docs_tree):
    root = docs_tree({"pkg/src/etc/adminhtml/system.xml": """<config><system>
<section id="mage_obsidian_frontend">
<group id="speculation"><field id="retain"><config_path>mage_obsidian/navigation/retain</config_path></field><field id="plain"/></group>
<group id="outer"><group id="inner"><field id="deep"/></group></group>
</section>
</system></config>"""})
    assert config_paths([root / "pkg"]) == [
        "mage_obsidian/navigation/retain",
        "mage_obsidian_frontend/outer/inner/deep",
        "mage_obsidian_frontend/speculation/plain",
    ]


def test_env_vars_from_engine_and_sample(docs_tree):
    root = docs_tree({
        "engine/src/cli/build.ts": "const c = process.env.MAGE_OBSIDIAN_BUILD_CONCURRENCY; process.env.NODE_ENV",
        "vite/.env.sample": "VITE_SERVER_HOST=\nVITE_SERVER_PORT=5173\n",
    })
    assert env_vars(root / "engine/src", root / "vite/.env.sample") == [
        "MAGE_OBSIDIAN_BUILD_CONCURRENCY", "VITE_SERVER_HOST", "VITE_SERVER_PORT"]


def test_undocumented_items_are_reported(docs_tree):
    root = docs_tree({"cli.md": "Run `mage-obsidian:frontend:config` to generate."})
    assert undocumented(["mage-obsidian:frontend:config", "mage-obsidian:cms:jit"], root / "cli.md") == ["mage-obsidian:cms:jit"]
