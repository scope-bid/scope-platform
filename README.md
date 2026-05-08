# Scope.bid

[![Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Lint](https://github.com/scope-bid/scope-platform/actions/workflows/lint.yml/badge.svg)](https://github.com/scope-bid/scope-platform/actions/workflows/lint.yml)
<!-- The marketplace badge below resolves once the official Anthropic
     listing approves. Until then it points at the submission docs. -->
[![Anthropic Marketplace](https://img.shields.io/badge/marketplace-pending-lightgrey.svg)](https://code.claude.com/docs/en/plugins)

The vertical-services MCP platform. Skills, slash commands, and agents
for legal, claims, and AEC vendor dispatch, installable inside Cowork
and Claude Code.

Scope is the layer your AI calls when it needs to hire a vendor in a
regulated industry. The platform packages auto-firing skills (matter
intake parsing, vendor dispatch, conflict-check workflow), slash
commands (`/scope-legal:dispatch`, `/scope-claims:ime`,
`/scope-aec:prequal`), and an end-to-end dispatch agent that takes a
matter description and stages vendor quotes for the lawyer's review.
Three verticals: legal services live, insurance claims preview in Q3
2026, AEC subcontractor preview in 2027. The cross-category
coordination thesis - one matter spans multiple vendor categories that
require different agencies - is the lead because that is where Scope's
value actually shows up. ABA Model Rules 5.4 and 7.2 sit underneath
every skill body and slash command; voice canon is enforced in CI by
`scripts/lint-voice-canon.py`.

Who's using it: mid-market plaintiff PI firms, workers comp plaintiff
firms, and insurance defense panel firms in the founding cohort.
In-house legal at mid-market companies and corporate legal deal teams
as the next-out cohort. Founding cohort opens Q3 2026 with twenty
partners per category nationally and MSA-level exclusivity per
category.

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
|  scope-legal (5 skills + 7 commands)   |
|  scope-claims (5 skills + 4 commands)  |
|  scope-aec (4 skills + 3 commands)     |
+----------------------------------------+
|  Layer 1: MCP servers                  |
|  scope-legal (live)                    |
|  scope-claims (preview, V2 Q3 2026)    |
|  scope-aec (preview, V3 2027)          |
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

Vendor agencies can ship their own plugin inside this marketplace.
See `plugins/partner-built/_README.md` for the contract, the lint
rails, and the submission flow. The example at
`plugins/partner-built/_example-partner-plugin/` is a working
reference.

## Headless / managed-agent use

The same dispatch agent runs headless via Anthropic's `/v1/agents`
public-beta runtime. The cookbook at
`managed-agent-cookbooks/scope-dispatch-agent/` ships the orchestrator
config, four leaf-worker subagents, and the human sign-off rail. See
its README for deployment.

## Customer-cloud routing

If your firm requires LLM traffic to stay inside your AWS account, GCP
project, or Azure tenant, see `scope-firm-routing/` for the install
templates and the routing validator. Forward-deployed for the AmLaw 200
procurement moment; not required for solo or mid-market.

## License

Apache 2.0. See `LICENSE`.
