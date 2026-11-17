#!/usr/bin/env python3
"""CI drift check: fail if committed generated platform output no longer
matches what build_plugins.py would generate from _source/.

This is what actually prevents the "same field hand-edited in two plugin.json files"
bug from recurring -- going forward, a field fix happens in _source/, gets regenerated
with `build_plugins.py --write`, and this check confirms the two never drifted apart
again. Does not modify anything; exits non-zero with a report on any mismatch.

Run via: python3 scripts/check_build_drift.py
"""
import sys

from build_plugins import TEAMS, check_team, load_yaml, ROOT


def check_version_parity():
    ok = True
    for team in TEAMS:
        manifest = load_yaml(ROOT / "Plugins" / team / "_source" / "manifest.yaml")
        platform_versions = {
            platform: settings["version"]
            for platform, settings in manifest.items()
            if platform in {"claude", "openai", "microsoft365"}
        }
        if len(set(platform_versions.values())) != 1:
            print(
                f"[{team}] ERROR: platform versions differ: {platform_versions}. "
                "A release must carry one version across its platform packages."
            )
            ok = False
    return ok


def main():
    ok = True
    for team in TEAMS:
        if not check_team(team):
            ok = False
    if not check_version_parity():
        ok = False
    if not ok:
        print(
            "\nDrift detected: committed generated platform content "
            "does not match what build_plugins.py generates from _source/. Either someone "
            "hand-edited the shipped tree directly, or _source/ is out of date. Fix by "
            "editing _source/ and running `python3 scripts/build_plugins.py --write`, "
            "then commit the regenerated diff."
        )
        sys.exit(1)
    print("check_build_drift: PASS -- committed output matches _source/ for all teams")


if __name__ == "__main__":
    main()
