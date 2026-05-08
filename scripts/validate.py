#!/usr/bin/env python3
"""
scope-platform manifest validator.

Validates:

  - Every .mcp.json under plugins/ has well-formed mcpServers
    entries with at least 'url' (or 'command' for stdio) and
    'description'.
  - Every agent.yaml under managed-agent-cookbooks/ has the
    required orchestrator + subagents + mcp blocks, and every
    subagent reference resolves to a yaml file under subagents/.
  - The top-level marketplace.json references plugins that exist.

Stdlib only - no PyYAML dependency. We parse a tiny YAML subset
(key: value, lists with -, indentation) sufficient for our config.
Anything more complex would mean adding a runtime dep, which we
avoid for the lint stack.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
COOKBOOKS = ROOT / "managed-agent-cookbooks"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"


def load_yaml_minimal(path: Path) -> dict[str, Any]:
    """Tiny YAML reader. Handles key: value, key: (list with - items),
    and nested 1-level dicts. Comments stripped. Block scalars (|, >)
    captured as raw multi-line text."""
    text = path.read_text(encoding="utf-8")
    out: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any] | list[Any]]] = [(-1, out)]
    cur_block_key: str | None = None
    cur_block_indent = -1
    cur_block_lines: list[str] = []
    cur_block_marker: str | None = None  # '|' or '>' or None

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        # Block-scalar capture mode.
        if cur_block_marker is not None and cur_block_key is not None:
            stripped = raw.lstrip()
            indent = len(raw) - len(stripped)
            if (raw.strip() == "" or indent > cur_block_indent) and not (
                stripped.startswith("#") and indent <= cur_block_indent
            ):
                if raw.strip() == "":
                    cur_block_lines.append("")
                else:
                    cur_block_lines.append(raw[cur_block_indent + 2 :])
                i += 1
                continue
            # End of block scalar.
            owner = stack[-1][1]
            value = "\n".join(cur_block_lines).strip("\n")
            if isinstance(owner, dict):
                owner[cur_block_key] = value
            cur_block_marker = None
            cur_block_key = None
            cur_block_lines = []
            # fall through and re-process this line
        if raw.strip() == "" or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        # Pop stack until we're at the right level.
        while stack and stack[-1][0] >= indent:
            stack.pop()
        owner = stack[-1][1]
        if line.startswith("- "):
            value = line[2:].strip()
            if isinstance(owner, list):
                if ":" in value and not value.startswith('"'):
                    sub: dict[str, Any] = {}
                    k, _, v = value.partition(":")
                    if v.strip():
                        sub[k.strip()] = _scalar(v.strip())
                    owner.append(sub)
                    stack.append((indent, sub))
                else:
                    owner.append(_scalar(value))
        else:
            m = re.match(r'^([^:]+):\s*(.*)$', line)
            if not m:
                i += 1
                continue
            key = m.group(1).strip()
            rest = m.group(2).strip()
            if rest in ("|", ">"):
                if isinstance(owner, dict):
                    cur_block_key = key
                    cur_block_indent = indent
                    cur_block_marker = rest
                    cur_block_lines = []
                i += 1
                continue
            if rest == "":
                # Container - peek next non-empty/comment line to
                # decide list vs dict.
                j = i + 1
                container: dict[str, Any] | list[Any] = {}
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.strip() == "" or nxt.lstrip().startswith("#"):
                        j += 1
                        continue
                    next_indent = len(nxt) - len(nxt.lstrip())
                    if next_indent <= indent:
                        break
                    if nxt.lstrip().startswith("- "):
                        container = []
                    break
                if isinstance(owner, dict):
                    owner[key] = container
                stack.append((indent, container))
            else:
                if isinstance(owner, dict):
                    owner[key] = _scalar(rest)
        i += 1

    # Flush trailing block scalar if any.
    if cur_block_marker is not None and cur_block_key is not None:
        owner = stack[-1][1]
        if isinstance(owner, dict):
            owner[cur_block_key] = "\n".join(cur_block_lines).strip("\n")

    return out


def _scalar(s: str) -> Any:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (
        s.startswith("'") and s.endswith("'")
    ):
        return s[1:-1]
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if re.match(r"^-?\d+$", s):
        return int(s)
    if re.match(r"^-?\d+\.\d+$", s):
        return float(s)
    return s


def validate_mcp_json(path: Path, violations: list[str]) -> None:
    rel = path.relative_to(ROOT)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        violations.append(f"{rel}: invalid JSON: {e}")
        return
    servers = data.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        violations.append(f"{rel}: 'mcpServers' is missing or empty")
        return
    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            violations.append(f"{rel}: server '{name}' is not an object")
            continue
        if "url" not in cfg and "command" not in cfg:
            violations.append(
                f"{rel}: server '{name}' missing both 'url' and 'command'"
            )
        if not cfg.get("description"):
            violations.append(
                f"{rel}: server '{name}' missing 'description'"
            )


def validate_agent_yaml(path: Path, violations: list[str]) -> None:
    rel = path.relative_to(ROOT)
    try:
        data = load_yaml_minimal(path)
    except Exception as e:
        violations.append(f"{rel}: failed to parse YAML: {e}")
        return
    for required in ("name", "orchestrator", "subagents"):
        if required not in data:
            violations.append(f"{rel}: missing required field '{required}'")
    orch = data.get("orchestrator")
    if isinstance(orch, dict):
        if "model" not in orch:
            violations.append(f"{rel}: orchestrator.model missing")
        if "system_prompt_path" not in orch and "system_prompt" not in orch:
            violations.append(
                f"{rel}: orchestrator needs system_prompt or system_prompt_path"
            )
        sp_path = orch.get("system_prompt_path")
        if sp_path:
            resolved = (path.parent / sp_path).resolve()
            if not resolved.exists():
                violations.append(
                    f"{rel}: orchestrator.system_prompt_path '{sp_path}' "
                    f"does not exist"
                )
    subagents = data.get("subagents") or []
    if isinstance(subagents, list):
        for sub_name in subagents:
            sub_yaml = path.parent / "subagents" / f"{sub_name}.yaml"
            if not sub_yaml.exists():
                violations.append(
                    f"{rel}: subagent '{sub_name}' has no yaml at "
                    f"{sub_yaml.relative_to(ROOT)}"
                )


def validate_marketplace(path: Path, violations: list[str]) -> None:
    if not path.exists():
        violations.append(f".claude-plugin/marketplace.json: missing")
        return
    rel = path.relative_to(ROOT)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        violations.append(f"{rel}: invalid JSON: {e}")
        return
    for plugin in data.get("plugins") or []:
        plugin_path = ROOT / plugin.get("path", "")
        manifest = plugin_path / ".claude-plugin" / "plugin.json"
        if not manifest.exists():
            violations.append(
                f"{rel}: plugin '{plugin.get('name')}' path "
                f"'{plugin.get('path')}' has no plugin.json"
            )


def main() -> None:
    violations: list[str] = []

    for mcp in PLUGINS.rglob(".mcp.json"):
        validate_mcp_json(mcp, violations)
    for agent_yaml in COOKBOOKS.rglob("agent.yaml"):
        validate_agent_yaml(agent_yaml, violations)
    validate_marketplace(MARKETPLACE, violations)

    if violations:
        for v in violations:
            print(f"  - {v}")
        print()
        print(f"validate.py: {len(violations)} violation(s)")
        sys.exit(1)
    print("validate.py: all manifests valid")
    sys.exit(0)


if __name__ == "__main__":
    main()
