# THINK School Growth Team Marketplace

The **public marketplace contains two independently installable plugins**. Growth Team is the umbrella for Capture and Proposal, not a third installable plugin.

| Team | Work stages | Claude Code source | Codex source |
|---|---|---|---|
| [Capture Team](claude/capture-team/) | Find, Qualify, Research, Capture | `Plugins/claude/capture-team/` | [`Plugins/codex/capture-team/`](codex/capture-team/) |
| [Proposal Team](claude/proposal-team/) | Respond, Review | `Plugins/claude/proposal-team/` | [`Plugins/codex/proposal-team/`](codex/proposal-team/) |

The six stages describe the **learning and work lifecycle**, not a claim that every stage has a dedicated built-in Digital Employee or integration. Check each plugin's actual supported capabilities and configure your own organization inputs.

## Install

### Claude Code

The Claude marketplace uses [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) and points to `Plugins/claude/<team>/`. In Claude Code, use:

```text
/plugin marketplace add Compound-Leverage/THINK-school
/plugin install capture-team@think-school
```

Or install `proposal-team@think-school`. See [Claude instructions](../.claude-plugin/README.md). These commands are for Claude Code, **not ordinary Claude chat**.

### Codex

The Codex marketplace uses [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) and points to `Plugins/codex/<team>/`, whose skill structure differs from the Claude Code packages. See [Codex instructions](../.agents/README.md). Availability and installation surfaces can vary; do not assume that uploading a SKILL.md in an ordinary chat installs a full plugin.

## Work with the teams

Begin with [the six-stage learning path](../Learn/README.md). Provide authorized organization-specific inputs and approve the deliverable at each relevant gate.

- **Capture Team:** Chet (cluster discovery), Kipp (CRM intake), Ben (signal delivery). [Historical example prompts](../Archive/Legacy-Resources/Prompts/capture-team.md).
- **Proposal Team:** Maya (orchestration), Chase (research), Priya (assessment), Porter (strategy), Quinn (writing), Diego (QA), Blair (funder pitch development). [Historical example prompts](../Archive/Legacy-Resources/Prompts/proposal-team.md).

## Preserved source packages

Seven older team packages are preserved under [`Archive/Other-Teams/`](../Archive/Other-Teams/). They are **not listed in either public marketplace manifest**. Their historical prompts, templates, and workflows are under [`Archive/Legacy-Resources/`](../Archive/Legacy-Resources/). Archived team packages are not maintained installation targets.

[Learning stages](../Learn/README.md) · [Standalone skills](../Skills/README.md) · [Repository map](../Docs/repo-map.md)
