#!/usr/bin/env python3
"""Generate the claude/, openai/, and shared assets/ trees from each team's _source/.

Usage:
    python3 scripts/build_plugins.py --team capture-team|proposal-team|all --check
    python3 scripts/build_plugins.py --team capture-team|proposal-team|all --write

--check renders everything in memory and diffs it against the committed files under
Plugins/<team>/ (assets/, claude/, openai/) without writing anything.
--write renders and overwrites those committed files.

Package-boundary note (corrected 2026-11-15): each platform package must be
self-contained. OpenAI requires the manifest at the plugin root and all declared paths
to stay inside that root with a ./ prefix. Claude's directory likewise requires its
icon inside the Claude plugin root. The source icon and customization templates are
therefore rendered into both openai/assets/ and claude/assets/. Team-level assets/ are
also retained for repository compatibility, but released packages never depend on them.

Scope note: plugin.json, the shared icon/config assets, and the per-platform README are
unified here -- one value in _source feeds both platform renders. The openai master
SKILL.md is still stored once per platform and copied out verbatim -- its content
genuinely differs by platform beyond mechanics (routing table, hoisted rules), see the
project plan at /Users/admin/.claude/plans/calm-hatching-bentley.md.

Per-role skill content (2026-11-15 update): roles with a `body.md` in their
_source/skills/<role>/ directory are "unified" -- one canonical body rendered into both
platforms' shapes (see render_unified_claude_skill / render_unified_openai_reference).
Roles that still have separate claude.md/openai.md files are "legacy" -- copied out
verbatim, unchanged, because their actual content differs between platforms beyond
mechanical formatting (different intro framing, generic role names vs persona names,
selectively combined/dropped Rules bullets) and force-unifying them would silently
change approved, shipped wording on one platform or the other. See
Docs/plugin-content-audit-2026-11-15.md for which roles are which and why.

Cross-team shared content (2026-11-15): Plugins/_shared/ holds content identical across
BOTH teams and BOTH platforms -- not team-specific like _source/, so it isn't duplicated
into each team's own source tree. See shared_resource_discovery(): appended once per
claude role's SKILL.md, hoisted once into each team's openai master SKILL.md.
"""
import argparse
import json
import re
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
        # Directory-only metadata: Claude Code currently warns that it ignores this
        # field, while Anthropic's directory requires it and requires the path to stay
        # inside the plugin root.
        "icon": "./assets/think-school.png",
        "description": descriptions["long_description"],
        "author": {"name": manifest["author"]["name"], "url": manifest["author"]["url"]},
        "homepage": manifest["shared_urls"]["homepage"],
        # Directory-only listing metadata. Released Claude Code builds warn that
        # they ignore these fields, but Anthropic's directory reads all four.
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
            "privacyPolicyURL": manifest["shared_urls"]["privacy_policy"],
            "termsOfServiceURL": manifest["shared_urls"]["terms_of_service"],
            "brandColor": o["brand_color"],
            "composerIcon": "./assets/think-school.png",
            "logo": "./assets/think-school.png",
            "defaultPrompt": o["default_prompt"],
        },
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def read_text(path):
    return path.read_text(encoding="utf-8")


def read_bytes(path):
    return path.read_bytes()


def render_unified_claude_skill(body, meta):
    """Render a unified role's claude.md from its canonical body + meta.

    Canonical body is authored claude-flavored (em dash, no platform path prefix --
    {{ASSETS}} token instead) with an {{INTRO}} token marking wherever the intro
    heading belongs (not always right after frontmatter -- several roles have the
    guardrail section before it). Claude render: frontmatter, {{INTRO}} resolves to
    its heading, {{ASSETS}} resolves to the plugin-root-relative path, the optional
    review-ref sentence token resolves to its claude phrasing, and any other
    per-platform cross-reference token (e.g. {{RESEARCH_REF}} for maya's phase
    pointers, which differ by platform the same way review_ref does -- claude
    references a skill by name, openai by file path) resolves generically.
    """
    text = body.replace("{{INTRO}}", f'## {meta["intro_heading"]}\n\n')
    text = text.replace("{{ASSETS}}", "../../assets")
    if "review_ref" in meta:
        text = text.replace("{{REVIEW_REF_SENTENCE}}", meta["review_ref"]["claude"])
    text = _apply_platform_refs(text, meta, "claude")
    frontmatter = f'---\nname: {meta["claude_name"]}\ndescription: "{meta["claude_description"]}"\n---\n\n'
    return frontmatter + text


def _apply_platform_refs(text, meta, platform):
    """Resolve any {{KEY}} token where meta[key] is a {"claude": ..., "openai": ...}
    dict, other than review_ref (handled separately for backward-compatible naming
    with its existing {{REVIEW_REF_SENTENCE}} token in already-unified roles)."""
    for key, value in meta.items():
        if key == "review_ref" or not isinstance(value, dict):
            continue
        if "claude" in value and "openai" in value:
            text = text.replace("{{" + key.upper() + "}}", value[platform])
    return text


