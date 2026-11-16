# Plugin release validation checklist

This checklist is a **manual test protocol**, not a claim that installations have been tested.

## Static checks

- [ ] Both [Claude marketplace manifest](../.claude-plugin/marketplace.json) and [Codex marketplace manifest](../.agents/plugins/marketplace.json) parse as JSON.
- [ ] Each manifest points to an existing package directory for Capture Team and Proposal Team.
- [ ] Each package includes its platform-specific metadata and executable instructions.
- [ ] All relative asset and role-reference links resolve.
- [ ] No plugin silently assumes the publisher's organization is the user's client.
- [ ] Historical content is not required from the `legacy-archive` branch.
- [ ] `python3 scripts/check_build_drift.py` reports zero generated-file drift and no version drift.
- [ ] `python3 scripts/validate_release.py` confirms every capability contract entry on both platforms.
- [ ] `python3 scripts/build_release_packages.py` produces four archives and a checksum manifest from one commit.

## OpenAI submission zip boundary

`Plugins/<team>/openai/` is the OpenAI plugin root. Its `.codex-plugin/`, `skills/`,
`assets/`, and `README.md` entries must remain together. The submission ZIP contains one
top-level `<team>/` directory whose direct contents are those plugin-root entries. The
manifest must therefore resolve at `<team>/.codex-plugin/plugin.json`, not one level
deeper at `<team>/openai/.codex-plugin/plugin.json`. All declared paths start with `./`
and stay inside this root. OpenAI's upload has rejected a zip before with "Plugin
manifest not found... at the ZIP root or inside its only top-level directory" --
confirmed by a real rejection in this repo's history.
`openai-plugin/*.zip` are gitignored, locally-built artifacts, not committed to the repo.

Build (or rebuild) them with `python3 scripts/build_openai_zip.py --team <name>|all` --
it copies the contents of `openai/` (not the containing directory, `claude/`, `_source/`,
or the compatibility team-level `assets/`) into a single top-level `<team>/` directory,
validates the manifest and icon paths, and zips that.

## Claude directory icon boundary

Anthropic's public directory reads the `icon` field even though Claude Code itself
currently reports that field as directory-only metadata. The icon path must resolve
inside the Claude plugin root. Each Claude package therefore carries
`assets/think-school.png` and references it as `./assets/think-school.png`; do not point
the Claude manifest at the team-level compatibility copy outside the plugin root.

`privacyPolicyUrl`, `termsOfServiceUrl`, `supportUrl`, and `documentationUrl` are
directory-only listing metadata. Released Claude Code builds currently warn that they
ignore these fields at plugin load time, but Anthropic's directory review explicitly
reads all four and reports that no action is needed. Keep them in the submitted
manifest; use non-strict `claude plugin validate` for the release check until the CLI
recognizes directory-only fields.

Configuration templates are also copied into each platform package's own `assets/`
directory. Skills must reference those in-package copies and must not depend on the
team-level compatibility `assets/` directory outside the released plugin root.

## Live platform tests (run separately)

- [ ] Claude Code direct: load each Claude package with `--plugin-dir` and confirm its skills are available.
- [ ] Claude Code marketplace: add a clean local or Git marketplace, install Capture Team, and run the fictional first assignment.
- [ ] Claude Code: install Proposal Team, verify Chase stops at the human gate.
- [ ] OpenAI direct: install or load each OpenAI package in a supported clean client and confirm the team skill is available.
- [ ] OpenAI repo marketplace: add a clean marketplace source, install Capture Team, and run the fictional first assignment.
- [ ] Codex: install Proposal Team, verify the research gate and role references.
- [ ] For both Capture installs, request autonomous execution and confirm a decision-ready report is returned without claiming background or scheduled work.
- [ ] For both Proposal installs, request autonomous execution and confirm internal phases can continue while final pursuit, pricing, outreach, and submission decisions remain human-gated.
- [ ] Verify no outbound messages, CRM writes, or invented citations occur without explicit authorization.
- [ ] Record client version, install steps, failures, screenshots/logs, and date.

## Autonomous reporting acceptance criteria

The shared `Plugins/_shared/autonomous-reporting.md` contract is generated into both
teams on both platforms. Automated checks prove the instructions are packaged; live
tests prove the host actually invokes them.

- [ ] Autonomous mode completes all safe internal stages without stopping only to narrate role handoffs.
- [ ] The final report lists completed work, sources, assumptions, gaps, risks, blockers, next actions, and required approvals.
- [ ] A missing connector is reported as a limitation but does not block work that can use provided files, session context, or credible public sources.
- [ ] The plugin does not claim background, scheduled, or recurring execution unless the host has actually configured it.
- [ ] Final pursuit, pricing, outreach, submission, CRM-write, and other external-action decisions remain human-gated on both platforms.

## Adoption measurement

Measure **repository discovery → documented install attempts → successful installations → first completed assignment → repeat assignments**. GitHub stars and forks are discovery proxies only; they do not prove installations or completed work. Do not publish installation or completion rates until instrumentation exists.
