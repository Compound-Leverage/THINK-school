# Proposal Team for Microsoft 365 Copilot

This directory is an installable Microsoft 365 app package source for the Proposal Team
Copilot plugin. It contains a declarative agent and the same generated Proposal Team
Agent Skill used to preserve the shared Intake, Research, Assessment, Strategy, Draft,
QA/Review, Output workflow.

## Install the generic package

Build the release archives from the repository root:

```bash
python3 scripts/build_release_packages.py
```

Use `release-packages/proposal-team-microsoft365-v<VERSION>.zip` for validation or
tenant upload. The generic package enables web research only and ships with
organization placeholders. It does not include customer data, tenant identifiers, or
write-capable actions.

## Tenant-configured packages

A private tenant-package builder (`scripts/build_microsoft365_package.py`) exists today
for Capture Team only. Proposal Team's organization-specific inputs are five
configuration files (company profile, pricing model, case studies, brand guidelines,
and bid-sizing rules) rather than Capture Team's single pursuit-type selector, so
scoping which fields of those files are safe to override through a tenant builder is a
separate, not-yet-made product decision. Until that builder exists, configure a
tenant-specific deployment by editing the packaged
`skills/proposal-team/assets/*.json` and `*.md` files directly before upload, the same
way Claude Code and OpenAI installs are configured today.

`_source/microsoft365/deployment-config.example.json` documents the organization
identity, agent branding, and Microsoft knowledge-grounding scopes (SharePoint, Teams,
read-only Outlook, People, web search) that are mechanically identical to Capture
Team's -- those are honored by the same builder mechanics once Proposal Team support is
added.

## Governance boundary

- Tenant upload, organizational catalog submission, assignment, and installation are
  separate administrator-controlled actions.
- SharePoint, Teams, Outlook, and People capabilities require the applicable Microsoft
  licensing or pay-as-you-go configuration. Outlook, People, and Teams knowledge
  currently require a Microsoft 365 Copilot license.
- The package produces research, drafts, and recommendations. Humans retain final
  pursue, pricing, content, outreach, and submission decisions.
- Scheduled tasks are user-created in Microsoft Copilot and are not defined by this
  package. A schedule does not grant extra permissions or authorize external actions.
- Validate in a development or test tenant before any customer deployment.
