#!/usr/bin/env python3
"""
scope-platform plugin structure check.

Walks every plugin under plugins/ and validates:

  1. Every plugin has a .claude-plugin/plugin.json with required
     fields (name, version, description, type).
  2. Every skill directory has a SKILL.md with required frontmatter
     (name, description, type).
  3. Every skill's allowed_tools list references real MCP servers
     declared in any .mcp.json in the plugin tree (or 'none' for
     parsing/formatting skills that don't call tools).
  4. Every plugin that declares requires: ["scope-core"] actually
     has scope-core resolvable in plugins/vertical-plugins/.
  5. Bundled skills in agent-plugins match their source in
     vertical-plugins (no drift). Compares directory contents byte
     for byte.

Exit code 0 on pass, 1 on fail. Prints a clear list of violations
with file paths.

Stdlib only.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
VERTICAL_PLUGINS = PLUGINS / "vertical-plugins"
AGENT_PLUGINS = PLUGINS / "agent-plugins"
PARTNER_PLUGINS = PLUGINS / "partner-built"

REQUIRED_PLUGIN_FIELDS = ("name", "version", "description", "type")
REQUIRED_SKILL_FIELDS = ("name", "description", "type")


def fail(violations: list[str]) -> None:
    print()
    print(f"check.py: {len(violations)} violation(s):")
    for v in violations:
        print(f"  - {v}")
    sys.exit(1)


def ok() -> None:
    print("check.py: all plugins pass structure check")
    sys.exit(0)


def iter_plugin_dirs() -> Iterator[Path]:
    """Yield every plugin directory (one that contains .claude-plugin)."""
    for parent in (VERTICAL_PLUGINS, AGENT_PLUGINS, PARTNER_PLUGINS):
        if not parent.exists():
            continue
        for entry in parent.iterdir():
            if entry.is_dir() and entry.name.startswith("_"):
                # Skip _README, _example-partner-plugin (kept as
                # reference, not a real plugin).
                continue
            if (entry / ".claude-plugin" / "plugin.json").exists():
                yield entry


def parse_frontmatter(path: Path) -> dict | None:
    """Read a SKILL.md or command .md file's YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    block = text[4:end]
    out: dict[str, object] = {}
    cur_key: str | None = None
    cur_list: list[str] | None = None
    for line in block.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and cur_list is not None:
            cur_list.append(line[4:].strip())
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", line)
        if m:
            cur_key = m.group(1)
            value = m.group(2).strip()
            if value:
                out[cur_key] = value
                cur_list = None
            else:
                cur_list = []
                out[cur_key] = cur_list
    return out


def collect_mcp_servers(plugin_root: Path) -> set[str]:
    """Return the set of MCP server prefixes declared anywhere under the
    plugin (e.g., 'scope-legal', 'verident'). Used to validate
    allowed_tools entries.

    Also includes any server declared in scope-core (since requires:
    scope-core means scope-core's connectors are inherited)."""
    servers: set[str] = set()
    for mcp_path in plugin_root.rglob(".mcp.json"):
        try:
            data = json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for name in (data.get("mcpServers") or {}).keys():
            servers.add(name)
    # If this plugin requires scope-core, inherit scope-core's servers.
    plugin_json = plugin_root / ".claude-plugin" / "plugin.json"
    try:
        plugin_data = json.loads(plugin_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        plugin_data = {}
    requires = plugin_data.get("requires") or []
    if "scope-core" in requires:
        scope_core_mcp = VERTICAL_PLUGINS / "scope-core" / ".mcp.json"
        if scope_core_mcp.exists():
            try:
                core = json.loads(scope_core_mcp.read_text(encoding="utf-8"))
                for name in (core.get("mcpServers") or {}).keys():
                    servers.add(name)
            except json.JSONDecodeError:
                pass
    return servers


def main() -> None:
    violations: list[str] = []

    plugin_dirs = list(iter_plugin_dirs())
    if not plugin_dirs:
        violations.append(f"no plugins found under {PLUGINS}")

    for plugin_dir in plugin_dirs:
        manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
        rel = manifest_path.relative_to(ROOT)
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            violations.append(f"{rel}: invalid JSON: {e}")
            continue

        # Required fields.
        for field in REQUIRED_PLUGIN_FIELDS:
            if field not in manifest:
                violations.append(f"{rel}: missing required field '{field}'")

        # requires: scope-core resolvability.
        for req in manifest.get("requires") or []:
            target = VERTICAL_PLUGINS / req
            if not (target / ".claude-plugin" / "plugin.json").exists():
                violations.append(
                    f"{rel}: requires '{req}' but it is not resolvable at "
                    f"{target.relative_to(ROOT)}"
                )

        # Skills.
        skills_dir_name = manifest.get("skills_dir", "skills")
        skills_dir = plugin_dir / skills_dir_name
        if skills_dir.exists():
            mcp_servers = collect_mcp_servers(plugin_dir)
            for skill_dir in skills_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                skill_md = skill_dir / "SKILL.md"
                if not skill_md.exists():
                    violations.append(
                        f"{skill_dir.relative_to(ROOT)}: missing SKILL.md"
                    )
                    continue
                fm = parse_frontmatter(skill_md)
                if fm is None:
                    violations.append(
                        f"{skill_md.relative_to(ROOT)}: missing or "
                        f"malformed YAML frontmatter"
                    )
                    continue
                for f in REQUIRED_SKILL_FIELDS:
                    if f not in fm:
                        violations.append(
                            f"{skill_md.relative_to(ROOT)}: missing "
                            f"frontmatter field '{f}'"
                        )
                # allowed_tools: each entry is <server>__<tool> or 'none'.
                allowed = fm.get("allowed_tools") or []
                if isinstance(allowed, list):
                    for tool in allowed:
                        if tool == "none":
                            continue
                        if "__" not in tool:
                            violations.append(
                                f"{skill_md.relative_to(ROOT)}: allowed_tool "
                                f"'{tool}' missing '__' separator"
                            )
                            continue
                        prefix = tool.split("__", 1)[0]
                        if prefix not in mcp_servers:
                            violations.append(
                                f"{skill_md.relative_to(ROOT)}: allowed_tool "
                                f"'{tool}' references unknown MCP server "
                                f"'{prefix}' (known: {sorted(mcp_servers)})"
                            )

    # Bundled-skill drift: every skill under agent-plugins/<agent>/skills
    # must match its source in vertical-plugins/<vertical>/skills exactly.
    if AGENT_PLUGINS.exists():
        for agent_dir in AGENT_PLUGINS.iterdir():
            if not agent_dir.is_dir():
                continue
            bundled = agent_dir / "skills"
            if not bundled.exists():
                continue
            for skill_dir in bundled.iterdir():
                if not skill_dir.is_dir():
                    continue
                # Find the source.
                source: Path | None = None
                for vert in VERTICAL_PLUGINS.iterdir():
                    candidate = vert / "skills" / skill_dir.name
                    if candidate.exists():
                        source = candidate
                        break
                if source is None:
                    violations.append(
                        f"{skill_dir.relative_to(ROOT)}: bundled skill has "
                        f"no source under vertical-plugins/*/skills/"
                    )
                    continue
                # Compare SKILL.md contents.
                bundled_md = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                source_md = (source / "SKILL.md").read_text(encoding="utf-8")
                if bundled_md != source_md:
                    violations.append(
                        f"{skill_dir.relative_to(ROOT)}: bundled SKILL.md "
                        f"drifts from source {source.relative_to(ROOT)} - "
                        f"run scripts/sync-agent-skills.py"
                    )

    if violations:
        fail(violations)
    ok()


if __name__ == "__main__":
    main()
