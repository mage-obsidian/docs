import re
import xml.etree.ElementTree as ET
from pathlib import Path

COMMAND = re.compile(r"""(?:setName\(\s*|name:\s*|\$defaultName\s*=\s*)['"](mage-obsidian:[a-z0-9:-]+)['"]""")
ENV = re.compile(r"process\.env\.([A-Z][A-Z0-9_]+)")
IGNORED_ENV = {"NODE_ENV", "PATH", "HOME", "CI"}


def commands(packages_dirs):
    found = set()
    for package in packages_dirs:
        for php in Path(package).rglob("Console/Command/*.php"):
            found.update(COMMAND.findall(php.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)


def _group_fields(group, prefix):
    for field in group.findall("field"):
        yield field.findtext("config_path") or f'{prefix}/{group.get("id")}/{field.get("id")}'
    for child in group.findall("group"):
        yield from _group_fields(child, f'{prefix}/{group.get("id")}')


def config_paths(packages_dirs):
    found = set()
    for package in packages_dirs:
        for xml in Path(package).rglob("etc/adminhtml/system.xml"):
            root = ET.parse(xml).getroot()
            for section in root.iter("section"):
                for group in section.findall("group"):
                    found.update(_group_fields(group, section.get("id")))
    return sorted(found)


def env_vars(engine_src, env_sample):
    found = set()
    for source in Path(engine_src).rglob("*.ts"):
        found.update(ENV.findall(source.read_text(encoding="utf-8", errors="ignore")))
    for line in Path(env_sample).read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            found.add(line.split("=", 1)[0].strip())
    return sorted(found - IGNORED_ENV)


def undocumented(items, page):
    text = Path(page).read_text(encoding="utf-8")
    return [item for item in items if f"`{item}`" not in text]


def run(args):
    framework, storefront, docs = (Path(a) for a in args)
    packages = [*Path(framework, "packages").iterdir(), *Path(storefront, "packages").iterdir()]
    reference = Path(docs, "reference")
    engine = Path(framework, "packages/js-package-utils/src")
    sample = Path(framework, "packages/component-modern-frontend/vite/.env.sample")
    findings = [f"cli.md: {c}" for c in undocumented(commands(packages), reference / "cli.md")]
    findings += [f"config-paths.md: {p}" for p in undocumented(config_paths(packages), reference / "config-paths.md")]
    findings += [f"env.md: {v}" for v in undocumented(env_vars(engine, sample), reference / "env.md")]
    return findings
