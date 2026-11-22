#!/usr/bin/env python3
"""Build versioned, checksum-pinned release bundles for supported platforms.

Every archive is copied from the committed generated package directory used by the
repository marketplace. The same bytes therefore back direct installs and provider
submissions; provider-specific package shapes remain separate.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

import yaml

from build_plugins import render_team

ROOT = Path(__file__).resolve().parents[1]
TEAMS = ("capture-team", "proposal-team")
PLATFORMS_BY_TEAM = {
    "capture-team": ("claude", "openai", "microsoft365"),
    "proposal-team": ("claude", "openai", "microsoft365"),
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_commit():
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def team_version(team):
    manifest = yaml.safe_load(
        (ROOT / "Plugins" / team / "_source" / "manifest.yaml").read_text(encoding="utf-8")
    )
    versions = {manifest[platform]["version"] for platform in PLATFORMS_BY_TEAM[team]}
    if len(versions) != 1:
        raise ValueError(f"{team}: platform versions differ: {sorted(versions)}")
    return versions.pop()


def build_archive(team, platform, version, output_dir):
    package = ROOT / "Plugins" / team / platform
    generated = {
        Path(path).relative_to(platform): content
        for path, content in render_team(team).items()
        if path.startswith(f"{platform}/")
    }
    committed = {
        path.relative_to(package): path.read_bytes()
        for path in package.rglob("*") if path.is_file()
    }
    if generated != committed:
        missing = sorted(str(path) for path in generated.keys() - committed.keys())
        extra = sorted(str(path) for path in committed.keys() - generated.keys())
        changed = sorted(
            str(path) for path in generated.keys() & committed.keys()
            if generated[path] != committed[path]
        )
        raise ValueError(
            f"{package}: generated-package drift; missing={missing}, "
            f"extra={extra}, changed={changed}"
        )
    if platform == "microsoft365":
        metadata = package / "manifest.json"
    else:
        metadata = package / (".claude-plugin/plugin.json" if platform == "claude" else ".codex-plugin/plugin.json")
    details = json.loads(metadata.read_text(encoding="utf-8"))
    if details.get("version") != version:
        raise ValueError(f"{metadata}: expected version {version}")
    if not any(package.rglob("SKILL.md")):
        raise ValueError(f"{package}: no skills")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{team}-{platform}-v{version}.zip"
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for item in sorted(package.rglob("*")):
            if item.is_file():
                archive_path = item.relative_to(package)
                if platform != "microsoft365":
                    archive_path = Path(team) / archive_path
                bundle.write(item, archive_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(temp_dir)
        extracted = Path(temp_dir) if platform == "microsoft365" else Path(temp_dir) / team
        original_files = {
            p.relative_to(package): sha256(p) for p in package.rglob("*") if p.is_file()
        }
        extracted_files = {
            p.relative_to(extracted): sha256(p) for p in extracted.rglob("*") if p.is_file()
        }
        if original_files != extracted_files:
            raise ValueError(f"{archive}: extracted content differs from {package}")
    return archive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "release-packages")
    args = parser.parse_args()
    versions = {team: team_version(team) for team in TEAMS}
    if len(set(versions.values())) != 1:
        raise ValueError(f"team release versions differ: {versions}")

    records = []
    for team in TEAMS:
        for platform in PLATFORMS_BY_TEAM[team]:
            archive = build_archive(team, platform, versions[team], args.output_dir)
            records.append({
                "team": team,
                "platform": platform,
                "version": versions[team],
                "archive": archive.name,
                "sha256": sha256(archive),
            })
            print(f"[{team}/{platform}] {archive} ({archive.stat().st_size:,} bytes)")

    manifest = {
        "schema_version": 1,
        "version": next(iter(versions.values())),
        "source_commit": source_commit(),
        "packages": records,
    }
    manifest_path = args.output_dir / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"release manifest: {manifest_path}")


if __name__ == "__main__":
    main()
