# THINK School Marketplaces

The Growth Team marketplace currently offers **Capture Team** and **Proposal Team**. Choose the execution environment, then install the corresponding plugin.

| Environment | Marketplace configuration | Package directory |
|---|---|---|
| Claude Code | [Claude marketplace](../.claude-plugin/marketplace.json) | [Claude packages](../Plugins/claude/) |
| OpenAI Codex | [Codex marketplace](../.agents/plugins/marketplace.json) | [Codex packages](../Plugins/OpenAI/) |

**Start with a task:** [Capture Team quickstart](../Docs/quickstart-capture.md) · [Proposal Team quickstart](../Docs/quickstart-proposal.md). See [sample deliverables](../Docs/samples/capture-brief.md) and [release validation](../Docs/plugin-validation.md).

The marketplace manifests remain at their platform-specific root locations for discovery. This folder is the **human-facing marketplace index**, not a replacement for those manifests.

**ChatGPT:** No separate ChatGPT-specific package is verified in this repository. A Codex plugin is not automatically a ChatGPT plugin.

[Plugins](../Plugins/README.md) · [Skills](../Skills/README.md) · [Learn](../Learn/README.md)
