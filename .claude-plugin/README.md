# Claude Code marketplace

The [`marketplace.json`](marketplace.json) manifest lists **Capture Team and Proposal Team only**. Both point to their multi-persona packages under `Plugins/`.

In Claude Code:

```text
/plugin marketplace add Compound-Leverage/THINK-school
/plugin install capture-team@think-school
```

Alternatively, install `proposal-team@think-school`. Reload plugins or restart the session if your environment requires it.

**Claude Code plugins are not the same as ordinary Claude.ai chat attachments.** Configure your own organizational inputs; do not put private credentials into committed files. Store custom configuration outside replaceable plugin files where practical.

[Plugin guide](../Plugins/README.md) · [Six-stage learning path](../Learn/README.md) · [Codex packages](../.agents/README.md)
