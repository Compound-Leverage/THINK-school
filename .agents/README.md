# Codex marketplace

The Codex marketplace manifest is [`plugins/marketplace.json`](plugins/marketplace.json). It currently lists **Capture Team and Proposal Team only**, pointing to `Plugins/OpenAI/capture-team/` and `Plugins/OpenAI/proposal-team/` respectively.

These Codex-oriented packages use an orchestration skill with role references. They are **not identical** to the multi-persona Claude Code packages under `Plugins/`.

Open the plugin browser in a supported Codex environment and select the THINK School marketplace, if available. The exact installation UI may vary by client and account; the presence of a manifest does not guarantee a public directory listing or an installed ChatGPT plugin.

See [the plugin guide](../Plugins/README.md) and [the six-stage learning path](../Learn/README.md). For Claude Code, use [the Claude marketplace guide](../.claude-plugin/README.md).
