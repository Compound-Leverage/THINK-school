# Release notes: v1.4.0 Microsoft 365 Copilot package for Proposal Team

Date: November 21, 2026

## Proposal Team

- Added an installable Microsoft 365 Copilot app-package source using app manifest
  v1.30 and declarative agent manifest v1.9, matching Capture Team's existing
  packaging model.
- Packaged the shared Proposal Team workflow (Intake, Research, Assessment, Strategy,
  Draft, QA/Review, Output) as a Microsoft 365 Agent Skill, reusing all eight role
  reference files generated for the OpenAI package.
- Added Microsoft 365 icon, path, version, capability, and human-approval validation
  for Proposal Team alongside Capture Team's existing checks.
- Added deployment, licensing, reporting, scheduling, governance, and administrator
  prerequisite documentation covering both teams.

## Generator generalization (Capture Team unaffected)

Three Capture-Team-specific assumptions were generalized so the Microsoft 365 render
path works for any team whose `_source/manifest.yaml` declares a `microsoft365` block:

- `scripts/build_plugins.py`: the declarative agent id, skill folder, and disclaimer
  text now come from `manifest.yaml`'s `microsoft365.agent_id` / `disclaimer` fields
  instead of being hardcoded to Capture Team's values. The per-skill configuration copy
  now loops over every file in `_source/customization/`, matching the existing
  Claude/OpenAI asset loop, instead of copying a single hardcoded filename.
- `scripts/validate_release.py`: Microsoft 365 structural validation (manifest version,
  declarative agent version, skill references, instruction length, icon dimensions, no
  `EmailActions`) now loops over every team with a `Plugins/<team>/microsoft365/`
  directory instead of checking only Capture Team's.
- `scripts/build_release_packages.py`: `PLATFORMS_BY_TEAM` now includes `microsoft365`
  for Proposal Team.

Capture Team's generated output is byte-for-byte unchanged by this generalization
(`check_build_drift.py` confirms zero drift) -- the previously hardcoded values were
moved into `Plugins/capture-team/_source/manifest.yaml` rather than changed.

`scripts/build_microsoft365_package.py` (the private, tenant-configured package
builder) remains Capture Team-only. Its config schema (`active_pursuit_type`, the
`capture_config` override allowlist) matches Capture Team's single configuration file;
Proposal Team's five separate configuration files have no equivalent "active mode"
selector, so deciding which of their fields are safe tenant overrides is a deferred
product decision, not a mechanical rename. The generic, organization-neutral Microsoft
365 package for Proposal Team is unaffected by this limitation.

Deferred integration points (Managed Teams MCP connector, OAuth, customer Brain, work
wallet) are documented, not implemented -- see
[Microsoft 365 Copilot distribution and governance](microsoft365-copilot.md#deferred-integration-points-not-implemented).

## Cross-platform parity

Claude, OpenAI, and Microsoft 365 packages for both Capture Team and Proposal Team are
generated from the same canonical `_source/` content and carry version 1.4.0.

## Validation evidence

The following passed locally on November 21, 2026:

- `python3 scripts/build_plugins.py --team all --check`
- `python3 scripts/validate_release.py`
- `python3 scripts/check_build_drift.py`
- `python3 scripts/build_release_packages.py --output-dir <temporary directory>`
- Generated Proposal Team manifests checked against the same app-manifest v1.30 and
  declarative-agent v1.9 structural rules already enforced for Capture Team
- ZIP re-extraction and exact committed-package byte comparison for all six archives

The release builder produced six archives, including an installable
`proposal-team-microsoft365-v1.4.0.zip` with `manifest.json` at its root.

## Not yet validated or published

- No package has been uploaded to or installed in a customer tenant.
- Microsoft Validation Layer and live Microsoft 365 Copilot behavior remain tenant
  acceptance gates for both teams.
- SharePoint, Teams, Outlook, and People access remain disabled in both generic
  packages.
- No Microsoft Marketplace or organization-catalog publication has occurred.
- A private tenant-package builder for Proposal Team does not exist yet (see above).
