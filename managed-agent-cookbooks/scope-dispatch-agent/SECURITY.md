# Security model: human sign-off rail

The agent presents; people at the firm decide. The actions listed
below are meant to wait for a human commit event from the runtime;
the note after the second list says which ones `agent.yaml` gates.
Spending is also gated on Scope's server: every award waits for a firm
approver at scope.bid/approvals, unless a firm admin approved that
spending in advance within set limits.

## What the agent NEVER does without human commit

The orchestrator halts and emits a `handoff_request` steering event
for every one of these. The runtime forwards the event to the firm's
review UI; the human approves, revises, or abandons; the runtime
emits `handoff_commit` back to resume the loop.

- Award a professional's quote with `scope_award_matter`. The lawyer
  or claims VP names the professional.
- Book a calendar slot with the awarded professional. The human
  approves the booking, including date, location, and any logistics
  riders.
- Modify the firm's roster (promote primary, demote to backup,
  exclude). The human commits each change.
- Work around the dispatch-time conflict gate. The gate runs
  server-side on `scope_dispatch_matter` dispatches, excluding
  professionals with declared relationships to the matter's named
  parties; the agent never attempts to clear it, override it, or
  steer an award toward a professional it excluded.
- Send any external communication (email a professional, dispatch a
  records authorization, file a subpoena). The agent stages the
  draft; the human sends.

## What the agent DOES autonomously

- Read the matter description.
- Parse it into structured fields.
- Call `scope_dispatch_matter`. With the default `award` setting,
  Scope chooses a professional by the firm's roster and price when it
  can, and the award waits for a firm approver unless a firm admin
  approved that spending in advance within set limits. The reply can
  instead ask for missing work-order details or say that no
  professional was returned.
- Format quotes side by side.
- Wait for the human.

The agent never releases an approval and never works around the
dispatch-time conflict gate.

`human_gates` in `agent.yaml` declares the award, calendar and roster
gates. It does not gate outside messages, and the orchestrator can
reach Scope tools that notify a professional by email (a reschedule
does). Add a runtime gate for outside messages if your deployment
needs one.

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
