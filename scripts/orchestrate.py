#!/usr/bin/env python3
"""
Reference event loop for the Managed Agent runtime.

This is a stub. Your firm's orchestration layer hooks here.

What this does:

  Reads steering events from stdin (one JSON object per line),
  routes them between the orchestrator and the leaf-worker
  subagents declared in agent.yaml, and emits handoff_request /
  handoff_commit events back on stdout.

What this does NOT do:

  - Call Anthropic's /v1/agents endpoint. The real runtime is
    Anthropic's; this script is a local development harness for
    walking through the event flow without spinning up the API.
  - Persist state. Every run starts fresh. Production runtime
    persists matter context, conflict-check results, and quote
    arrays in the firm's matter-management database.
  - Execute MCP calls. The real runtime has the MCP servers wired;
    this stub just logs the call signature it would have made.

To extend:

  1. Replace `route_event()` with a real router that calls
     Anthropic's API or your firm's gateway.
  2. Replace `dispatch_to_subagent()` with a real subagent
     invocation (LLM call with the subagent's system prompt and
     allowed_tools).
  3. Wire `emit_handoff_request()` to your firm's matter-management
     UI so the human can review and commit.

Stdlib only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
COOKBOOK = ROOT / "managed-agent-cookbooks" / "scope-dispatch-agent"


def log(msg: str) -> None:
    print(f"[orchestrate] {msg}", file=sys.stderr)


def route_event(event: dict[str, Any]) -> dict[str, Any]:
    """Route a steering event to the right subagent. Stub: routes
    based on event_type; the real implementation calls the
    orchestrator LLM with the agent.md system prompt and lets the
    model pick the subagent."""
    et = event.get("event_type")
    if et == "matter_intake":
        return dispatch_to_subagent("matter-parser", event)
    if et == "conflict_check":
        return dispatch_to_subagent("conflict-checker", event)
    if et == "vendor_dispatch":
        return dispatch_to_subagent("vendor-dispatcher", event)
    if et == "format_quotes":
        return dispatch_to_subagent("quote-formatter", event)
    if et == "handoff_commit":
        # Human committed a staged result; resume the loop. Real
        # runtime continues from where the orchestrator paused.
        return {"event_type": "ack", "resumed": True}
    return {
        "event_type": "error",
        "reason": f"unknown event_type: {et}",
    }


def dispatch_to_subagent(subagent: str, event: dict[str, Any]) -> dict[str, Any]:
    """Stub subagent invocation. Real impl: load subagent yaml,
    construct LLM call with system_prompt + allowed_tools, return
    the subagent's structured output."""
    log(f"would dispatch to subagent '{subagent}' with payload: {event}")
    return {
        "event_type": "subagent_invoked",
        "subagent": subagent,
        "stub": True,
        "note": (
            "Real runtime calls Anthropic /v1/agents with the "
            "subagent's system_prompt and allowed_tools."
        ),
    }


def emit_handoff_request(payload: dict[str, Any]) -> None:
    """Emit a handoff_request to stdout. The runtime forwards this to
    the firm's matter-management UI for human review."""
    print(json.dumps({"event_type": "handoff_request", "payload": payload}))


def main() -> None:
    if not COOKBOOK.exists():
        log(f"cookbook not found at {COOKBOOK}")
        sys.exit(1)
    log(f"orchestrating from {COOKBOOK}")
    log("reading steering events from stdin (one JSON object per line)")
    log("ctrl-D to exit")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as e:
            log(f"invalid JSON: {e}")
            continue
        result = route_event(event)
        print(json.dumps(result))


if __name__ == "__main__":
    main()
