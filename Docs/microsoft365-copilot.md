# Microsoft 365 Copilot distribution and governance

Capture Team and Proposal Team each ship as an installable Microsoft 365 app package.
Each package contains a Microsoft 365 Copilot declarative agent and a generated
team Agent Skill. Neither requires a hosted bot or a separate Compound Leverage
runtime.

## Why this packaging model

Microsoft 365 declarative agent schema v1.9 can reference Agent Skill directories
directly. That lets each package reuse the same canonical team workflow and role
content that generate the Claude and OpenAI packages. A custom-engine agent would add
an independently hosted runtime and is not required for the current research,
qualification, briefing, drafting, and review workflows.

The source of truth remains `Plugins/<team>/_source/`. Do not hand-edit the generated
`Plugins/<team>/microsoft365/` directory.

## Package contents

- `manifest.json`: Microsoft 365 app manifest v1.30.
- `declarativeAgent.json`: declarative agent manifest v1.9.
- `skills/<team>/`: shared team skill, role references, and runtime configuration.
- `color.png` and `outline.png`: required 192 x 192 and 32 x 32 package icons.
- `deployment-config.example.json`: private tenant-configuration template.

The generic release package enables web search only. It is useful for package
validation and organization-neutral use. A customer build can add only the approved
SharePoint, Teams, read-only Outlook, and People scopes declared in its private
deployment configuration.

## Build and install

Build the generic installable packages:

```bash
python3 scripts/build_plugins.py --team all --check
python3 scripts/validate_release.py
python3 scripts/build_release_packages.py
```

The output is `release-packages/capture-team-microsoft365-v<VERSION>.zip` and
`release-packages/proposal-team-microsoft365-v<VERSION>.zip`. Each ZIP has
`manifest.json` at its root as Microsoft 365 requires.

For a Capture Team customer-configured build, copy the example configuration outside
the public repository, replace or remove every placeholder, and run:

```bash
python3 scripts/build_microsoft365_package.py \
  --config /private/path/deployment-config.json \
  --output-dir release-packages/customer
```

This private tenant-package builder currently supports Capture Team only -- its config
schema (`active_pursuit_type`, the `capture_config` override allowlist) matches Capture
Team's single configuration file. Proposal Team's organization-specific inputs are five
separate files (company profile, pricing, case studies, brand guidelines, bid sizing)
with no equivalent "active mode" selector; scoping which of their fields are safe
tenant overrides is a deferred product decision, not a mechanical rename. Until that
builder exists, configure a Proposal Team tenant deployment by editing the packaged
`skills/proposal-team/assets/*` files directly before upload. See
[Proposal Team's Microsoft 365 README](../Plugins/proposal-team/_source/readme/microsoft365.md).

Do not commit a private configuration or tenant package. Upload and assignment must
be performed by an authorized tenant administrator after nonproduction validation.

## Configuration model

Capture Team's `my-capture-config.json` defines the shared pursuit workflow. Its
`pursuit_types.active` value selects business development, government contracting,
grant funding, or membership development without forking the core skill. Each type can
use its own qualification profile and deliverable label.

Proposal Team's five configuration files (`my-company-profile.json`,
`my-pricing-model.json`, `my-case-studies.json`, `my-brand-guidelines.md`,
`my-bid-sizing.json`) define the bidding organization's profile, pricing, proof points,
voice, and funder bid-sizing rules used across every phase of its pipeline.

The private Microsoft deployment configuration controls tenant capabilities for either
team:

| Setting | Result | Guardrail |
|---|---|---|
| `sharepoint_urls` | Adds scoped SharePoint or OneDrive grounding | Explicit HTTPS URLs only; an empty list grants no SharePoint access |
| `teams_urls` | Adds scoped Teams message grounding | Explicit URLs only; maximum five |
| `email` | Adds read-only Outlook search | Must name an approved mailbox, group mailbox, or folder; `EmailActions` is never added |
| `people` | Adds organization people knowledge | Related content is off unless explicitly enabled |
| `web_search` | Adds public web grounding | Can be disabled for a tenant-only package |

Microsoft applies the signed-in user's existing permissions. Packaging a source does
not grant access to content the user cannot already access.

## Licensing and tenant prerequisites

Before tenant installation, confirm:

