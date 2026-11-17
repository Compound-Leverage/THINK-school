# Microsoft 365 Copilot distribution and governance

Capture Team ships as an installable Microsoft 365 app package. The package contains a
Microsoft 365 Copilot declarative agent and a generated Capture Team Agent Skill. It
does not require a hosted bot or a separate Compound Leverage runtime.

## Why this packaging model

Microsoft 365 declarative agent schema v1.9 can reference Agent Skill directories
directly. That lets this package reuse the same canonical Capture Team workflow and
role content that generate the Claude and OpenAI packages. A custom-engine agent would
add an independently hosted runtime and is not required for the current research,
qualification, and briefing workflow.

The source of truth remains `Plugins/capture-team/_source/`. Do not hand-edit the
generated `Plugins/capture-team/microsoft365/` directory.

## Package contents

- `manifest.json`: Microsoft 365 app manifest v1.30.
- `declarativeAgent.json`: declarative agent manifest v1.9.
- `skills/capture-team/`: shared Capture Team skill, role references, and runtime
  configuration.
- `color.png` and `outline.png`: required 192 x 192 and 32 x 32 package icons.
- `deployment-config.example.json`: private tenant-configuration template.

The generic release package enables web search only. It is useful for package
validation and organization-neutral use. A customer build can add only the approved
SharePoint, Teams, read-only Outlook, and People scopes declared in its private
deployment configuration.

## Build and install

Build the generic installable package:

```bash
python3 scripts/build_plugins.py --team capture-team --check
python3 scripts/validate_release.py
python3 scripts/build_release_packages.py
```

The output is `release-packages/capture-team-microsoft365-v<VERSION>.zip`. The ZIP has
`manifest.json` at its root as Microsoft 365 requires.

For a customer-configured build, copy the example configuration outside the public
repository, replace or remove every placeholder, and run:

```bash
python3 scripts/build_microsoft365_package.py \
  --config /private/path/deployment-config.json \
  --output-dir release-packages/customer
```

Do not commit the private configuration or tenant package. Upload and assignment must
be performed by an authorized tenant administrator after nonproduction validation.

## Configuration model

`my-capture-config.json` defines the shared pursuit workflow. Its `pursuit_types.active`
value selects business development, government contracting, grant funding, or
membership development without forking the core skill. Each type can use its own
qualification profile and deliverable label.

The private Microsoft deployment configuration controls tenant capabilities:

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

The plugin can prepare a Membership Development Briefing or Capture Brief during an
interactive run. Microsoft 365 admin reporting measures adoption and activity, not the
business accuracy or acceptance of those briefs. Track business outcomes in an
authorized system of record with human review.

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
- Confirm the package does not send outreach, change a record, or make the final pursuit
  decision without explicit human authorization.
- Record package checksum, tenant, audience, owner, approver, validation evidence,
  installation state, and rollback owner.

No repository build or local ZIP creation authorizes upload to a customer tenant.

## Microsoft references

- [Declarative agent manifest v1.9](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/declarative-agent-manifest-1.9)
- [Microsoft 365 app packages](https://learn.microsoft.com/en-us/office/dev/add-ins/overview/app-package-for-microsoft-365)
- [Development and licensing prerequisites](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/prerequisites)
- [Publishing and sharing](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/publish)
- [Agent usage report](https://learn.microsoft.com/en-us/microsoft-365/admin/activity-reports/microsoft-365-copilot-agents-new)
- [Scheduled prompts and tasks](https://learn.microsoft.com/en-us/copilot/manage/scheduled-prompts)
