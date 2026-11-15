#!/usr/bin/env python3
"""Build the OpenAI submission zip for one or both teams.

Usage:
    python3 scripts/build_openai_zip.py --team capture-team|proposal-team|all

Zip-boundary requirement (see Docs/plugin-validation.md "OpenAI submission zip
boundary"): the archive's single top-level <team>/ directory is the plugin root.
It directly contains .codex-plugin/, skills/, assets/, and README.md. Every declared
path starts with ./ and remains inside that root.

Output: openai-plugin/<team>.zip (gitignored, locally-built, not committed).
"""
import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAMS = ("capture-team", "proposal-team")


def validate_staging(team, staging):
    manifest_path = staging / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise ValueError(f"[{team}] manifest is not at the staged plugin root")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != team:
        raise ValueError(f"[{team}] manifest name mismatch")
    if not any((staging / "skills").rglob("SKILL.md")):
        raise ValueError(f"[{team}] staged package has no skill")
    for field in ("composerIcon", "logo"):
        value = manifest.get("interface", {}).get(field, "")
        if not isinstance(value, str) or not value.startswith("./") or ".." in Path(value).parts:
            raise ValueError(f"[{team}] unsafe {field} path: {value!r}")
        target = (staging / value).resolve()
        if not target.is_relative_to(staging.resolve()) or not target.is_file():
            raise ValueError(f"[{team}] missing in-package {field}: {value}")


def build_zip(team):
    team_src = ROOT / "Plugins" / team
    out_path = ROOT / "openai-plugin" / f"{team}.zip"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / team
        shutil.copytree(team_src / "openai", staging)
        validate_staging(team, staging)

        if out_path.exists():
            out_path.unlink()
        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(staging.rglob("*")):
                if f.is_file():
                    zf.write(f, f.relative_to(Path(tmp)))

    print(f"[{team}] wrote {out_path.relative_to(ROOT)} ({out_path.stat().st_size:,} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="all", choices=[*TEAMS, "all"])
    args = ap.parse_args()
    teams = TEAMS if args.team == "all" else (args.team,)
    for t in teams:
        build_zip(t)


if __name__ == "__main__":
    main()
