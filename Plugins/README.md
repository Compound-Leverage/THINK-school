# THINK School Growth Team Plugins

The [public marketplaces](../Marketplaces/README.md) contain two independently installable plugins. Growth Team is the umbrella for Capture and Proposal, not a third installable plugin.

| Team | Work stages | Claude Code source | OpenAI (Codex) source |
|---|---|---|---|
| [Capture Team](capture-team/claude/) | Find, Qualify, Research, Capture | `Plugins/capture-team/claude/` | [`Plugins/capture-team/openai/`](capture-team/openai/) |
| [Proposal Team](proposal-team/claude/) | Respond, Review | `Plugins/proposal-team/claude/` | [`Plugins/proposal-team/openai/`](proposal-team/openai/) |

The six stages describe the **learning and work lifecycle**, not a claim that every stage has a dedicated built-in Digital Employee or integration. Check each plugin's actual supported capabilities and configure your own organization inputs.

## Install directly from GitHub

The repository is the **user-install distribution path**. Official marketplace approval is not needed to install the packages using a supported client. The platform-specific manifests below support discovery and installation from this repository; an official listing is an optional separate channel.


### Claude Code

The repository's Claude marketplace manifest uses [`.claude-plugin/marketplace.json`](../.claude-plugin/marketplace.json) and points to `Plugins/<team>/claude/`. In Claude Code, use:

```text
/plugin marketplace add Compound-Leverage/THINK-school
/plugin install capture-team@think-school
```

Or install `proposal-team@think-school`. See [Claude instructions](../.claude-plugin/README.md). These commands are for Claude Code, **not ordinary Claude chat**.

### OpenAI (Codex packages)

The repository's Codex marketplace manifest uses [`.agents/plugins/marketplace.json`](../.agents/plugins/marketplace.json) and points to `Plugins/<team>/openai/`, whose skill structure differs from the Claude Code packages. See [Codex instructions](../.agents/README.md). Availability and installation surfaces can vary; do not assume that uploading a SKILL.md in an ordinary chat installs a full plugin.

## Quickstarts and quality checks

[Capture Team: first assignment](../Docs/quickstart-capture.md) · [Proposal Team: first assignment](../Docs/quickstart-proposal.md) · [Validation checklist](../Docs/plugin-validation.md)

## Work with the teams

Begin with [the six-stage learning path](../Learn/README.md). Provide authorized organization-specific inputs and approve the deliverable at each relevant gate.

- **Capture Team:** Chet (cluster discovery), Kipp (CRM intake), Ben (signal delivery).
- **Proposal Team:** Maya (orchestration), Chase (research), Priya (assessment), Porter (strategy), Quinn (writing), Diego (QA), Blair (funder pitch development).

## Preserved source packages

Historical packages and resources are preserved on the [`legacy-archive` branch](https://github.com/Compound-Leverage/THINK-school/tree/legacy-archive/Archive). They are not listed in the active marketplaces.

[Learning stages](../Learn/README.md) · [Standalone skills](../Skills/README.md) · [Repository map](../Docs/repo-map.md)
