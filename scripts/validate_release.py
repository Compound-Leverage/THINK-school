#!/usr/bin/env python3
"""Static release checks for THINK School marketplaces and local documentation."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

ROOT = Path(__file__).resolve().parents[1]
errors = []
package_versions = {}
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
            version = details.get("version")
            require(isinstance(version, str) and bool(version), f"{meta}: missing version")
            package_versions[(name, platform)] = version
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
        for skill in package.rglob("SKILL.md"):
            skill_content = skill.read_text(encoding="utf-8")
            require("Shipley" not in skill_content,
                    f"{skill}: contains unnecessary third-party branding: Shipley")
        forbidden_runtime_content = {
            "https://www.compoundleverage.com/content.md": "dynamic external instruction index",
            "https://www.compoundleverage.com/managed-teams-plans/": "undisclosed promotional offer",
            "https://www.skool.com/": "undisclosed third-party promotion",
            "https://www.shipleywins.com/": "external third-party reference",
        }
        for skill in package.rglob("SKILL.md"):
            skill_content = skill.read_text(encoding="utf-8")
            for forbidden, reason in forbidden_runtime_content.items():
                require(forbidden not in skill_content,
                        f"{skill}: contains {reason}: {forbidden}")

# Each team release is one cross-platform capability release. Provider review timing
# may differ, but package versions and declared capabilities may not drift.
for team in ("capture-team", "proposal-team"):
    claude_version = package_versions.get((team, "claude"))
    openai_version = package_versions.get((team, "openai"))
    require(claude_version == openai_version,
            f"{team}: Claude version {claude_version!r} != OpenAI version {openai_version!r}")

    manifest_source = yaml.safe_load(
        (ROOT / "Plugins" / team / "_source" / "manifest.yaml").read_text(encoding="utf-8")
    )
    if "microsoft365" in manifest_source:
        microsoft365_version = manifest_source["microsoft365"].get("version")
        require(microsoft365_version == claude_version,
                f"{team}: Microsoft 365 version {microsoft365_version!r} != Claude/OpenAI {claude_version!r}")

    contract_path = ROOT / "Plugins" / team / "_source" / "capabilities.yaml"
    try:
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        capabilities = contract["capabilities"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"{contract_path}: invalid capability contract: {exc}")
        continue
    ids = [item.get("id") for item in capabilities if isinstance(item, dict)]
    require(len(ids) == len(set(ids)) and all(ids), f"{contract_path}: capability ids must be unique")
    for capability in capabilities:
        capability_id = capability.get("id", "<missing>")
        platforms = ["claude", "openai"]
        if (ROOT / "Plugins" / team / "microsoft365").is_dir():
            platforms.append("microsoft365")
        for platform in platforms:
            evidence = capability.get(platform, {})
            rel = evidence.get("path", "") if isinstance(evidence, dict) else ""
            marker = evidence.get("marker", "") if isinstance(evidence, dict) else ""
            target = ROOT / "Plugins" / team / platform / rel
            require(bool(rel) and bool(marker),
                    f"{contract_path}: {capability_id} missing {platform} evidence")
            if target.is_file() and marker:
                require(marker in target.read_text(encoding="utf-8"),
                        f"{target}: missing {capability_id} marker {marker!r}")
            else:
                require(False, f"{target}: missing capability evidence file")

# Microsoft 365 Copilot is an app package: manifest and referenced agent/skill files
# must stay inside the package, icons must have exact dimensions (checked by PNG IHDR),
# and the generic public package must not request write-capable email access.
import struct
def png_size(path):
    with path.open("rb") as stream:
        header = stream.read(24)
    require(header[:8] == b"\x89PNG\r\n\x1a\n", f"{path}: not a PNG")
    return struct.unpack(">II", header[16:24])

for team in ("capture-team", "proposal-team"):
    m365 = ROOT / "Plugins" / team / "microsoft365"
    if not m365.is_dir():
        continue
    try:
        app = json.loads((m365 / "manifest.json").read_text(encoding="utf-8"))
        agent = json.loads((m365 / "declarativeAgent.json").read_text(encoding="utf-8"))
        require(app.get("manifestVersion") == "1.30", f"{team}: Microsoft 365 app manifest must use 1.30")
        require(agent.get("version") == "v1.9", f"{team}: Microsoft 365 declarative agent must use v1.9")
        agent_ref = app["copilotAgents"]["declarativeAgents"][0]
        require(agent_ref.get("file") == "declarativeAgent.json", f"{team}: Microsoft 365 agent reference mismatch")
        skill_refs = agent.get("agent_skills", [])
        require(0 < len(skill_refs) <= 8, f"{team}: Microsoft 365 agent must reference 1-8 skills")
        for skill_ref in skill_refs:
            folder = skill_ref.get("folder", "")
            require(folder.startswith("./") and ".." not in Path(folder).parts,
                    f"{team}: Microsoft 365 unsafe skill path: {folder}")
            require((m365 / folder / "SKILL.md").is_file(),
                    f"{team}: Microsoft 365 missing skill: {folder}/SKILL.md")
        require(len(agent.get("instructions", "")) <= 8000,
                f"{team}: Microsoft 365 instructions exceed 8,000 characters")
        capability_names = {item.get("name") for item in agent.get("capabilities", [])}
        require("EmailActions" not in capability_names,
                f"{team}: generic Microsoft 365 package must not enable EmailActions")
        require(png_size(m365 / "color.png") == (192, 192), f"{team}: Microsoft 365 color icon must be 192x192")
        require(png_size(m365 / "outline.png") == (32, 32), f"{team}: Microsoft 365 outline icon must be 32x32")
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        errors.append(f"{team}: Microsoft 365 package invalid: {exc}")

try:
    claude_marketplace_version = json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
    )["metadata"]["version"]
    released_versions = {v for v in package_versions.values() if v}
    require(released_versions == {claude_marketplace_version},
            f"marketplace/package versions differ: {sorted(released_versions)} vs {claude_marketplace_version}")
except (OSError, ValueError, KeyError, TypeError) as exc:
    errors.append(f".claude-plugin/marketplace.json: invalid metadata.version: {exc}")

require(not (ROOT / "Archive").exists(), "Archive/ must remain on legacy-archive branch")

# Validate links in the actively maintained navigation and quickstart docs.
docs = [
    "README.md", "Marketplaces/README.md", "Plugins/README.md",
    "Docs/repo-map.md", "Docs/quickstart-capture.md",
    "Docs/quickstart-proposal.md", "Docs/plugin-validation.md",
    "Docs/distribution-and-release.md",
    "Docs/microsoft365-copilot.md",
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
