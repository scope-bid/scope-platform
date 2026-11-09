<p align="center">
  <img src="https://scope.bid/brand/scope-wordmark-300.png?v=20260508" alt="Scope" width="300">
</p>

# Scope.bid

[![Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Lint](https://github.com/scope-bid/scope-platform/actions/workflows/lint.yml/badge.svg)](https://github.com/scope-bid/scope-platform/actions/workflows/lint.yml)

The vertical-services MCP platform. Skills, slash commands, and agents
for dispatching professionals, installable inside Cowork and Claude
Code.

Scope is the layer your AI calls when it needs to engage a professional
in a regulated industry. The platform packages auto-firing skills
(`matter-intake-parsing`, `vendor-dispatch`, `quote-comparison`),
slash commands (`/scope-legal:dispatch`, `/scope-legal:depo`,
`/scope-claims:ime`), and an end-to-end dispatch agent that takes a
matter description and stages quotes from professionals for the
lawyer's review. The legal plugins run against Scope's live legal MCP
server; the claims and AEC plugins are previews. House wording rules
are enforced in CI by `scripts/lint-voice-canon.py`.

Scope is live in production with demo mode available, and it is
opening to its first firms and professionals now.

## Install

New here? Try the live demo in 60 seconds: see [DEMO.md](DEMO.md).
The plugin ships with demo mode enabled, so you'll see realistic
seeded responses immediately - no signup required.

```
/plugin marketplace add github.com/scope-bid/scope-platform
/plugin install scope-core@scope-bid
/plugin install scope-legal@scope-bid
/plugin install scope-dispatch-agent@scope-bid
```

## Architecture (three layers)

```
+----------------------------------------+
|  Layer 3: Agents                       |
|  scope-dispatch-agent (Cowork plugin)  |
|  scope-dispatch-agent (managed cookbook)|
+----------------------------------------+
|  Layer 2: Skills + slash commands      |
|  scope-core (5 shared skills)          |
|  scope-legal (5 skills + 6 commands)   |
|  scope-claims (5 skills + 4 commands)  |
|  scope-aec (5 skills + 4 commands)     |
+----------------------------------------+
|  Layer 1: MCP servers                  |
|  scope-legal (live)                    |
|  scope-claims (preview)                |
|  scope-aec (preview)                   |
+----------------------------------------+
```

Layer 1 lives outside this repo, in the npm packages and the Anthropic
MCP Registry under `bid.scope`. Layer 2 and Layer 3 live here.

## Install order

`scope-core` first. Every other plugin depends on it. Then the
verticals (`scope-legal`, `scope-claims`, `scope-aec`) in any order.
Then the agent plugin if you want the end-to-end dispatch flow.

The marketplace manifest at `.claude-plugin/marketplace.json` declares
the install graph. Cowork or Claude Code reads it and sequences the
install.

## Customization

Every plugin is meant to be forked and adjusted:

- Swap connectors via `.mcp.json`. If your firm runs Scope behind a
  customer-cloud LLM gateway or a private MCP endpoint, point the URL
  there.
- Swap skills. Each skill is a markdown file with frontmatter; edit
  the prose body to match your firm's preferred phrasing or add
  firm-specific guardrails.
- Fork agents. Copy `plugins/agent-plugins/scope-dispatch-agent/`
  into your firm's repo and adjust the system prompt, the bundled
  skills, and the human-gate list.

## Partner plugins

`plugins/partner-built/_README.md` documents the manifest contract,
the lint rules, and the pull request flow for plugins built by
outside teams. The example at
`plugins/partner-built/_example-partner-plugin/` is a working
reference.

## Headless / managed-agent use

The same dispatch agent runs headless via Anthropic's `/v1/agents`
public-beta runtime. The cookbook at
`managed-agent-cookbooks/scope-dispatch-agent/` ships the orchestrator
config, three leaf-worker subagents, and the human sign-off rail. See
its README for deployment.

## Multi-agent orchestration: parallel dispatch on one matter

Claude Managed Agents (Anthropic public beta, shipped 2026-05-07)
lets a coordinator agent split work across specialist sub-agents in
parallel on a shared session. Scope is designed to be on the
receiving end of that fan-out: each sub-agent dispatches a different
service category to bid.scope/legal at the same time, and the
coordinator consolidates the responses.

### When to reach for this pattern

When a single matter triggers multiple service needs at once. New PI
case intake is the canonical example: serve the defendant, pull
records, schedule an IME, book a court reporter for the deposition.
Running the categories in parallel returns the whole intake in a
single coordinator response instead of one category at a time.

### Example: new PI matter intake

Four specialist agents, one coordinator. Each specialist owns one
service category and connects to the bid.scope/legal MCP server. The
coordinator fans the work out, the specialists run on independent
session threads, and the coordinator consolidates their structured
payloads into a single status card.

API source:
[platform.claude.com/docs/en/managed-agents/multi-agent](https://platform.claude.com/docs/en/managed-agents/multi-agent).
All Managed Agents requests carry the `managed-agents-2026-04-01`
beta header (the SDK adds it automatically).

```python
from anthropic import Anthropic

client = Anthropic()

SCOPE_MCP = {
    "type": "url",
    "url": "https://scope.bid/api/mcp/legal",
    "name": "scope-legal",
    "authorization_token": "scope_pk_demo_2026",
}

# Four specialist sub-agents, one per service category. Each one's
# only job is to invoke scope_dispatch_matter (or scope_book_deposition)
# for its category and return the structured quote payload verbatim.
service_agent = client.beta.agents.create(
    name="service-dispatch",
    model="claude-sonnet-4-7",
    system=(
        "You dispatch process-server requests to bid.scope/legal. "
        "Given a defendant name, service address, and jurisdiction, "
        "call scope_dispatch_matter with vendor_type='process_server' "
        "and return the structured quote payload verbatim. Do not "
        "summarize. Do not pick a professional."
    ),
    mcp_servers=[SCOPE_MCP],
)

records_agent = client.beta.agents.create(
    name="records-dispatch",
    model="claude-sonnet-4-7",
    system=(
        "You dispatch medical-records retrieval requests to "
        "bid.scope/legal. Given a patient name, custodian, and date "
        "range, call scope_dispatch_matter with "
        "vendor_type='records_retrieval' and return the structured "
        "quote payload verbatim. Do not summarize. Do not pick a "
        "professional."
    ),
    mcp_servers=[SCOPE_MCP],
)

ime_agent = client.beta.agents.create(
    name="ime-dispatch",
    model="claude-sonnet-4-7",
    system=(
        "You dispatch independent-medical-exam requests to "
        "bid.scope/legal. Given a patient name and injury type, "
        "call scope_dispatch_matter with vendor_type='ime' and "
        "return the structured quote payload verbatim. Do not "
        "summarize. Do not pick an examiner."
    ),
    mcp_servers=[SCOPE_MCP],
)

depo_agent = client.beta.agents.create(
    name="depo-dispatch",
    model="claude-sonnet-4-7",
    system=(
        "You dispatch court-reporter bookings to bid.scope/legal. "
        "Given a deposition date and jurisdiction, call "
        "scope_book_deposition and return the structured quote "
        "payload verbatim. Do not summarize. Do not pick a "
        "professional."
    ),
    mcp_servers=[SCOPE_MCP],
)

# Coordinator: owns the user-facing intake prompt, parses the matter,
# delegates to the four specialists in parallel, consolidates results.
coordinator = client.beta.agents.create(
    name="pi-intake-coordinator",
    model="claude-opus-4-7",
    system=(
        "You handle new personal-injury matter intake for a "
        "plaintiff firm. When the user names a new case, parse the "
        "four standard needs (service, records, IME, court "
        "reporter) from their message and delegate each to the "
        "relevant specialist agent. The four specialists run in "
        "parallel. When all four return, consolidate their quote "
        "payloads into a single status card with one line per "
        "service category. Surface the lowest-total quote and the "
        "fastest-availability quote per category as factual flags, "
        "never as a pick. The lawyer awards; you present."
    ),
    tools=[{"type": "agent_toolset_20260401"}],
    multiagent={
        "type": "coordinator",
        "agents": [
            {"type": "agent", "id": service_agent.id},
            {"type": "agent", "id": records_agent.id},
            {"type": "agent", "id": ime_agent.id},
            {"type": "agent", "id": depo_agent.id},
        ],
    },
)

# Open a session against the coordinator and send the intake message.
session = client.beta.sessions.create(
    agent=coordinator.id,
    environment_id=ENVIRONMENT_ID,
)

client.beta.sessions.events.send(
    session.id,
    events=[{
        "type": "user.message",
        "content": (
            "I just signed a new PI case in Sacramento for a "
            "rear-end collision. Plaintiff is Maria Santos, "
            "defendant is Robert Chen. Can you get everything "
            "moving - serve the defendant, pull medical records "
            "from Sample Medical Center (example), schedule an IME, "
            "and book a court reporter for the depo on June 15?"
        ),
    }],
)
```

### What the coordinator returns

A consolidated status card across all four parallel dispatches.
Sketch with sample data - every name is coined and nothing below is a
real dispatch (exact rendering depends on whether the host surface
honors Scope's `display_widget` HTML):

```
Four dispatches fired against bid.scope/legal in parallel.

[Process server]    matter SC-EXAMPLE-1    5 quotes returned
  Lowest:   Example Process Service (example)    $185 flat
  Fastest:  Sample Serve Co. (example)           24-hour rush available

[Records retrieval]  matter SC-EXAMPLE-2    4 quotes returned
  Lowest:   Sample Records Retrieval (example)   $325 + $0.10/page
  HIPAA-compliant custodian handling confirmed across all four

[IME (orthopedic)]   matter SC-EXAMPLE-3    5 quotes returned
  Lowest:   Example IME Group (example)          $1,950 / 90-min exam
  Earliest available: 2026-06-09, Sample IME Practice (example)

[Court reporter, deposition 2026-06-15]
                     matter SC-EXAMPLE-4    5 quotes returned
  Lowest:   Sample Court Reporting (example)     $325/hr + transcript
  All five professionals confirmed availability on the requested date

Ready to request the awards. Reply "request all lowest" or "request
[professional] for [matter]" - each request parks as a pending
approval, and a firm approver releases it from scope.bid/approvals.
```

### Why this composes cleanly

Each sub-agent owns one service category and one MCP tool surface.
No coordination overhead at the prompt layer. Scope's HTTP transport
handles four simultaneous requests cleanly because each is an
independent JSON-RPC call against bid.scope/legal with no shared
state. The coordinator gets back four structured payloads and
renders a single status card.

The pattern extends: when a matter spans more than four service
categories (e.g., a multi-vehicle accident that adds translation
services, life-care planning, and accident reconstruction), add
more specialist sub-agents to the coordinator's roster.
`multiagent.agents` accepts up to 20 unique agents, and the
coordinator can spawn multiple instances of any one of them, up to
25 concurrent threads per session.

### Notes and limits

- The Managed Agents beta header (`managed-agents-2026-04-01`) is
  required on every request. The SDK sets it automatically.
- Coordinator depth is one level. A specialist sub-agent cannot
  spawn its own sub-agents.
- A specialist can hold its own MCP servers, skills, and tools
  scoped to its category. The coordinator only needs the agent
  toolset.
- The example above uses the public `scope_pk_demo_2026` token so
  any developer can run it end-to-end without a Scope account. Swap
  in your production token (issued at scope.bid/settings) for live
  dispatches.

## Customer-cloud routing

If your firm requires LLM traffic to stay inside your AWS account, GCP
project, or Azure tenant, see `scope-firm-routing/` for the install
templates and the routing validator. The default install does not
need it.

## License

Apache 2.0. See `LICENSE`.
