# Setup walkthrough: routing the Scope dispatch agent through your
firm's LLM gateway

This walkthrough assumes you have:

- An AWS, GCP, or Azure account with a Claude-capable LLM endpoint
  configured (Bedrock, Vertex AI, or Azure OpenAI).
- IAM or service-account credentials with permission to invoke the
  Claude model on that endpoint.
- A copy of the scope-platform repo at the firm's source-control
  location.

## Step 1. Pick the right template

Three templates ship in `templates/`:

- `agent-bedrock.yaml` for AWS Bedrock
- `agent-vertex.yaml` for Google Vertex AI
- `agent-azure.yaml` for Azure OpenAI

Copy the right one over the cookbook's default `agent.yaml`:

```
cp scope-firm-routing/templates/agent-bedrock.yaml \
   managed-agent-cookbooks/scope-dispatch-agent/agent.yaml
```

Each template has the `orchestrator.model` block pre-configured for
that gateway. The rest of the agent config (subagents, MCP, human
gates) is identical to the default.

## Step 2. Fill in the auth fields

Each template has placeholder fields that need your gateway-specific
values. Look for `<FILL_IN>` markers.

For Bedrock:

- `model_endpoint`: the regional Bedrock endpoint
  (e.g., `https://bedrock-runtime.us-east-1.amazonaws.com`)
- `model_id`: the Claude model ARN or alias
  (e.g., `anthropic.claude-sonnet-4-5-v1:0` or your firm's
  cross-account inference profile)
- `auth.role_arn`: the IAM role the agent assumes
  (e.g., `arn:aws:iam::123456789012:role/scope-dispatch-agent`)

For Vertex AI:

- `project_id`: the GCP project that hosts the Claude model
- `location`: the region the model is deployed to
  (e.g., `us-east5`)
- `model_id`: the Vertex model name
  (e.g., `claude-sonnet-4-5@20251201`)
- `auth.service_account`: the service account email

For Azure OpenAI:

- `endpoint`: the Azure OpenAI endpoint URL
- `deployment_name`: the Azure deployment that proxies to Claude
  (some firms use a custom deployment name)
- `auth.tenant_id`, `auth.client_id`: Entra ID app registration
  for the agent

## Step 3. Validate

Run the routing validator:

```
python3 scope-firm-routing/validate-routing.py \
  --config managed-agent-cookbooks/scope-dispatch-agent/agent.yaml
```

The validator probes the gateway, confirms the Claude model is
reachable, and confirms the auth flow works. Exit code 0 on success.

If validation fails, the script prints the failing field and the
gateway's error response. Common issues:

- IAM role does not have `bedrock:InvokeModel` permission.
- The Vertex AI service account does not have
  `roles/aiplatform.user`.
- Azure OpenAI deployment is paused or the model version has been
  deprecated.

## Step 4. Deploy

Once validation passes, deploy the cookbook to your runtime per the
managed-agent README at `managed-agent-cookbooks/scope-dispatch-
agent/README.md`. The agent's behavior is identical; only the LLM
call routes through your gateway.

## Step 5. Observability

Two places log the agent's traffic:

- Your gateway. Bedrock CloudWatch, Vertex AI Cloud Logging, or
  Azure Application Insights captures every model call. Use those
  for audit, cost, and rate-limit review.
- Your matter-management or claims system. Every steering event
  the agent emits is logged with the matter ID and the human's
  commit decision. Use that for ABA-rails audit and sign-off
  review.

## Troubleshooting

- The agent times out on every call. Check the gateway's network
  policy. The agent makes outbound HTTPS calls to the MCP servers
  at `scope.bid/api/mcp/*`; that traffic must be allowed.
- The agent reports an MCP-tool failure. The MCP servers run on
  Scope's infrastructure, not yours. Confirm Scope's status page
  shows the legal MCP as live.
- The agent halts on every conflict check. Either the firm's
  conflict database returns false positives, or the agent's
  conflict-checker subagent is misrouted. Re-run validation with
  a known-clear matter.
