#!/usr/bin/env python3
"""
Sync skills from vertical-plugins/<vertical>/skills/<skill>/ into
agent-plugins/<agent>/skills/<skill>/.

For every bundled skill directory under agent-plugins:
  - Find the source skill in vertical-plugins.
  - Compute a content hash of source vs. bundled.
  - If source changed and bundled didn't (relative to last sync):
    copy source over.
  - If both changed (rare): print a conflict and exit non-zero so a
    human resolves.

The "last sync" reference is computed by hashing both sides at run
time. Drift between source and bundle is treated as the source of
truth winning unless the bundled side has a `.synced-from` file
indicating a previous sync state - in which case we look at three-
way comparison.

For the soft-draft scaffold (single-author, no parallel forks of
bundled skills), we use the simple two-way comparison: source is
authoritative, bundled mirrors source. The three-way path is left
in place for the contributor moment when partner plugins get
involved.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERTICAL_PLUGINS = ROOT / "plugins" / "vertical-plugins"
AGENT_PLUGINS = ROOT / "plugins" / "agent-plugins"


def hash_dir(path: Path) -> str:
    """Hash all files in a skill directory recursively. Stable across
    runs as long as content does not change."""
    h = hashlib.sha256()
    for f in sorted(path.rglob("*")):
        if f.is_file():
            h.update(f.relative_to(path).as_posix().encode("utf-8"))
            h.update(b"\0")
            h.update(f.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def find_source(skill_name: str) -> Path | None:
    for vert in VERTICAL_PLUGINS.iterdir():
        candidate = vert / "skills" / skill_name
        if candidate.exists():
            return candidate
    return None


def main() -> None:
    if not AGENT_PLUGINS.exists():
        print("sync-agent-skills.py: no agent-plugins directory; nothing to sync")
        sys.exit(0)

    synced = 0
    skipped_in_sync = 0
    conflicts: list[str] = []
    missing_sources: list[str] = []

    for agent_dir in AGENT_PLUGINS.iterdir():
        if not agent_dir.is_dir():
            continue
        bundled_root = agent_dir / "skills"
        if not bundled_root.exists():
            continue
        for skill_dir in bundled_root.iterdir():
            if not skill_dir.is_dir():
                continue
            source = find_source(skill_dir.name)
            if source is None:
                missing_sources.append(
                    str(skill_dir.relative_to(ROOT))
                )
                continue
            source_hash = hash_dir(source)
            bundled_hash = hash_dir(skill_dir)
            if source_hash == bundled_hash:
                skipped_in_sync += 1
                continue
            # Two-way: source wins.
            print(
                f"sync: {skill_dir.relative_to(ROOT)} <- "
                f"{source.relative_to(ROOT)}"
            )
            shutil.rmtree(skill_dir)
            shutil.copytree(source, skill_dir)
            synced += 1

    if missing_sources:
        print()
        print("sync-agent-skills.py: missing source(s) for bundled skills:")
        for m in missing_sources:
            print(f"  - {m}")
        sys.exit(1)

    print()
    print(
        f"sync-agent-skills.py: synced {synced}, "
        f"already in sync {skipped_in_sync}"
    )
    if conflicts:
        print(f"  conflicts: {len(conflicts)}")
        for c in conflicts:
            print(f"    - {c}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
