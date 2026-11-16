# Release notes: v1.2.0 package parity and autonomous reporting

Release date: 2026-11-16

## What changed

- Added a Claude Capture Team orchestrator so the Claude package can run the same
  discovery-to-brief autonomous workflow as the OpenAI team skill.
- Added a shared autonomous-reporting contract to Capture and Proposal on both
  platforms. A completed run reports outputs, evidence, assumptions, gaps, risks,
  blockers, next actions, and required approvals without claiming unconfigured
  background or scheduled execution.
- Added per-team capability contracts and made Claude/OpenAI version drift a release
  failure.
- Added a four-package release builder with commit provenance, checksums, and extracted
  byte-for-byte validation.
- Extended CI to validate pull requests into Staging as well as main and upload the
  complete cross-platform package set.
- Documented direct-install, repository-marketplace, OpenAI directory, and Anthropic
  directory update behavior and manual gates.

## Validation evidence

- `scripts/build_plugins.py --team all --check`: zero diff for both teams.
- `scripts/validate_release.py`: passed metadata, version, capability, package, and
  documentation validation.
- `scripts/check_build_drift.py`: passed for both teams.
- `scripts/build_release_packages.py`: built and re-extracted all four v1.2.0 archives;
  extracted file checksums matched the committed generated packages.
- Claude Code 2.1.215, isolated configuration: validated both package roots and the
  marketplace, then installed Capture Team v1.2.0 and Proposal Team v1.2.0. Claude
  discovered 4 Capture skills and 8 Proposal skills. Directory-only metadata produced
  the expected non-fatal Claude Code warnings.
- Codex CLI 0.167.0, isolated configuration: added the repository marketplace, listed
  both v1.2.0 packages, installed both, and confirmed both enabled from the isolated
  cache.

These tests validate generated archives and direct/repository marketplace installs.
They do not establish that v1.2.0 is live in either provider's public directory.

## Publication requirements

- OpenAI: upload each v1.2.0 OpenAI archive to its existing public plugin, complete
  automated checks and any review, then publish the approved package. On the validation
  date, the signed-in catalog still served v1.1.20 for both public listings.
- Anthropic: each Claude package is a separate directory submission. Complete or update
  its developer-portal submission, validation, review, and publication. Whether later
  versions auto-publish depends on the portal's assigned publish setting.

Use [distribution and release parity](distribution-and-release.md) for the maintained
release procedure and update matrix.
