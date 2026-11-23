# Release notes: v2.0.0 Capture skill renames and Proposal orchestration fixes

Release date: pending

This is a major release because three Claude Code skills were renamed. Per the
versioning policy in [PUBLIC_LISTING.md](PUBLIC_LISTING.md), a renamed role is a
breaking change. Both teams and both platforms move to 2.0.0 together.

## Breaking changes

Four Claude Code skills were renamed to match what each role now does:

| Old skill name | New skill name |
|---|---|
| `cluster-discovery-chet` | `opportunity-discovery-chet` |
| `crm-intake-kipp` | `opportunity-qualification-kipp` |
| `signal-delivery-ben` | `capture-brief-ben` |
| `pitch-development-blair` (Proposal Team) | `grant-proposal-blair` |

Plugin install names are unchanged (`capture-team@think-school`, `proposal-team@think-school`). Anything that calls
the old skill names directly, such as saved prompts or notes using
`/capture-team:cluster-discovery-chet`, must switch to the new names. The OpenAI
package is unaffected, because it uses one team skill with reference files.

## Other changes

- Listing names are now plural on every surface: "Managed Teams for Capture Work" and
  "Managed Teams for Proposals". The Proposal name is shortened to stay within the
  30-character limit that `validate_release.py` enforces for OpenAI.
- Updated the three Capture skill descriptions, which Claude Code uses to decide when
  to run a skill. They now describe general opportunity discovery, qualification
  against your criteria, and the decision-ready Capture Brief.
- Fixed Maya's Claude workflow, which referred to Proposal skills by names that do not
  exist (for example `proposal-researcher`). It now names the shipped skills
  (`proposal-researcher-chase` and the others).
- Added grant and funder routing to Maya on both platforms: grant opportunities go to
  Chase's Go/No-Go Discovery Brief first, then (after a human Go) Blair's funder track
  instead of the Assessment-through-Draft chain. Blair will not start without that brief.
- Stated in Maya that phase gates are required human decisions in both autonomous and
  human-led mode.

- Blair: reframed from sales "pipeline prospects" to grant and funder proposals, stops for
  review after drafting, and sends every draft through Diego's QA before approval.
- Chase: the Discovery Brief now includes risks and red flags, and the assumptions rule
  allows user-approved assumptions when they are labeled. Fixed the OpenAI path to the
  review library.

- Codex marketplace: both plugins now use the category "Business & Operations" (was "Sales"),
  matching the Claude manifests.
- QA verdicts: Maya and Blair now use Diego's actual verdicts (PASS / WARNING / FAIL)
  instead of a nonexistent REVISE verdict. Diego's scope includes Blair's funder drafts.

- Added three Proposal capability contract entries so CI fails if the per-phase gate,
  the grant routing to Blair, or Blair's QA step is removed.

- Configuration templates (additive, existing filled-in files still work):
  `my-brand-guidelines.md` gains a Delivery Methodology section for Diego's framework
  check; `my-company-profile.json` gains per-service-line evidence, set-aside status, NAICS codes, UEI/CAGE and contract vehicles; `my-pricing-model.json` gains a cost build-up section (labor categories, indirect rates, fee) for the Green Team and drops sample ROI numbers; `my-case-studies.json` gains an engagement `status` field and a privacy note on
  reference contacts. Blair treats bracketed bid-sizing placeholders as unconfigured. `my-capture-config.json` describes both of Chet's discovery patterns, gives Ben's brief Capture Brief sections, and no longer shares files with the owner by default.

- OpenAI Proposal team skill and both Proposal READMEs: every phase gates in both modes,
  QA verdict wording matches Diego, grant drafts go through Diego QA, "AI Team" is now
  "Managed Team", and the READMEs name the config files and the grant track.

- Keywords: `ai-team` is now `managed-team` on both teams; Capture drops `lead-enrichment`
  and `intelligence-brief` for `opportunity-qualification` and `capture-brief`, and the
  Claude Capture listing gains the grant and govcon keywords OpenAI already had.

- Capture now stops after every stage (Discover, Qualify, Brief) in both modes, like
  Proposal, with a matching capability check. Public sources need the user's
  authorization in the session.
- Kipp proposes CRM records and writes them only after approval; enrichment runs only
  with an authorized tool; "daily sweep" is now on-demand.
- Ben presents the brief in the session and saves or shares it only after approval; his
  output uses the full Investigate / Conditional Pursue label.
- Chet reads a website only with permission, asks before writing new groups into the
  config, and refreshes clusters on request instead of claiming a recurring cadence.

## Validation evidence

- `scripts/build_plugins.py --team all --check`: zero diff for both teams.
- `scripts/check_build_drift.py`: passed.
- `scripts/validate_release.py`: passed.
- `scripts/build_release_packages.py`: built and re-extracted all four v2.0.0 archives.

Live installation tests in Claude Code and Codex have not been run for 2.0.0.

## Publication requirements

Both public directory listings need the new packages uploaded and reviewed. The
Claude directory listing should be checked for references to the old skill names.
