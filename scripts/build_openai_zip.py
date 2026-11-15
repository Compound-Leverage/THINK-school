#!/usr/bin/env python3
"""Build the OpenAI submission zip for one or both teams.

Usage:
    python3 scripts/build_openai_zip.py --team capture-team|proposal-team|all

Zip-boundary requirement (see Docs/plugin-validation.md "OpenAI submission zip
boundary"): Plugins/<team>/openai/.codex-plugin/plugin.json references the shared
icon/config templates one level up, at Plugins/<team>/assets/ -- a sibling of
openai/, not a child of it. OpenAI's upload has rejected a zip before with "Plugin
manifest not found... at the ZIP root or inside its only top-level directory" when
the manifest referenced a path outside the zipped folder. The zip's single
top-level directory must therefore contain openai/ and assets/ together -- not
claude/ or _source/, which aren't part of the OpenAI submission at all.

Output: openai-plugin/<team>.zip (gitignored, locally-built, not committed).
"""
import argparse
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEAMS = ("capture-team", "proposal-team")


def build_zip(team):
    team_src = ROOT / "Plugins" / team
    out_path = ROOT / "openai-plugin" / f"{team}.zip"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / team
        shutil.copytree(team_src / "openai", staging / "openai")
        shutil.copytree(team_src / "assets", staging / "assets")

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
