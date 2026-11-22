# Release notes: v1.3.0 Microsoft 365 Copilot package

Date: November 17, 2026

## Capture Team

- Added an installable Microsoft 365 Copilot app-package source using app manifest
  v1.30 and declarative agent manifest v1.9.
- Packaged the shared Capture Team workflow as a Microsoft 365 Agent Skill rather than
  creating a separate customer-specific prompt fork.
- Added configurable pursuit types for business development, government contracting,
  grant funding, and membership development.
- Added a private tenant-package builder that can scope SharePoint, Teams, read-only
  Outlook, People, and web knowledge. The builder rejects unresolved placeholders,
  unscoped email access, and unsupported configuration overrides.
- Added Microsoft 365 icon, path, version, capability, and human-approval validation.
- Added deployment, licensing, reporting, scheduling, governance, and administrator
  prerequisite documentation.

## Cross-platform parity

Claude, OpenAI, and Microsoft 365 Capture Team packages are generated from the same
canonical `_source/` content and carry version 1.3.0. Proposal Team's Claude and OpenAI
packages were regenerated at the repository release version without functional content
changes.

## Validation evidence

The following passed locally on November 17, 2026:

- `python3 scripts/validate_release.py`
- `python3 scripts/check_build_drift.py`
- `python3 scripts/build_release_packages.py --output-dir <temporary directory>`
- Generic and configured manifests against Microsoft's downloaded app-manifest v1.30
  and declarative-agent v1.9 JSON schemas
- ZIP re-extraction and exact committed-package byte comparison

The release builder produced five archives, including an installable
`capture-team-microsoft365-v1.3.0.zip` with `manifest.json` at its root.

## Not yet validated or published

- No package has been uploaded to or installed in a customer tenant.
- Microsoft Validation Layer and live Microsoft 365 Copilot behavior remain tenant
  acceptance gates.
- SharePoint, Teams, Outlook, and People access remain disabled in the generic package.
- No Microsoft Marketplace or organization-catalog publication has occurred.
