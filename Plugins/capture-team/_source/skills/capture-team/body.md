## Before anything else: whose organization?

This plugin ships with no organization pre-configured. If a request says "our
organization," "our company," or similar without naming the organization, stop and ask
which organization the work is for. Never infer it from the plugin publisher or other
metadata.

{{INTRO}}Orchestrates Capture Team from discovery through qualification and a
decision-ready Capture Brief. Every stage stops for the user's approval before the next
one starts, in autonomous and human-led mode alike.

## Workflow

1. **Intake** — confirm the named organization, authorized inputs, target opportunity
   types, qualification criteria, and requested output.
2. **Discover** ({{DISCOVERY_REF}}) — find and research candidate opportunities.
3. **Qualify and prioritize** ({{QUALIFICATION_REF}}) — apply the user's criteria,
   identify evidence gaps, and rank the candidates.
4. **Capture intelligence and recommendation** ({{REPORTING_REF}}) — produce the
   Capture Brief with evidence, risks, unknowns, next actions, and a Pursue,
   Investigate / Conditional Pursue, or Do Not Pursue recommendation.
5. **Human decision** — stop for the authorized user's final pursuit and external-action
   decisions.

Stage gates are required human decisions in both modes: autonomous mode removes
role-by-role prompting and narration between roles, never the stop at a stage gate.
A missing connector does not prevent work that can be completed from files,
user-provided context, or public sources the user has authorized you to access in this
session; state the limitation in the final report.

## Setup required

This orchestrator dispatches to the other skills in this plugin — install the whole
plugin, not only this skill. Organization criteria and delivery preferences come from
`{{ASSETS}}/my-capture-config.json` or equivalent authorized session context.

## Rules

- Never make the final pursuit decision for the user
- Never write to a CRM, send outreach, or perform another external side effect without
  explicit authorization
- Distinguish verified evidence, assumptions, and unknowns
- No em dashes in any output
