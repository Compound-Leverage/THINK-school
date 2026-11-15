# Plugin skill-content audit (2026-11-15)

Confirmed by direct diff of every role's `claude.md` against its `openai.md` in
`Plugins/<team>/_source/skills/<role>/`, as the last step of closing out the
platform-content-duplication work. Two outcomes:

## Unified (one `body.md` + `meta.yaml`, rendered into both shapes)

`capture-team`: chet, kipp, ben. `proposal-team`: chase, review-system.

After normalizing the known mechanical differences (frontmatter vs H1, em dash
vs double-hyphen, asset-path depth, the "No em dashes" rule hoisted to the
openai master file instead of repeated per role, and -- for chase/kipp -- an
intro heading ("## Purpose" or similar) that sits after the guardrail block
instead of at the very top), these five roles' actual instructional text was
byte-identical. `scripts/build_plugins.py` now renders both platforms from one
canonical `body.md` per role; see `render_unified_claude_skill` /
`render_unified_openai_reference` there for exactly what's mechanical.

**One disclosed, accepted exception:** capture-team's three openai reference
files (`ben.md`, `chet.md`, `kipp.md`) now carry a few lines of pure line-wrap
reflow relative to what was committed before this change -- the original
`claude.md` and `openai.md` were independently hand-wrapped at slightly
different widths for the same sentences. Unifying into one body necessarily
picks one wrap (claude's, since that's what the canonical body is authored
in). This changes zero words and zero rendered meaning, only where a soft line
break falls. `proposal-team`'s chase and review-system did not have this
issue -- their original wrapping already matched.

## Still legacy (separate `claude.md` + `openai.md`, unchanged, do not merge)

`priya`, `porter`, `quinn`, `diego`, `blair`, `maya` -- all in `proposal-team`.
These have **real, authored content differences**, not just formatting.
Force-unifying them would silently change approved, shipped wording on one
platform or the other, which is explicitly out of scope for this pass. Found,
by role:

- **Every one of priya/porter/quinn/diego/blair/maya's openai.md opens with an
  extra paragraph that claude.md doesn't have** -- a prose version of the
  claude frontmatter's `description:` field, since openai has no frontmatter
  to hold it separately. This is *not* pure duplication of the frontmatter
  text -- it's independently phrased, not a mechanical restatement (e.g.
  maya's frontmatter says "dispatching Researcher, Analyst, Strategist,
  Writer, and QA"; her openai body-intro says "dispatching Research,
  Assessment, Strategy, Draft, and QA" -- roles vs. phases). A content call
  (write one canonical intro and derive both, or keep them distinct as
  metadata vs. body prose) is needed before this can mechanize safely.
- **"the researcher" (claude) vs. "Chase" (openai)**, and the equivalent for
  other named roles -- priya, porter, and diego's claude.md consistently
  refers to upstream roles generically ("the researcher's Discovery Brief");
  their openai.md consistently names the actual persona ("Chase's Discovery
  Brief"). Deliberate, consistent voice difference across all three files,
  not drift -- needs a decision on which voice is canonical before merging.
- **Selectively combined/dropped Rules bullets**: quinn's claude.md Rules has
  one bullet "No em dashes, no emojis"; the openai.md version keeps only "No
  emojis" (dropping the em-dash half, since that's hoisted elsewhere) --
  splitting a combined bullet is an editorial choice, not something the
  generator can infer safely for other similarly-combined bullets.
- **blair has the most real divergence**: openai's intro adds two full
  sentences claude's doesn't have at all ("Generation is autonomous;
  submission to external funders requires your approval." and an explicit
  `chase.md -> priya.md -> porter.md -> quinn.md -> diego.md` chain
  reference). This is actual missing content on the claude side, not a
  wording variant -- worth a real content decision, not a mechanical fix.

**Recommendation for the next pass, if these get picked up:** resolve the
voice question (generic role name vs. persona name) and the intro-paragraph
duplication (frontmatter description vs. body intro) as explicit content
decisions first, then these six roles likely unify the same way the first
five did.
