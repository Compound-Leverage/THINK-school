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

## Update 2026-11-15 (later same day): unified, content decisions resolved

Marvin resolved the three open content questions below, and `priya`, `porter`,
`quinn`, `diego`, `blair`, `maya` are now unified into `body.md` + `meta.yaml`
the same way the first five roles were:

- **Voice: persona name everywhere, both platforms.** Claude's generic
  references ("the researcher's Discovery Brief") were rewritten to the
  persona name ("Chase's Discovery Brief"), matching openai and matching how
  Maya's own content already names everyone.
- **Intro-paragraph duplication:** one canonical intro, used as both the
  claude frontmatter `description:` and the openai body-intro prose (same
  pattern chase already used). Maya's specific case -- "dispatching
  Researcher, Analyst, Strategist, Writer, and QA" (frontmatter) vs.
  "dispatching Research, Assessment, Strategy, Draft, and QA" (openai body) --
  resolved to the phase-style wording (matching the Workflow list's existing,
  already-consistent phrasing on both platforms).
- **Blair's missing content** (the autonomy sentence and the explicit
  chase→priya→porter→quinn→diego chain reference) ported into the canonical
  body, now on both platforms.

**New generator mechanism added:** `_apply_platform_refs()` generalizes the
existing `review_ref` claude-vs-openai cross-reference pattern (claude
references a skill by name, openai by file path) to any meta.yaml key shaped
`{claude: ..., openai: ...}`. Maya needed five of these (one per pipeline
phase: `research_ref`, `assessment_ref`, `strategy_ref`, `draft_ref`,
`qa_ref`) plus `review_system_ref` for her review-orchestration paragraph,
since her Workflow list points at a different skill/file per phase per
platform -- `review_ref` alone only handled one cross-reference per role.

**Two small, disclosed deviations from strict content preservation** (content
was already changing here, per the plan's own note that byte-identical
reproduction wasn't the goal for this pass):
- Maya's "Setup required" line originally said `priya.md` (no `references/`
  prefix) on openai, inconsistent with the Workflow list's `references/
  priya.md`. Reused the same `{{ASSESSMENT_REF}}` token for both for
  consistency rather than adding a second, near-duplicate token just for this
  one line -- cosmetic only, both point at the same file.
- Blair's claude.md `Rules` section was only ever the em-dash rule; openai.md
  had no `Rules` heading at all (nothing else to repeat). Keeping the heading
  in the canonical body (claude still needs it stated somewhere -- unlike
  openai, claude has no shared master file to fall back on) left an empty
  `## Rules` heading dangling at the end of openai's render. Fixed with one
  additional regex in `render_unified_openai_reference` that drops a
  resulting empty trailing `## Rules` heading; verified it doesn't affect any
  other role, all of which have content after their Rules section.

## Original findings (for reference)

`priya`, `porter`, `quinn`, `diego`, `blair`, `maya` -- all in `proposal-team`.
These had **real, authored content differences**, not just formatting, which
is why they were left unmerged in the first pass. Found, by role:

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
