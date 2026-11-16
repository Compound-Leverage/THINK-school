# THINK School Marketplaces

THINK School provides **Capture Team** and **Proposal Team** for direct installation from GitHub. Official marketplaces are a separate distribution channel; marketplace approval is **not required** to use the repository packages. Choose your execution environment and follow its supported installation instructions.

| Environment | Marketplace configuration | Package directory |
|---|---|---|
| Claude Code | [Claude marketplace](../.claude-plugin/marketplace.json) | [Claude packages](../Plugins/) |
| OpenAI Codex | [Codex marketplace](../.agents/plugins/marketplace.json) | [Codex packages](../Plugins/) |

**Start with a task:** [Capture Team quickstart](../Docs/quickstart-capture.md) · [Proposal Team quickstart](../Docs/quickstart-proposal.md). See [sample deliverables](../Docs/samples/capture-brief.md) and [release validation](../Docs/plugin-validation.md).

The marketplace manifests remain at their platform-specific root locations for discovery. This folder is the **human-facing marketplace index**, not a replacement for those manifests.

**Official listing status (checked 2026-11-16):** the signed-in OpenAI catalog served
Capture Team and Proposal Team v1.1.20; v1.2.0 still requires provider upload, checks,
approval where applicable, and publication. Anthropic's developer-portal state is
account-gated and was not verified from this repository; v1.2.0 must not be described
as live there until the directory confirms publication. Repository packages may be
installed without waiting for public-directory approval, where supported by the client.

**ChatGPT:** No separate ChatGPT-specific package is verified in this repository. A Codex plugin is not automatically a ChatGPT plugin.

Repository installs and public-directory installs use the same generated capability
source but have different update mechanisms and approval gates. See
[distribution and release parity](../Docs/distribution-and-release.md).

[Plugins](../Plugins/README.md) · [Skills](../Skills/README.md)
