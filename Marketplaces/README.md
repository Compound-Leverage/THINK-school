# THINK School Marketplaces

THINK School provides **Capture Team** and **Proposal Team** for direct installation from GitHub. Official marketplaces are a separate distribution channel; marketplace approval is **not required** to use the repository packages. Choose your execution environment and follow its supported installation instructions.

| Environment | Marketplace configuration | Package directory |
|---|---|---|
| Claude Code | [Claude marketplace](../.claude-plugin/marketplace.json) | [Claude packages](../Plugins/claude/) |
| OpenAI Codex | [Codex marketplace](../.agents/plugins/marketplace.json) | [Codex packages](../Plugins/OpenAI/) |

**Start with a task:** [Capture Team quickstart](../Docs/quickstart-capture.md) · [Proposal Team quickstart](../Docs/quickstart-proposal.md). See [sample deliverables](../Docs/samples/capture-brief.md) and [release validation](../Docs/plugin-validation.md).

The marketplace manifests remain at their platform-specific root locations for discovery. This folder is the **human-facing marketplace index**, not a replacement for those manifests.

**Official listing status (publisher-reported):** OpenAI Capture and Proposal listings are published; Claude marketplace submissions remain pending approval. These statuses are not independently verified here. Repository packages may be installed without waiting for official listing approval, where supported by the client.

**ChatGPT:** No separate ChatGPT-specific package is verified in this repository. A Codex plugin is not automatically a ChatGPT plugin.

[Plugins](../Plugins/README.md) · [Skills](../Skills/README.md) · [Learn](../Learn/README.md)
