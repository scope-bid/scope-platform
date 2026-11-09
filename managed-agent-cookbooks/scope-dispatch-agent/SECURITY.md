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
- Work around the dispatch-time conflict gate. The gate runs
  server-side on `scope_dispatch_matter` dispatches, excluding
  vendors with declared relationships to the matter's named parties;
  the agent never attempts to clear it, override it, or steer an
  award toward a vendor it excluded.
- Send any external communication (email a vendor, dispatch a
  records authorization, file a subpoena). The agent stages the
  draft; the human sends.

## What the agent DOES autonomously

- Read the matter description.
- Parse it into structured fields.
- Call MCP dispatch tools in dry-run mode (commit=false) to surface
  available quotes.
- Format quotes side by side.
- Wait for the human.

The agent never moves money, never confirms an award, never sends an
external email or calendar invite, never modifies a roster, never
works around the dispatch-time conflict gate.

## Presentation rules

- The lawyer's judgment on whom to engage stays the lawyer's. The
  agent surfaces factual fields; the lawyer weighs and decides.
- Quotes are returned and presented. The agent does not pick one or
  label one as the right choice.

## Audit trail

Every steering event the orchestrator emits is logged with:

- Timestamp (UTC, ISO 8601)
- Agent version (from `plugin.json`)
- Subagent that produced the staged result
- The matter ID or claim file ID
- The full payload (parsed matter, conflict gate result, quotes)
- The human action taken (commit, revise, abandon)
- The committing user's identity (from the runtime's auth)

This steering-event log lives with the firm's matter-management or
claims system, and the firm owns it. It is separate from the record
Scope's own servers keep of MCP tool calls and matter activity.

## Customer-cloud routing

When the firm is routing through a customer-cloud LLM gateway
(`scope-firm-routing/`), the model endpoint inside the agent's
config points at the gateway, not at Anthropic's API. The audit
trail expectations stay the same; the gateway handles the data
residency and the BAA constraints.
