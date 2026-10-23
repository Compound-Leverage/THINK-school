# THINK School Growth Team Plugins

The [public marketplaces](../Marketplaces/README.md) contain two independently installable plugins. Growth Team is the umbrella for Capture and Proposal, not a third installable plugin.

| Team | Work stages | Claude Code source | OpenAI (Codex) source |
|---|---|---|---|
| [Capture Team](claude/capture-team/) | Find, Qualify, Research, Capture | `Plugins/claude/capture-team/` | [`Plugins/OpenAI/capture-team/`](OpenAI/capture-team/) |
| [Proposal Team](claude/proposal-team/) | Respond, Review | `Plugins/claude/proposal-team/` | [`Plugins/OpenAI/proposal-team/`](OpenAI/proposal-team/) |

The six stages describe the **learning and work lifecycle**, not a claim that every stage has a dedicated built-in Digital Employee or integration. Check each plugin's actual supported capabilities and configure your own organization inputs.

## Install

### Claude Code

The Claude marketplace uses [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) and points to `Plugins/claude/<team>/`. In Claude Code, use:

```text
/plugin marketplace add Compound-Leverage/THINK-school
/plugin install capture-team@think-school
```

Or install `proposal-team@think-school`. See [Claude instructions](../.claude-plugin/README.md). These commands are for Claude Code, **not ordinary Claude chat**.

### OpenAI (Codex packages)

The Codex marketplace uses [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) and points to `Plugins/OpenAI/<team>/`, whose skill structure differs from the Claude Code packages. See [Codex instructions](../.agents/README.md). Availability and installation surfaces can vary; do not assume that uploading a SKILL.md in an ordinary chat installs a full plugin.

## Work with the teams

Begin with [the six-stage learning path](../Learn/README.md). Provide authorized organization-specific inputs and approve the deliverable at each relevant gate.

- **Capture Team:** Chet (cluster discovery), Kipp (CRM intake), Ben (signal delivery).
- **Proposal Team:** Maya (orchestration), Chase (research), Priya (assessment), Porter (strategy), Quinn (writing), Diego (QA), Blair (funder pitch development).

## Preserved source packages

Historical packages and resources are preserved on the [`legacy-archive` branch](https://github.com/Compound-Leverage/THINK-school/tree/legacy-archive/Archive). They are not listed in the active marketplaces.

[Learning stages](../Learn/README.md) · [Standalone skills](../Skills/README.md) · [Repository map](../Docs/repo-map.md)