1. A development or test tenant allows custom-app upload.
2. Test users and representative nonproduction data are available.
3. The tenant has Microsoft 365 Copilot licenses or supported pay-as-you-go billing for
   SharePoint and connector grounding.
4. Users who need Outlook, People, Teams-message, or meeting knowledge have Microsoft
   365 Copilot licenses. Microsoft currently lists these as license-only capabilities.
5. An authorized administrator owns upload, app approval, assignment, availability,
   and retirement.
6. Business and data owners approve every SharePoint URL, mailbox, Teams location, and
   audience included in the package.

Sideloading for development is not organizational publication. Organization catalog
submission, admin approval, assignment, user installation, and Microsoft Marketplace
publication are separate states and must be recorded separately.

## Reporting and scheduling limits

Capture Team can prepare a Membership Development Briefing or Capture Brief, and
Proposal Team a Discovery Brief, assessment, draft, or QA report, during an interactive
run. Microsoft 365 admin reporting measures adoption and activity, not the business
accuracy or acceptance of those deliverables. Track business outcomes in an authorized
system of record with human review.

Scheduled tasks are created and owned by individual users in Microsoft Copilot. The
package cannot pre-create or silently activate a schedule. As of November 2026,
scheduled tasks require a Microsoft Copilot license, are managed in Copilot's Task Hub,
and support up to 10 active and 50 total schedules per user. They do not grant new data
permissions or authorize CRM writes, outreach, or other external actions.

Use a scheduled task only for read-only preparation such as a weekly briefing. Use a
separately governed workflow or Copilot Studio automation when deterministic background
execution, shared service identity, or system writes are required.

## Deployment gates

- Validate JSON structure, package paths, icon dimensions, skill count, package size,
  and absence of write-capable email access.
- Run Microsoft Validation Layer or Microsoft 365 Agents Toolkit validation against the
  exact ZIP intended for the tenant.
- Test named-user access, least-privilege source scoping, missing-data behavior,
  recommendation gates, and denial for an unauthorized user.
- Confirm the package does not send outreach, change a record, commit pricing, submit a
  proposal, or make a final pursuit, content, or submission decision without explicit
  human authorization.
- Record package checksum, tenant, audience, owner, approver, validation evidence,
  installation state, and rollback owner.

No repository build or local ZIP creation authorizes upload to a customer tenant.

## Deferred integration points (not implemented)

This package is deliberately scoped to an organization-neutral, web-search-only
declarative agent. The following are documented as future integration points and are
**not** implemented here:

- **Managed Teams MCP connector** -- a hosted MCP server exposing Compound Leverage's
  managed-service tooling to a declarative agent's actions. The plugin manifest
  (`runtimes[].type: RemoteMCPServer`) is the schema hook for this; it requires a
  hosted, authenticated MCP endpoint this public repository does not provide.
- **OAuth** -- the plugin manifest's `runtimes[].auth.type: OAuthPluginVault` is the
  schema hook for authenticated actions (as opposed to the current `None`/no-auth,
  read-only web-search capability). Wiring it up requires an Entra app registration
  and a live tenant, and is out of scope for the generic repository package.
- **Customer Brain** -- any customer-specific knowledge/memory layer would be supplied
  through a tenant's own `knowledge` grounding scopes (SharePoint, Graph connectors,
  embedded knowledge) in a private deployment configuration, not through this public
  package's canonical `_source/`.
- **Work wallet** -- any metering, billing, or entitlement tracking tied to agent usage
  is a tenant- or product-level concern outside this package's declarative-agent
  manifest and is not represented in the schema used here.

Adding any of these would move a package from "declarative agent calling public web
search" to "declarative agent calling a hosted, authenticated backend" -- a materially
different trust and operational boundary that needs its own review, not an incremental
field addition.

## Microsoft references

- [Declarative agent manifest v1.9](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/declarative-agent-manifest-1.9)
- [Microsoft 365 app packages](https://learn.microsoft.com/en-us/office/dev/add-ins/overview/app-package-for-microsoft-365)
- [Development and licensing prerequisites](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/prerequisites)
- [Publishing and sharing](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish)
- [Agent usage report](https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/microsoft-365-copilot-agents-new)
- [Scheduled prompts and tasks](https://learn.microsoft.com/en-us/copilot/manage/scheduled-prompts)
