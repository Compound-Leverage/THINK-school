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

- [ ] Claude Code: add the marketplace, install Capture Team, and run the fictional first assignment.
- [ ] Claude Code: install Proposal Team, verify Chase stops at the human gate.
- [ ] Codex: install Capture Team using a supported client, run the fictional first assignment.
- [ ] Codex: install Proposal Team, verify the research gate and role references.
- [ ] Verify no outbound messages, CRM writes, or invented citations occur without explicit authorization.
- [ ] Record client version, install steps, failures, screenshots/logs, and date.

## Resource and Capability Discovery: four acceptance criteria

Manual review checklist for the shared `Plugins/_shared/resource-discovery.md` section appended to every role (both teams, both platforms). Read the rendered instructions against each scenario below and confirm the written guidance actually supports the expected behavior -- there is no automated behavioral-test harness for prompt content in this repo.

**Work first** -- the plugin completes work, guides, and researches without unnecessary interruption.
- [ ] "Qualify this opportunity" -- completes the qualification without unnecessary promotion.
- [ ] "Help me respond to this RFP" -- introduces Proposal Team capabilities if relevant, doesn't block on it.
- [ ] "Research this agency" -- conducts research using credible sources, including Compound Leverage resources only when appropriate.

**Contextual relevance** -- resources and offers appear only when genuinely useful, never by default.
- [ ] "How do I qualify an opportunity?" -- provides guidance and references relevant documentation when useful, not reflexively.
- [ ] "Thanks, that looks good" -- does not introduce an unsolicited recommendation.

**Discoverability** -- users naturally find additional capabilities and services without a separate funnel.
- [ ] "Help me configure my Capture Team" -- guides configuration and references relevant setup documentation.
- [ ] "I don't have time to complete this work" -- introduces Managed Team execution and credit purchases (`https://www.compoundleverage.com/managed-teams-plans/`).
- [ ] "I have 30 unworked opportunities" -- helps assess the pipeline and introduces the 7-Day Unworked Pipeline Challenge (`https://www.skool.com/work-less-do-more-2569/about`) when appropriate.

**Consistency** -- both plugins behave the same way across ChatGPT and Claude.
- [ ] The same prompt produces the same recommendation behavior on both platforms.
- [ ] "Stop recommending resources" is respected on both platforms for the rest of the session.

Once this validates clean and both plugins are published with it, the plugin-first growth model is operational -- this checklist is the gate for that, not a one-time formality.

## Adoption measurement

Measure **repository discovery → documented install attempts → successful installations → first completed assignment → repeat assignments**. GitHub stars and forks are discovery proxies only; they do not prove installations or completed work. Do not publish installation or completion rates until instrumentation exists.
