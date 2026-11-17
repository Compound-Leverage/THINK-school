# Capture Team for Microsoft 365 Copilot

This directory is an installable Microsoft 365 app package source for the Capture Team
Copilot plugin. It contains a declarative agent and the same generated Capture Team
Agent Skill used to preserve the shared Find, Qualify, Research, Capture workflow.

## Install the generic package

Build the release archives from the repository root:

```bash
python3 scripts/build_release_packages.py
```

Use `release-packages/capture-team-microsoft365-v<VERSION>.zip` for validation or
tenant upload. The generic package enables web research only and ships with
organization placeholders. It does not include customer data, tenant identifiers, or
write-capable actions.

## Build a tenant-configured package

Copy `_source/microsoft365/deployment-config.example.json` to a private, untracked
location, replace every bracketed placeholder, and run:

```bash
python3 scripts/build_microsoft365_package.py \
  --config /private/path/deployment-config.json \
  --output-dir release-packages/customer
```

The builder can scope the agent to approved SharePoint or OneDrive URLs, Teams URLs,
read-only Outlook mailboxes or folders, and basic People knowledge. It rejects
placeholders and never enables `EmailActions`. Keep the customer configuration and
resulting tenant package outside the public repository.

## Governance boundary

- Tenant upload, organizational catalog submission, assignment, and installation are
  separate administrator-controlled actions.
- SharePoint, Teams, Outlook, and People capabilities require the applicable Microsoft
  licensing or pay-as-you-go configuration. Outlook, People, and Teams knowledge
  currently require a Microsoft 365 Copilot license.
- The package makes pursuit recommendations. Humans retain final pursuit and external
  communication decisions.
- Scheduled tasks are user-created in Microsoft Copilot and are not defined by this
  package. A schedule does not grant extra permissions or authorize external actions.
- Validate in a development or test tenant before any customer deployment.
