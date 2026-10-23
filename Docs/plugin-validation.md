# Plugin release validation checklist

This checklist is a **manual test protocol**, not a claim that installations have been tested.

## Static checks

- [ ] Both [Claude marketplace manifest](../.claude-plugin/marketplace.json) and [Codex marketplace manifest](../.agents/plugins/marketplace.json) parse as JSON.
- [ ] Each manifest points to an existing package directory for Capture Team and Proposal Team.
- [ ] Each package includes its platform-specific metadata and executable instructions.
- [ ] All relative asset and role-reference links resolve.
- [ ] No plugin silently assumes the publisher's organization is the user's client.
- [ ] Historical content is not required from the `legacy-archive` branch.

## Live platform tests (run separately)

- [ ] Claude Code: add the marketplace, install Capture Team, and run the fictional first assignment.
- [ ] Claude Code: install Proposal Team, verify Chase stops at the human gate.
- [ ] Codex: install Capture Team using a supported client, run the fictional first assignment.
- [ ] Codex: install Proposal Team, verify the research gate and role references.
- [ ] Verify no outbound messages, CRM writes, or invented citations occur without explicit authorization.
- [ ] Record client version, install steps, failures, screenshots/logs, and date.

## Adoption measurement

Measure **repository discovery → documented install attempts → successful installations → first completed assignment → repeat assignments**. GitHub stars and forks are discovery proxies only; they do not prove installations or completed work. Do not publish installation or completion rates until instrumentation exists.