def render_unified_openai_reference(body, meta):
    """Render a unified role's openai reference.md from the same canonical body.

    OpenAI render: H1 title instead of frontmatter, {{INTRO}} resolves to nothing
    (openai doesn't repeat the intro heading -- the H1 already serves that role),
    em dash mechanically rewritten to double-hyphen, {{ASSETS}} resolved to the
    reference-file-relative path (4 levels up from openai/skills/<team>/references/),
    review-ref token resolved to its openai phrasing, and the "No em dashes" rule
    bullet dropped (hoisted once into the team's openai master SKILL.md instead,
    not repeated per role). If a role's only Rules bullet was that one (e.g. blair),
    the now-empty trailing "## Rules" heading is dropped too rather than left dangling.
    """
    text = body.replace("{{INTRO}}", "")
    text = text.replace("—", "--")
    text = text.replace("{{ASSETS}}", "../../../assets")
    if "review_ref" in meta:
        text = text.replace("{{REVIEW_REF_SENTENCE}}", meta["review_ref"]["openai"])
    text = _apply_platform_refs(text, meta, "openai")
    text = re.sub(r"\n- No em dashes in any output\n", "\n", text)
    # If that was the only bullet under a trailing Rules heading (e.g. a role whose
    # claude.md Rules section is only ever the em-dash rule), don't leave an empty
    # heading dangling at the end of the openai render.
    text = re.sub(r"\n## Rules\n\n$", "\n", text)
    return f'# {meta["openai_title"]}\n\n' + text


def shared_resource_discovery():
    """Canonical cross-team, cross-platform resource/capability-discovery snippet.

    Lives at Plugins/_shared/, not under either team's _source/ -- it's identical
    for both plugins, not just both platforms within one plugin. Appended to every
    claude role's SKILL.md and hoisted once into each team's openai master SKILL.md,
    the same way other cross-cutting rules are hoisted vs. repeated per platform.
    """
    return read_text(ROOT / "Plugins" / "_shared" / "resource-discovery.md")


def render_team(team):
    """Return {relative_path_under_Plugins/<team>: bytes} for every generated file."""
    src = ROOT / "Plugins" / team / "_source"
    manifest = load_yaml(src / "manifest.yaml")
    descriptions = load_yaml(src / "descriptions.yaml")
    roles = load_yaml(src / "roles.yaml")["roles"]
    shared_claude = shared_resource_discovery()
    shared_openai = shared_claude.replace("—", "--")

    out = {}

    # plugin.json
    out[f"claude/.claude-plugin/plugin.json"] = render_claude_plugin_json(manifest, descriptions).encode("utf-8")
    out[f"openai/.codex-plugin/plugin.json"] = render_openai_plugin_json(manifest, descriptions).encode("utf-8")

    # Each platform package must carry its own icon inside its plugin root.
    # Keep the team-level copy for repository compatibility.
    icon = read_bytes(src / "icon" / "think-school.png")
    out["assets/think-school.png"] = icon
    out["claude/assets/think-school.png"] = icon
    out["openai/assets/think-school.png"] = icon

    # Customization/config templates are copied inside both platform roots so no
    # released package relies on a path outside its plugin boundary. Keep the
    # team-level copies for direct repository users and backwards compatibility.
    cust_dir = src / "customization"
    for f in sorted(cust_dir.iterdir()):
        content = read_bytes(f)
        out[f"assets/{f.name}"] = content
        out[f"claude/assets/{f.name}"] = content
        out[f"openai/assets/{f.name}"] = content

    # README
    out["claude/README.md"] = read_bytes(src / "readme" / "claude.md")
    out["openai/README.md"] = read_bytes(src / "readme" / "openai.md")

    # openai master SKILL.md (verbatim) + hoisted shared resource-discovery section
    master = read_text(src / "openai_master" / "SKILL.md").rstrip("\n") + "\n\n" + shared_openai
    out[f"openai/skills/{team}/SKILL.md"] = master.encode("utf-8")

    # per-role skill content: unified (one body.md -> both shapes) or legacy
    # (separate claude.md/openai.md, copied out verbatim) -- see module docstring.
    # Every claude role gets the shared resource-discovery section appended, since
    # claude loads one skill at a time with no always-on master to hoist it into.
    for role in roles:
        key = role["key"]
        platforms = role["platforms"]
        role_dir = src / "skills" / key
        body_path = role_dir / "body.md"
        if body_path.exists():
            body = read_text(body_path)
            meta = load_yaml(role_dir / "meta.yaml")
            if "claude" in platforms:
                rendered = render_unified_claude_skill(body, meta).rstrip("\n") + "\n\n" + shared_claude
                out[f"claude/skills/{role['claude_dir']}/SKILL.md"] = rendered.encode("utf-8")
            if "openai" in platforms:
                out[f"openai/skills/{team}/references/{role['openai_file']}"] = render_unified_openai_reference(body, meta).encode("utf-8")
        else:
            if "claude" in platforms:
                rendered = read_text(role_dir / "claude.md").rstrip("\n") + "\n\n" + shared_claude
                out[f"claude/skills/{role['claude_dir']}/SKILL.md"] = rendered.encode("utf-8")
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
