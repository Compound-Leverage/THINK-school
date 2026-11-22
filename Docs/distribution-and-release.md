# Distribution and release parity

Each Managed Team ships as one functional release across its supported package shapes.
Capture Team and Proposal Team both support Claude, OpenAI, and Microsoft 365 Copilot.
Platform syntax may differ, but a team's declared capabilities and version must match
across its packages.

## Build architecture

`Plugins/<team>/_source/` is the canonical source. Run:

```bash
python3 scripts/build_plugins.py --team all --write
python3 scripts/validate_release.py
python3 scripts/check_build_drift.py
python3 scripts/build_release_packages.py
```

The generator writes `Plugins/<team>/claude/`, `Plugins/<team>/openai/`, and
`Plugins/<team>/microsoft365/` for every team whose `_source/manifest.yaml` declares a
`microsoft365` block (Capture Team and Proposal Team, currently). Repository
marketplaces install the Claude and OpenAI directories. `build_release_packages.py`
archives the generated
directories for provider or tenant submission and writes `release-manifest.json` with
the source commit and SHA-256 checksum of every archive. Do not hand-edit a
generated package or build a provider upload from another directory.

Each team's `_source/capabilities.yaml` is the release contract. CI verifies that every
declared capability has evidence in every supported rendered package, that platform
versions match, that the Claude marketplace catalog carries that same release version,
and that each archive extracts to the exact committed package bytes.

## Update behavior by distribution path

| Distribution path | What a repository release changes | What is automatic | What remains manual |
|---|---|---|---|
| OpenAI repo marketplace / direct source | A push updates the Git source used by the marketplace. | Nothing should be assumed for an existing cached install. | Refresh the marketplace with `codex plugin marketplace upgrade` and install or update the plugin in a supported client. A folder or ZIP loaded directly must be replaced manually. |
| OpenAI public Plugins Directory | The release produces the ZIP to upload. | Hosted MCP-server changes can be picked up separately; these skills-only packages have no hosted MCP update path. | Metadata, assets, or bundled-skill changes require a new ZIP, automated checks/review, and publication of the approved version. Publishing replaces the prior package. See [OpenAI's update instructions](https://developers.openai.com/plugins/deploy/submission#update-your-published-plugin). |
| Claude third-party repo marketplace | A push makes the incremented version available from the tracked repository. | Third-party marketplace auto-update is off by default. If a user enables it, Claude Code refreshes after session start; the next session or `/reload-plugins` loads the new version. | Otherwise run `claude plugin update <plugin>@think-school`. A directly loaded folder or ZIP must be pulled or downloaded again. See [Claude Code update behavior](https://code.claude.com/docs/en/plugins/install#keep-plugins-updated). |
| Anthropic directory | The directory can track a branch or tag and scan new commits by webhook or scheduled check after the initial submission is configured. | Later passing versions can publish automatically only when Anthropic has enabled the applicable auto-publish setting and the publisher has turned it on. | Initial submission and review are manual. Depending on the portal's assigned publish setting, a passing update may still require the publisher to select Publish and/or an Anthropic reviewer to publish it. See [Anthropic's submission and update process](https://claude.com/docs/plugins/submit#update-a-published-plugin). |
| Microsoft 365 organizational catalog | The release produces an installable app-package ZIP with the manifest at its root. | Nothing is published, assigned, or installed automatically. | An authorized tenant administrator validates and uploads the exact package, reviews permissions and audience, approves it, and controls availability. Customer-specific packages must be built from private configuration and retained outside the public repository. See [Microsoft 365 Copilot distribution and governance](microsoft365-copilot.md). |

Provider publication timing never authorizes version drift in the repository. If one
provider is still reviewing a release, report that provider as pending while keeping
the same validated package version ready for every supported path.

## Release sequence

1. Edit only canonical `_source/` content and shared generator inputs.
2. Increment every supported platform version for each changed team to the same semver.
3. Regenerate and run every validation command above.
4. Validate clean installs for every supported platform. For Microsoft 365, use a
   development or test tenant and validate the exact ZIP.
5. Merge the validated commit through Staging and then main using protected-branch pull
   requests and required checks.
6. Build release archives from the final main commit. Provider portals and tenant
   administrators must receive those exact checksummed archives or track that exact
   commit/tag.
7. Record each provider's validation, review, approval, and publication state
   separately. A successful repository build or upload is not marketplace publication.

## Functional parity boundary

Parity means every package for a team can run the same user-visible workflow and
produce the same class of deliverable while preserving the same human approval and
external-action boundaries. It does not require identical files: Claude Code discovers
multiple skills, while OpenAI and Microsoft 365 use a team-level skill with reference
files. Platform-only metadata, grounding capabilities, licensing, and installation
mechanics remain platform-specific.
