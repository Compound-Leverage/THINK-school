# THINK School icon assets

`think-school.png` is the approved THINK School mark (dark background `#0D0C11`,
purple glyph `#673FBA`), copied here as the single shared visual identity for every
plugin's `interface.composerIcon` / `interface.logo` fields (see each
`Plugins/*/.codex-plugin/plugin.json`). Source: 1254x1254 PNG, square, no
transparency -- resolution is production-ready for the OpenAI submission portal.
Confirm exact size/format requirements in the portal at submit time; resize down
if it asks for something smaller, don't re-export from a lower-res source.

## Structure

Each team keeps one copy at `Plugins/<team>/assets/think-school.png` -- shared
between that team's Claude and OpenAI manifests (`../assets/think-school.png`
relative to each), not duplicated per platform. The team folder is the zip
boundary for OpenAI submission (see Docs/plugin-validation.md), so this file
has to live inside it, not at this repo-root `assets/icons/` location, which
is a reference copy only and isn't read by `scripts/build_plugins.py` -- the
real source of truth per team is `Plugins/<team>/_source/icon/think-school.png`.

Per-team icons, as they're approved, replace that team's copy -- as of
2026-11-15, proposal-team already has its own distinct icon (document/
checkmark design) under this filename; capture-team still uses the original
shared bar-chart mark:

```
assets/icons/
  think-school.png       (shared identity -- reference copy, in place)
  capture-team.png        (not yet supplied -- capture-team uses the shared mark)
  proposal-team.png       (supplied, but shipped as Plugins/proposal-team/assets/think-school.png, not this filename)
  content-team.png        (not yet supplied)
  sales-bd-team.png       (not yet supplied)
  sales-enablement.png    (not yet supplied)
  lead-discovery.png      (not yet supplied)
  fulfillment.png         (not yet supplied)
  proposal-generator.png  (not yet supplied)
```

When a per-team icon is supplied, drop it into that team's own
`Plugins/<team>/_source/icon/think-school.png` and run
`python3 scripts/build_plugins.py --write --team <name>` -- every other team
keeps using its existing icon until its turn comes.
