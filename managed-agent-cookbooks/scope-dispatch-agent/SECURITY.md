# Security model: human sign-off rail

Scope drafts; the human commits. Every action this agent takes that
affects the firm, the claim file, the matter file, the calendar, or
the vendor relationship is gated on a human commit event from the
runtime.

## What the agent NEVER does without human commit

The orchestrator halts and emits a `handoff_request` steering event
for every one of these. The runtime forwards the event to the firm's
review UI; the human approves, revises, or abandons; the runtime
emits `handoff_commit` back to resume the loop.

- Award a vendor quote. The lawyer or claims VP picks the vendor.
- Book a calendar slot with the awarded vendor. The human approves
  the booking, including date, location, and any logistics riders.
- Modify the firm's roster (promote primary, demote to backup,
  exclude). The human commits each change.
- Override a conflict-check hit. Conflict-check overrides require an
  informed-consent workflow that lives outside this agent. The
  agent halts on a conflict hit; the runtime routes the override
  workflow to the firm's ethics or general counsel.
- Send any external communication (email a vendor, dispatch a
  records authorization, file a subpoena). The agent stages the
  draft; the human sends.

## What the agent DOES autonomously

- Read the matter description.
- Parse it into structured fields.
- Query the conflict database (read only).
- Call MCP dispatch tools in dry-run mode (commit=false) to surface
  available quotes.
- Format quotes side by side.
- Wait for the human.

The agent never moves money, never confirms an award, never sends an
external email or calendar invite, never modifies a roster, never
overrides a conflict.

## ABA Model Rule alignment

Two rules sit underneath the rail:

- **Rule 5.4 (independence of professional judgment).** The lawyer's
  judgment on whom to retain stays the lawyer's. The agent surfaces
  factual fields; the lawyer weighs and decides.
- **Rule 7.2 (referrals and recommendations).** The agent does not
  recommend. Quotes are returned and presented. The lawyer's bar
  counsel can read every transcript without finding a Rule 7.2
  violation.

## Audit trail

Every steering event the orchestrator emits is logged with:

- Timestamp (UTC, ISO 8601)
- Agent version (from `plugin.json`)
- Subagent that produced the staged result
- The matter ID or claim file ID
- The full payload (parsed matter, conflict check, quotes)
- The human action taken (commit, revise, abandon)
- The committing user's identity (from the runtime's auth)

The audit trail lives with the firm's matter-management or claims
system. Scope does not retain it; the firm owns it.

## Customer-cloud routing

When the firm is routing through a customer-cloud LLM gateway
(`scope-firm-routing/`), the model endpoint inside the agent's
config points at the gateway, not at Anthropic's API. The audit
trail expectations stay the same; the gateway handles the data
residency and the BAA constraints.
