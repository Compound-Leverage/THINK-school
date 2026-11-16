#!/usr/bin/env python3
"""Static release checks for THINK School marketplaces and local documentation."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
def require(condition, message):
    if not condition:
        errors.append(message)

for manifest, platform, metadata in [
    (".claude-plugin/marketplace.json", "claude", ".claude-plugin/plugin.json"),
    (".agents/plugins/marketplace.json", "openai", ".codex-plugin/plugin.json"),
]:
    file = ROOT / manifest
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
        plugins = data["plugins"]
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f"{manifest}: cannot read marketplace: {exc}")
        continue
    names = [p.get("name") for p in plugins]
    require(sorted(names) == ["capture-team", "proposal-team"], f"{manifest}: expected Capture and Proposal only")
    for plugin in plugins:
        name = plugin.get("name", "")
        source = plugin.get("source", "")
        if isinstance(source, dict):
            source = source.get("path", "")
        require(isinstance(source, str) and source.startswith("./"), f"{manifest}: invalid source for {name}")
        if not isinstance(source, str) or not source.startswith("./"):
            continue
        expected = f"./Plugins/{name}/{platform}"
        require(source.rstrip("/") == expected, f"{manifest}: {name} points to {source}, expected {expected}")
        package = ROOT / source
        require(package.is_dir(), f"{manifest}: missing package {source}")
        meta = package / metadata
        try:
            details = json.loads(meta.read_text(encoding="utf-8"))
            require(details.get("name") == name, f"{meta}: name mismatch")
            if platform == "claude":
                icon = details.get("icon", "")
                require(isinstance(icon, str) and bool(icon), f"{meta}: missing directory icon")
                if isinstance(icon, str) and icon:
                    require(not Path(icon).is_absolute() and ".." not in Path(icon).parts,
                            f"{meta}: icon must stay inside plugin root: {icon}")
                    icon_file = (package / icon).resolve()
                    require(icon_file.is_relative_to(package.resolve()) and icon_file.is_file(),
                            f"{meta}: missing in-root icon: {icon}")
            else:
                policy = plugin.get("policy", {})
                require(bool(policy.get("authentication")),
                        f"{manifest}: {name} missing policy.authentication")
                for field in ("skills",):
                    value = details.get(field, "")
                    require(isinstance(value, str) and value.startswith("./") and ".." not in Path(value).parts,
                            f"{meta}: unsafe {field} path: {value}")
                    if isinstance(value, str) and value.startswith("./"):
                        target = (package / value).resolve()
                        require(target.is_relative_to(package.resolve()) and target.is_dir(),
                                f"{meta}: missing in-root {field}: {value}")
                interface = details.get("interface", {})
                require(isinstance(interface, dict), f"{meta}: missing interface object")
                if isinstance(interface, dict):
                    for field, limit in (
                        ("displayName", 30),
                        ("shortDescription", 30),
                        ("longDescription", 4000),
                        ("developerName", 80),
                    ):
                        value = interface.get(field, "")
                        require(isinstance(value, str) and bool(value.strip()),
                                f"{meta}: missing interface.{field}")
                        if isinstance(value, str):
                            require(len(value) <= limit,
                                    f"{meta}: interface.{field} exceeds {limit} characters")
                    short_description = interface.get("shortDescription", "")
                    if isinstance(short_description, str):
                        require("\n" not in short_description and "\r" not in short_description,
                                f"{meta}: interface.shortDescription must fit on one line")
                for field in ("composerIcon", "logo"):
                    value = interface.get(field, "") if isinstance(interface, dict) else ""
                    require(isinstance(value, str) and value.startswith("./") and ".." not in Path(value).parts,
                            f"{meta}: unsafe {field} path: {value}")
                    if isinstance(value, str) and value.startswith("./"):
                        target = (package / value).resolve()
                        require(target.is_relative_to(package.resolve()) and target.is_file(),
                                f"{meta}: missing in-root {field}: {value}")
        except (OSError, ValueError) as exc:
            errors.append(f"{meta}: invalid plugin metadata: {exc}")
        require(any(package.rglob("SKILL.md")), f"{package}: no SKILL.md")

require(not (ROOT / "Archive").exists(), "Archive/ must remain on legacy-archive branch")

# Validate links in the actively maintained navigation and quickstart docs.
docs = [
    "README.md", "Marketplaces/README.md", "Plugins/README.md",
    "Docs/repo-map.md", "Docs/quickstart-capture.md",
    "Docs/quickstart-proposal.md", "Docs/plugin-validation.md",
    "Docs/samples/capture-brief.md", "Docs/samples/proposal-discovery-brief.md",
]
pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
for name in docs:
    file = ROOT / name
    if not file.is_file():
        errors.append(f"missing documentation: {name}")
        continue
    content = file.read_text(encoding="utf-8")
    for raw in pattern.findall(content):
        target = raw.split("#", 1)[0].strip().split(" ", 1)[0]
        if not target or target.startswith(("https://", "http://", "mailto:", "/")):
            continue
        dest = (file.parent / unquote(target)).resolve()
        require(dest.is_relative_to(ROOT) and dest.exists(), f"{name}: broken link {raw}")

if errors:
    print("FAIL: " + str(len(errors)) + " release checks")
    for error in errors:
        print(" - " + error)
    sys.exit(1)
print("PASS: marketplace manifests, package metadata, skill files, and key documentation links")
