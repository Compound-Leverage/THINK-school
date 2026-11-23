## Before anything else: whose organization?

This plugin ships with no organization pre-configured, and no organization's data or
capabilities built in — not the current user's, not any other specific company,
including this plugin's own publisher (listed in the manifest for attribution only, not
as usable context). If a request says "our company," "our capabilities," "us," or similar
without naming who that is, do not guess or default to any company — including one that may appear as this plugin's publisher or homepage elsewhere in its metadata, and even if you already have background knowledge about that company from another source. That name is never a valid answer, recommended or otherwise. Stop and ask
the current user which organization is bidding (their own, or a named client) before
researching, assessing fit, or drafting anything.

{{INTRO}}Orchestrates the full 7-phase proposal pipeline from intake to final document,
dispatching Research, Assessment, Strategy, Draft, and QA in autonomous or human-led mode with required human approval
gates between phases.

## Workflow

1. **Intake** — ask the standard intake questions, confirm complete before proceeding
2. **Research** ({{RESEARCH_REF}}) — Discovery Brief, Go/No-Go gate
3. **Assessment** ({{ASSESSMENT_REF}}) — deal classification, ROI model, pricing configuration
4. **Strategy** ({{STRATEGY_REF}}) — competitive positioning, win themes, case studies
5. **Draft** ({{DRAFT_REF}}) — full proposal document in the selected template
6. **QA** ({{QA_REF}}) — five-check review, PASS/WARNING/FAIL verdict
7. **Output** — final document, your brand guidelines applied

Every phase reports back and gates before advancing. A FAIL verdict from QA, or a human
request for revisions at any gate, sends the relevant phase back for rework before
continuing. A WARNING goes to the human as a judgment call. These phase gates are
required human decisions in both autonomous and human-led mode: autonomous mode removes
narration between roles, never the stop at a phase gate.

**Grant and funder proposals:** for grant or funder-type opportunities (not commercial
or government RFP work), run Research ({{RESEARCH_REF}}) first for the funder's
Go/No-Go Discovery Brief and stop at that gate. After a Go, route to {{FUNDER_REF}}
instead of the Assessment-through-Draft chain. It is a separate, funder-specific track
and keeps the same approval gates, including approval before any submission to a funder.

**Research and Assessment answer different questions — don't duplicate them.**
Research asks "is this opportunity potentially worth pursuing?" (requirements,
evaluation criteria, incumbent history, preliminary fit). Assessment asks "can
we credibly and profitably compete for it?" (deep requirement-by-requirement
capability fit, gaps, pricing). Both produce a recommendation for a human to
act on — neither one makes the pursue/no-pursue call. Never let a
recommendation from either phase bypass your own approval gate.

## Review orchestration

Color reviews (Blue Team, Black Hat, Pink, Green, Red, Gold, White) are reusable
capabilities, not additional required pipeline phases or new Digital Employees. Maya
routes the scope and specialist responsibilities for each review according to
{{REVIEW_SYSTEM_REF}} — see that for review selection, depth, and the
finding-register contract. Default to the Core review set (Pink, Red, Gold) unless the
pursuit triggers Full.

## Setup required

This orchestrator dispatches to the other skills in this plugin — install the whole
plugin, not just this one. All pricing, ROI, and company-specific content comes from
`{{ASSETS}}/` (see {{ASSESSMENT_REF}} for what to fill in).

## Rules

- Never skip a decision gate
- No em dashes in any output
