# Scope firm routing

Use this when your firm is procurement-gated and requires LLM traffic
to stay inside your cloud. Not required for solo or mid-market
deployments.

This is the customer-cloud routing path. AmLaw 200 firms, large
defense panel firms, and carriers with strict BAA constraints often
require Claude calls to route through their own cloud-side LLM
gateway rather than Anthropic's public API. AWS Bedrock, Google
Vertex AI, and Azure OpenAI all expose Claude through that path.

This directory ships the install templates and a routing-validator
script so the firm's IT or platform team can wire the agent's
config to the firm's gateway in under an hour.

## When to use this

Use this path when any of these are true:

- Your firm requires LLM API traffic to stay inside the firm's AWS
  account, Google Cloud project, or Azure tenant for procurement,
  audit, or BAA reasons.
- The firm has a security review process that approves LLM gateways
  individually and Anthropic's public API has not been approved.
- The firm's data residency policy requires LLM traffic to land in
  a specific region (EU, Canada, US-only) that the firm's cloud
  account is configured for.

Do not use this path if:

- You are a solo, small-firm, or mid-market firm without a
  procurement-managed LLM gateway. The default Anthropic API path
  works for you and is faster to set up.
- You are running the agent inline inside a developer's Cowork or
  Claude Code session. Customer-cloud routing applies to the
  managed-agent runtime path (cookbook-based), not the inline path.

## What's in here

- `setup.md` - the admin walkthrough. How to point the agent's
  `agent.yaml` at the firm's gateway, how to configure auth, how to
  validate routing.
- `templates/agent-bedrock.yaml` - agent.yaml variant for AWS
  Bedrock routing. Drop in `model_endpoint` and IAM role.
- `templates/agent-vertex.yaml` - agent.yaml variant for Google
  Vertex AI routing. Drop in project ID and service account.
- `templates/agent-azure.yaml` - agent.yaml variant for Azure
  OpenAI routing. Drop in deployment name and Entra ID auth.
- `validate-routing.py` - confirms a firm's routing config is
  correct before deployment. Probes the gateway, confirms a
  Claude model is reachable, confirms the auth flow works.

## What this does not change

The agent's behavior, voice canon, ABA rails, and human sign-off
gates are identical regardless of routing path. The only thing that
changes is where the LLM call lands. Skills, slash commands, MCP
connectors, and steering events all behave the same way.

## Forward-deployed

This is forward-deployed for the AmLaw moment. The founder-led wedge
today (mid-market plaintiff PI, workers comp plaintiff, defense
panel) does not need this. It ships now so firms with mature
procurement teams can integrate Scope without a separate engagement.
