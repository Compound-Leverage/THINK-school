#!/usr/bin/env python3
"""Generate the claude/, openai/, and shared assets/ trees from each team's _source/.

Usage:
    python3 scripts/build_plugins.py --team capture-team|proposal-team|all --check
    python3 scripts/build_plugins.py --team capture-team|proposal-team|all --write

--check renders everything in memory and diffs it against the committed files under
Plugins/<team>/ (assets/, claude/, openai/) without writing anything.
--write renders and overwrites those committed files.

Zip-boundary note (corrected 2026-11-15): OpenAI's submission zip requires the manifest
to resolve inside the zip's one top-level directory -- confirmed by a real rejection in
this repo's history. That boundary is the TEAM folder (Plugins/<team>/), not the platform
folder. The icon and customization/config templates are byte-identical, non-platform-
specific assets, so they now live once at Plugins/<team>/assets/, referenced by relative
path from both plugin.json files ("../assets/...") and from the openai skill content
("../../../assets/..." from openai/skills/<team>/). Building the OpenAI submission zip
must zip Plugins/<team>/ as the top-level directory (openai/ + assets/ together), not
openai/ alone -- see Docs/plugin-validation.md.

Scope note: plugin.json, the shared icon/config assets, and the per-platform README are
unified here -- one value in _source feeds both platform renders. Skill content (SKILL.md
/ reference.md bodies) and the openai master SKILL.md are stored once per platform in
_source and copied out verbatim; they are not yet merged into one shared body, because
today's real content already differs by platform (see roles.yaml comments and the project
plan at /Users/admin/.claude/plans/calm-hatching-bentley.md). This script still gives
those files a single source-of-truth location, and check_build_drift.py still catches it
if the shipped tree is hand-edited without updating _source.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TEAMS = ("capture-team", "proposal-team")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def render_claude_plugin_json(manifest, descriptions):
    c = manifest["claude"]
    data = {
        "name": manifest["name"],
        "displayName": c["display_name"],
        "version": c["version"],
        "icon": "../assets/think-school.png",
        "description": descriptions["long_description"],
        "author": {"name": manifest["author"]["name"], "url": manifest["author"]["url"]},
        "homepage": manifest["shared_urls"]["homepage"],
        "privacyPolicyUrl": manifest["shared_urls"]["privacy_policy"],
        "termsOfServiceUrl": manifest["shared_urls"]["terms_of_service"],
        "supportUrl": c["support_url"],
        "documentationUrl": c["documentation_url"],
        "repository": manifest["repository"],
        "license": manifest["license"],
        "keywords": c["keywords"],
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_openai_plugin_json(manifest, descriptions):
    o = manifest["openai"]
    data = {
        "name": manifest["name"],
        "version": o["version"],
        "description": descriptions["openai_top_level_description"],
        "author": {"name": manifest["author"]["name"], "url": manifest["author"]["url"]},
        "homepage": manifest["shared_urls"]["homepage"],
        "repository": manifest["repository"],
        "license": manifest["license"],
        "keywords": o["keywords"],
        "skills": "./skills",
        "interface": {
            "displayName": o["display_name"],
            "shortDescription": o["short_description"],
            "longDescription": descriptions["long_description"],
            "developerName": o["developer_name"],
            "category": o["category"],
            "capabilities": o["capabilities"],
            "websiteURL": manifest["shared_urls"]["homepage"],
            "supportURL": o["support_url"],
            "customerSupportURL": o["customer_support_url"],
            "privacyPolicyURL": manifest["shared_urls"]["privacy_policy"],
            "termsOfServiceURL": manifest["shared_urls"]["terms_of_service"],
            "brandColor": o["brand_color"],
            "composerIcon": "../assets/think-school.png",
            "logo": "../assets/think-school.png",
            "defaultPrompt": o["default_prompt"],
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def read_text(path):
    return path.read_text(encoding="utf-8")


def read_bytes(path):
    return path.read_bytes()


def render_team(team):
    """Return {relative_path_under_Plugins/<team>: bytes} for every generated file."""
    src = ROOT / "Plugins" / team / "_source"
    manifest = load_yaml(src / "manifest.yaml")
    descriptions = load_yaml(src / "descriptions.yaml")
    roles = load_yaml(src / "roles.yaml")["roles"]

    out = {}

    # plugin.json
    out[f"claude/.claude-plugin/plugin.json"] = render_claude_plugin_json(manifest, descriptions).encode("utf-8")
    out[f"openai/.codex-plugin/plugin.json"] = render_openai_plugin_json(manifest, descriptions).encode("utf-8")

    # icon -> one shared copy at the team level (sibling of claude/ and openai/,
    # inside the zip boundary for OpenAI submission -- see module docstring)
    out["assets/think-school.png"] = read_bytes(src / "icon" / "think-school.png")

    # customization/config templates -> one shared copy at the team level
    cust_dir = src / "customization"
    for f in sorted(cust_dir.iterdir()):
        out[f"assets/{f.name}"] = read_bytes(f)

    # README
    out["claude/README.md"] = read_bytes(src / "readme" / "claude.md")
    out["openai/README.md"] = read_bytes(src / "readme" / "openai.md")

    # openai master SKILL.md (verbatim)
    out[f"openai/skills/{team}/SKILL.md"] = read_bytes(src / "openai_master" / "SKILL.md")

    # per-role skill content (verbatim copy-out per platform)
    for role in roles:
        key = role["key"]
        platforms = role["platforms"]
        role_dir = src / "skills" / key
        if "claude" in platforms:
            out[f"claude/skills/{role['claude_dir']}/SKILL.md"] = read_bytes(role_dir / "claude.md")
        if "openai" in platforms:
            out[f"openai/skills/{team}/references/{role['openai_file']}"] = read_bytes(role_dir / "openai.md")

    return out


def committed_files(team):
    """Return {relative_path: bytes} for every file currently committed under
    Plugins/<team>/ -- assets/ (shared, team-level) plus claude/ and openai/ (platform)."""
    out = {}
    team_root = ROOT / "Plugins" / team
    assets_dir = team_root / "assets"
    if assets_dir.is_dir():
        for p in assets_dir.rglob("*"):
            if p.is_file():
                out[f"assets/{p.relative_to(assets_dir).as_posix()}"] = p.read_bytes()
    for platform in ("claude", "openai"):
        base = team_root / platform
        for p in base.rglob("*"):
            if p.is_file():
                rel = f"{platform}/{p.relative_to(base).as_posix()}"
                out[rel] = p.read_bytes()
    return out


def check_team(team):
    generated = render_team(team)
    committed = committed_files(team)

    gen_keys = set(generated)
    com_keys = set(committed)

    missing = sorted(com_keys - gen_keys)  # committed but generator doesn't produce
    extra = sorted(gen_keys - com_keys)    # generator produces but not committed
    mismatched = sorted(k for k in gen_keys & com_keys if generated[k] != committed[k])

    ok = not missing and not extra and not mismatched
    if not ok:
        print(f"[{team}] DIFF FOUND")
        for k in missing:
            print(f"  MISSING FROM GENERATOR OUTPUT: {k}")
        for k in extra:
            print(f"  EXTRA IN GENERATOR OUTPUT (not committed): {k}")
        for k in mismatched:
            print(f"  CONTENT MISMATCH: {k}")
    else:
        print(f"[{team}] zero diff ({len(generated)} files match)")
    return ok


def write_team(team):
    generated = render_team(team)
    base = ROOT / "Plugins" / team
    for rel, content in generated.items():
        dest = base / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
    print(f"[{team}] wrote {len(generated)} files")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="all", choices=[*TEAMS, "all"])
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = ap.parse_args()

    teams = TEAMS if args.team == "all" else (args.team,)

    if args.check:
        ok = all(check_team(t) for t in teams)
        sys.exit(0 if ok else 1)
    else:
        for t in teams:
            write_team(t)


if __name__ == "__main__":
    main()
