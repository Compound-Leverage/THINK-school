# Repository map

## User-facing navigation

| Area | Purpose |
|---|---|
| [Marketplaces](../Marketplaces/README.md) | Platform-specific marketplace entry points for Capture and Proposal |
| [Plugins](../Plugins/README.md) | Claude and Codex execution packages |
| [Skills](../Skills/README.md) | Standalone capabilities |
| [Learn](../Learn/README.md) | Six work stages: Find, Qualify, Research, Capture, Respond, Review |
| [Docs](README.md) | Supporting architecture, methodology, and service guides |

## Technical directories

- `Plugins/claude/`: Claude Code-native team packages.
- `Plugins/OpenAI/`: Codex-oriented execution packages; different skill structure.
- `.claude-plugin/` and `.agents/plugins/`: platform-required marketplace manifests; do not relocate for cosmetic navigation.
- `Skills/`: standalone reusable skills, separate from plugin-internal execution skills.

## Learning model

Use [Learn](../Learn/README.md) to choose an assignment by the work to be done, then review the expected deliverable, human decision gate, and customization guidance. Some older reference material is named after Digital Employees; it does not require beginners to orchestrate individual personas.

Legacy team packages and historical reference materials are preserved on the [`legacy-archive` branch](https://github.com/Compound-Leverage/THINK-school/tree/legacy-archive/Archive), not in the active repository tree.
