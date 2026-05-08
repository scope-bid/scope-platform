# scope-platform

The vertical-services plugin marketplace for Scope. Skills, slash
commands, and agents that sit on top of the Scope MCP servers and
make vendor dispatch a one-line action inside Claude.

## What this is

Scope's MCP servers (`@scope-bid/scope-mcp`, `@scope-bid/scope-
claims-mcp`, `@scope-bid/scope-aec-mcp`) expose vendor-procurement
tools to any MCP-aware client. This repo is the layer above:
auto-fire skills that run when a lawyer, claims VP, GC, or deal
team describes a matter; slash commands the user can type into
Claude; and an end-to-end dispatch agent that takes a matter
description and stages vendor quotes for the human's review.

If you have used `anthropics/financial-services` as a reference,
the architecture mirrors it. Skills, commands, and agents on top
of MCP servers, packaged as plugins, distributed through a
marketplace manifest.

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

Layer 1 lives outside this repo, in the npm packages. Layer 2 and
Layer 3 live here.

## Install order

`scope-core` first. Every other plugin depends on it. Then the
verticals (`scope-legal`, `scope-claims`, `scope-aec`) in any
order. Then the agent plugin if you want the end-to-end
dispatch flow.

The marketplace manifest at `.claude-plugin/marketplace.json`
declares the install graph. Cowork or Claude Code reads it and
sequences the install.

## Customization

Every plugin is meant to be forked and adjusted. Three common
customization patterns:

- Swap connectors via `.mcp.json`. If you run Scope behind a
  customer-cloud LLM gateway or have a private MCP endpoint, point
  the URL there.
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
`managed-agent-cookbooks/scope-dispatch-agent/` ships the
orchestrator config, four leaf-worker subagents, and the human
sign-off rail. See its README for deployment.

## Customer-cloud routing

If your firm requires LLM traffic to stay inside your AWS account,
GCP project, or Azure tenant, see `scope-firm-routing/` for the
install templates and the routing validator. Forward-deployed for
the AmLaw 200 procurement moment; not required for solo or
mid-market.

## License

Apache 2.0. See `LICENSE`.
