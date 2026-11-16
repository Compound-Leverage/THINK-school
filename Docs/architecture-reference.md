# Where this fits

THINK-school is the free, public tier of Compound Leverage's Digital Employee
distribution. It never connects to CL's proprietary MCP — everything here is
bring-your-own-data.

Full architecture reference (all three repos, MCP tools, entitlement model) lives in
Compound Leverage's private internal documentation and is not published in this repo.

The released plugin roots are generated artifacts. Keep organization-specific data in
the supported in-package templates or authorized session context, and preserve a copy
outside an installed plugin cache before updating. Third-party Claude marketplaces do
not auto-update by default; users may enable auto-update or run an explicit update.
OpenAI and Anthropic directory publication have separate review and update gates. See
[distribution and release parity](distribution-and-release.md).
