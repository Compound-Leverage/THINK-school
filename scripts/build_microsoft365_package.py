#!/usr/bin/env python3
"""Build a private, tenant-configured Microsoft 365 Copilot app package.

The public repository package stays organization-neutral. This builder injects only
explicitly approved tenant scopes and writes the configured ZIP to an output directory.
"""
import argparse
import json
import re
import zipfile
from pathlib import Path
from urllib.parse import urlparse

from build_plugins import ROOT, render_team


def fail(message):
    raise ValueError(message)


def has_placeholder(value):
    if isinstance(value, str):
        return "[" in value or "]" in value
    if isinstance(value, list):
        return any(has_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(has_placeholder(item) for item in value.values())
    return False


def require_https(url, label):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{label} must be an absolute HTTPS URL: {url!r}")


def build_capabilities(config):
    knowledge = config.get("knowledge", {})
    capabilities = []
    if knowledge.get("web_search", True):
        capabilities.append({"name": "WebSearch"})

    sharepoint_urls = knowledge.get("sharepoint_urls", [])
    for url in sharepoint_urls:
        require_https(url, "SharePoint source")
    if sharepoint_urls:
        capabilities.append({
            "name": "OneDriveAndSharePoint",
            "items_by_url": [{"url": url} for url in sharepoint_urls],
        })

    teams_urls = knowledge.get("teams_urls", [])
    for url in teams_urls:
        require_https(url, "Teams source")
    if len(teams_urls) > 5:
        fail("Microsoft 365 supports at most five scoped Teams URLs per agent")
    if teams_urls:
        capabilities.append({
            "name": "TeamsMessages",
            "urls": [{"url": url} for url in teams_urls],
        })

    email = knowledge.get("email", {})
    if email.get("enabled"):
        capability = {"name": "Email"}
        shared_mailbox = email.get("shared_mailbox", "").strip()
        group_mailboxes = email.get("group_mailboxes", [])
        folders = email.get("folders", [])
        if not (shared_mailbox or group_mailboxes or folders):
            fail("Email must be scoped to an approved mailbox, group mailbox, or folder")
        if shared_mailbox:
            capability["shared_mailbox"] = shared_mailbox
        if group_mailboxes:
            if len(group_mailboxes) > 25:
                fail("Microsoft 365 supports at most 25 group mailboxes")
            capability["group_mailboxes"] = group_mailboxes
        if folders:
            capability["folders"] = [{"folder_id": folder} for folder in folders]
        capabilities.append(capability)

    people = knowledge.get("people", {})
    if people.get("enabled"):
        capabilities.append({
            "name": "People",
            "include_related_content": bool(people.get("include_related_content", False)),
        })

    if not capabilities:
        fail("Enable at least one approved knowledge capability")
    return capabilities


def configured_package(config):
    if has_placeholder(config):
        fail("Replace or remove every bracketed placeholder before building")
    organization = config.get("organization", {})
    org_name = organization.get("name", "").strip()
    owner = organization.get("owner", "").strip()
    pursuit_type = config.get("active_pursuit_type", "").strip()
    if not org_name or not owner or not pursuit_type:
        fail("organization.name, organization.owner, and active_pursuit_type are required")

    rendered = {
        Path(name).relative_to("microsoft365").as_posix(): content
        for name, content in render_team("capture-team").items()
        if name.startswith("microsoft365/")
    }
    app = json.loads(rendered["manifest.json"])
    agent = json.loads(rendered["declarativeAgent.json"])
    capture_config_path = "skills/capture-team/assets/my-capture-config.json"
    capture_config = json.loads(rendered[capture_config_path])

    agent_config = config.get("agent", {})
    short_name = agent_config.get("short_name", "Capture Team").strip()
    name = agent_config.get("name", app["name"]["full"]).strip()
    description = agent_config.get("description", agent["description"]).strip()
    if len(short_name) > 30:
        fail("agent.short_name must be 30 characters or fewer")
    if len(name) > 100:
        fail("agent.name must be 100 characters or fewer")
    if len(description) > 1000:
        fail("agent.description must be 1,000 characters or fewer")

    app["name"] = {"short": short_name, "full": name}
    agent["name"] = name
    agent["description"] = description
    agent["capabilities"] = build_capabilities(config)
    capture_config["organization"] = {
        "name": org_name,
        "business_owner": owner,
    }
    capture_config["pursuit_types"]["active"] = pursuit_type
    allowed_overrides = {
        "capability_map", "scanning", "qualification_profiles", "routing_flags",
        "notion", "enrichment", "delivery", "brief_structure",
    }
    for key, value in config.get("capture_config", {}).items():
        if key not in allowed_overrides:
            fail(f"capture_config override is not allowed for key: {key}")
        capture_config[key] = value

    rendered["manifest.json"] = (json.dumps(app, indent=2) + "\n").encode()
    rendered["declarativeAgent.json"] = (json.dumps(agent, indent=2) + "\n").encode()
    rendered[capture_config_path] = (json.dumps(capture_config, indent=2) + "\n").encode()
    return rendered


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "release-packages")
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    package = configured_package(config)
    slug = re.sub(r"[^a-z0-9]+", "-", config["organization"]["name"].lower()).strip("-")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = args.output_dir / f"capture-team-microsoft365-{slug}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(package.items()):
            bundle.writestr(name, content)
    if archive.stat().st_size > 10 * 1024 * 1024:
        archive.unlink()
        fail("Microsoft 365 app package exceeds the 10 MB limit")
    print(archive)


if __name__ == "__main__":
    main()
