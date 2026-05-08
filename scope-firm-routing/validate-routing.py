#!/usr/bin/env python3
"""
Routing validator. Confirms a firm's customer-cloud routing config
is correct before deployment.

Probes the gateway, confirms a Claude model is reachable, confirms
the auth flow works.

Usage:
  python3 scope-firm-routing/validate-routing.py \
    --config managed-agent-cookbooks/scope-dispatch-agent/agent.yaml

Stdlib only. The actual gateway probe (HTTPS call to Bedrock /
Vertex / Azure) is stubbed with a clear error message - the real
implementation calls the firm's gateway with the configured auth
and a small Claude prompt to confirm the round-trip works. Stub
mode prints what it would have done so the firm's IT team can
sanity-check the config without firing live calls.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

# Reuse the YAML reader from validate.py.
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from validate import load_yaml_minimal  # noqa: E402
except ImportError:
    print("validate-routing.py: could not import scripts/validate.py")
    sys.exit(1)


def probe_bedrock(orch: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for required in ("model_endpoint", "model_id", "region"):
        if not orch.get(required):
            issues.append(f"orchestrator.{required} is empty")
        elif "<FILL_IN>" in str(orch.get(required, "")):
            issues.append(f"orchestrator.{required} still has <FILL_IN> marker")
    auth = orch.get("auth") or {}
    if auth.get("type") != "iam_role":
        issues.append("orchestrator.auth.type must be 'iam_role' for bedrock")
    role_arn = auth.get("role_arn", "")
    if not role_arn or "<FILL_IN>" in str(role_arn):
        issues.append("orchestrator.auth.role_arn missing or unfilled")
    elif not re.match(r"^arn:aws:iam::\d{12}:role/", str(role_arn)):
        issues.append(f"orchestrator.auth.role_arn '{role_arn}' is not a valid IAM role ARN")
    return issues


def probe_vertex(orch: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for required in ("project_id", "location", "model_id"):
        if not orch.get(required):
            issues.append(f"orchestrator.{required} is empty")
        elif "<FILL_IN>" in str(orch.get(required, "")):
            issues.append(f"orchestrator.{required} still has <FILL_IN> marker")
    auth = orch.get("auth") or {}
    if auth.get("type") != "service_account":
        issues.append("orchestrator.auth.type must be 'service_account' for vertex_ai")
    sa = auth.get("service_account", "")
    if not sa or "<FILL_IN>" in str(sa):
        issues.append("orchestrator.auth.service_account missing or unfilled")
    return issues


def probe_azure(orch: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for required in ("endpoint", "deployment_name"):
        if not orch.get(required):
            issues.append(f"orchestrator.{required} is empty")
        elif "<FILL_IN>" in str(orch.get(required, "")):
            issues.append(f"orchestrator.{required} still has <FILL_IN> marker")
    auth = orch.get("auth") or {}
    if auth.get("type") != "entra_id":
        issues.append("orchestrator.auth.type must be 'entra_id' for azure_openai")
    for required in ("tenant_id", "client_id"):
        if not auth.get(required) or "<FILL_IN>" in str(auth.get(required, "")):
            issues.append(f"orchestrator.auth.{required} missing or unfilled")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()

    if not args.config.exists():
        print(f"validate-routing.py: config not found at {args.config}")
        sys.exit(1)

    data = load_yaml_minimal(args.config)
    orch = data.get("orchestrator") or {}
    provider = orch.get("provider")

    if provider not in ("bedrock", "vertex_ai", "azure_openai"):
        print(
            f"validate-routing.py: unknown or missing orchestrator.provider "
            f"'{provider}' (expected bedrock, vertex_ai, or azure_openai)"
        )
        sys.exit(1)

    print(f"validate-routing.py: probing {provider} routing config")
    if provider == "bedrock":
        issues = probe_bedrock(orch)
    elif provider == "vertex_ai":
        issues = probe_vertex(orch)
    else:
        issues = probe_azure(orch)

    if issues:
        for i in issues:
            print(f"  - {i}")
        print()
        print(f"validate-routing.py: {len(issues)} issue(s) - fix and re-run")
        sys.exit(1)

    print(
        "validate-routing.py: config shape passes. "
        "(Stub: live gateway probe is not wired in this scaffold; the "
        "real implementation calls the gateway with a small Claude "
        "prompt to confirm round-trip auth.)"
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
