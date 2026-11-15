# Plugin release validation checklist

This checklist is a **manual test protocol**, not a claim that installations have been tested.

## Static checks

- [ ] Both [Claude marketplace manifest](../.claude-plugin/marketplace.json) and [Codex marketplace manifest](../.agents/plugins/marketplace.json) parse as JSON.
- [ ] Each manifest points to an existing package directory for Capture Team and Proposal Team.
- [ ] Each package includes its platform-specific metadata and executable instructions.
- [ ] All relative asset and role-reference links resolve.
- [ ] No plugin silently assumes the publisher's organization is the user's client.
- [ ] Historical content is not required from the `legacy-archive` branch.

## OpenAI submission zip boundary

`Plugins/<team>/openai/.codex-plugin/plugin.json` references the icon and config
templates one level up, at `Plugins/<team>/assets/` -- a sibling of `openai/`, not a
child of it. When building the OpenAI submission zip, **zip `Plugins/<team>/` as the
top-level directory** (so `openai/` and `assets/` are both inside it), not `openai/`
alone. OpenAI's upload has rejected a zip before with "Plugin manifest not found... at
the ZIP root or inside its only top-level directory" when the manifest referenced a path
outside the zipped folder -- confirmed by a real rejection in this repo's history.
`openai-plugin/*.zip` are gitignored, locally-built artifacts, not committed to the repo.

## Claude directory icon boundary

Anthropic's public directory reads the `icon` field even though Claude Code itself
currently reports that field as directory-only metadata. The icon path must resolve
inside the Claude plugin root. Each Claude package therefore carries
`assets/think-school.png` and references it as `./assets/think-school.png`; do not point
the Claude manifest at the team-level `../assets/` copy used by the OpenAI package.

`privacyPolicyUrl`, `termsOfServiceUrl`, `supportUrl`, and `documentationUrl` are
directory-only listing metadata. Released Claude Code builds currently warn that they
ignore these fields at plugin load time, but Anthropic's directory review explicitly
reads all four and reports that no action is needed. Keep them in the submitted
manifest; use non-strict `claude plugin validate` for the release check until the CLI
recognizes directory-only fields.

## Live platform tests (run separately)

- [ ] Claude Code: add the marketplace, install Capture Team, and run the fictional first assignment.
- [ ] Claude Code: install Proposal Team, verify Chase stops at the human gate.
- [ ] Codex: install Capture Team using a supported client, run the fictional first assignment.
- [ ] Codex: install Proposal Team, verify the research gate and role references.
- [ ] Verify no outbound messages, CRM writes, or invented citations occur without explicit authorization.
- [ ] Record client version, install steps, failures, screenshots/logs, and date.

## Adoption measurement

Measure **repository discovery → documented install attempts → successful installations → first completed assignment → repeat assignments**. GitHub stars and forks are discovery proxies only; they do not prove installations or completed work. Do not publish installation or completion rates until instrumentation exists.
