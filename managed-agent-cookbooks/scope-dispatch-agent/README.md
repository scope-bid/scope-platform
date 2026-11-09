# Scope dispatch agent (managed-agent cookbook)

Headless deployment of the Scope dispatch agent via Anthropic's
`/v1/agents` (public beta). Same source as the Cowork plugin at
`../../plugins/agent-plugins/scope-dispatch-agent/`. The system
prompt at `agent.md` is one source of truth for both deployment
paths; the cookbook here wires the orchestrator + subagents +
steering events for headless use.

## What this is

A three-subagent orchestrator that takes a matter description and
stages quotes from professionals for the human's review:

- `matter-parser` parses the free-text matter into structured fields.
- `vendor-dispatcher` calls the right MCP server.
- `quote-formatter` renders the side-by-side view.

The orchestrator routes between them. SECURITY.md lists what waits
for a human commit event and which of those `agent.yaml` declares as
gates (awards, calendar bookings and roster changes). A dispatch does
not wait for one: with the default `award` setting, Scope chooses a
professional, and that award waits for a firm approver unless a firm
admin approved that spending in advance within set limits.

## When you use this path

You use the managed-agent runtime when:

- The agent runs server-side, not inside a developer's Cowork or
  Claude Code session.
- The firm's matter-management or claims-management UI calls the
  agent via API and renders the staged result inside its own
  interface.
- You want the orchestrator to handle long-running matters that span
  hours or days (parsing now, dispatch later after the lawyer
  reviews).

You use the Cowork plugin path instead when the lawyer or claims VP
is interacting with Claude directly (Claude Code, Claude.ai, Cowork
session), and the dispatch is fast and inline.

## Deploy

1. Confirm Anthropic `/v1/agents` access. As of 2026-05-08 this is
   public beta; verify your API key has the agents capability.
2. Confirm the MCP servers are reachable from your runtime. The
   legal MCP at `https://scope.bid/api/mcp/legal` is the live one;
   claims and AEC are preview.
3. Read the system prompt from
   `../../plugins/agent-plugins/scope-dispatch-agent/agent.md`.
4. POST the agent + subagent configs to `/v1/agents`. The
   subagents are listed in the `subagents` block of `agent.yaml`.
5. Wire the runtime's `handoff_request` event handler to your
   firm's matter-management or claims UI. Example payload at
   `steering-events/example-handoff.json`.

## Customer-cloud routing

If your firm is procurement-gated to a customer-cloud LLM gateway
(AWS Bedrock, Google Vertex AI, Azure OpenAI), point the
orchestrator's model endpoint at the gateway via the templates in
`../../scope-firm-routing/templates/`. The default deployment does
not need it.

## Voice rails

The agent and every subagent enforce the Scope voice canon:

- Quotes are returned, presented, shown. The human picks; the agent
  presents.
- ASCII hyphens. No em-dashes, no smart quotes, no ellipsis
  character.
- Sentence case for any pill, label, or status.

If the runtime UI surfaces any string the agent emitted, the same
rails apply on the firm's side. Run the lint script in
`../../scripts/lint-voice-canon.py` against any prompt or template
your firm authors before shipping.
