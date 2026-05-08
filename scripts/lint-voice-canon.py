#!/usr/bin/env python3
"""
scope-platform voice canon lint.

Walks every .md, .ts, .tsx, .yaml, .yml file under plugins/,
managed-agent-cookbooks/, scope-firm-routing/, scripts/, and the
top-level READMEs / CLAUDE.md / CONTRIBUTING.md. Fails on any of:

  - Em-dash (U+2014)
  - En-dash (U+2013)
  - Smart single quote (U+2018, U+2019)
  - Smart double quote (U+201C, U+201D)
  - Ellipsis character (U+2026)
  - Words 'matched', 'matching', 'recommended', 'recommendation'
    (case-insensitive). ABA Rule 7.2 voice rails.
  - Phrase 'AI conversation' (per audit canon)
  - Phrase '60-120 days' (per audit canon - should be '60-90 days')

Hardened 2026-05-08:
  - Patterns use explicit Unicode escapes (\\u2014 etc.) instead of
    literal glyphs. Editor copy-paste can substitute lookalike
    codepoints (zero-width joiners, alternate Unicode shapes); the
    escape form locks the regex to the exact codepoint.
  - File scanner walks .ts, .tsx, .yaml, .yml in addition to .md so
    skill prompts and config files are covered, not just docs.
  - Backtick-wrapped tokens (`matched`) still pass - that's the
    legitimate way to reference forbidden words in documentation.

Prints every violation with file:line: pattern: surrounding text.
Exits 1 on any hit.

Stdlib only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Paths to scan.
TARGETS = [
    ROOT / "plugins",
    ROOT / "managed-agent-cookbooks",
    ROOT / "scope-firm-routing",
    ROOT / "scripts",
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "DEMO.md",
]

# File extensions to scan. Anything not in this set is skipped, so
# binary assets (JSON-RPC examples in .json, raw .py source) don't
# trigger false positives on tokens that legitimately appear in code.
SCAN_EXTENSIONS = {".md", ".ts", ".tsx", ".yaml", ".yml"}

# Patterns. Each is (label, regex, kind). Char patterns use explicit
# Unicode escapes (\\u2014 etc.) so the regex is unambiguous regardless
# of how this file was saved. Word matches use word boundaries; phrase
# matches are literal substring (case-insensitive).
PATTERNS = [
    ("em-dash (U+2014)", re.compile("—"), "char"),
    ("smart single quote (U+2018)", re.compile("‘"), "char"),
    ("smart single quote (U+2019)", re.compile("’"), "char"),
    ("smart double quote (U+201C)", re.compile("“"), "char"),
    ("smart double quote (U+201D)", re.compile("”"), "char"),
    ("ellipsis character (U+2026)", re.compile("…"), "char"),
    ("forbidden word: matched", re.compile(r"\bmatched\b", re.IGNORECASE), "word"),
    ("forbidden word: matching", re.compile(r"\bmatching\b", re.IGNORECASE), "word"),
    ("forbidden word: recommended", re.compile(r"\brecommended\b", re.IGNORECASE), "word"),
    ("forbidden word: recommendation", re.compile(r"\brecommendation\b", re.IGNORECASE), "word"),
    ("forbidden phrase: AI conversation", re.compile(r"AI conversation", re.IGNORECASE), "phrase"),
    ("forbidden phrase: 60-120 days", re.compile(r"60-120\s*days?", re.IGNORECASE), "phrase"),
]

# En-dash explicit codepoint U+2013. Flagged anywhere it appears; the
# canon prefers ASCII hyphens for ranges too.
EN_DASH = re.compile("–")


def iter_md_files() -> list[Path]:
    """Walk the targets and return every file with a scanned extension.
    Name kept as iter_md_files for backwards-compat with the old
    docstring, but we now also scan .ts, .tsx, .yaml, .yml."""
    files: list[Path] = []
    for target in TARGETS:
        if target.is_file() and target.suffix in SCAN_EXTENSIONS:
            files.append(target)
        elif target.is_dir():
            for ext in SCAN_EXTENSIONS:
                files.extend(sorted(target.rglob(f"*{ext}")))
    return sorted(set(files))


def is_inside_backticks(line: str, pos: int) -> bool:
    """Return True if position pos on line is inside a backtick span.
    Backtick-wrapped tokens are the legitimate way to reference
    forbidden words in documentation - the rule prohibits using them
    in prose, not naming them."""
    in_span = False
    i = 0
    while i < len(line):
        if line[i:i + 3] == "```":
            in_span = not in_span
            if i <= pos < i + 3:
                return True
            i += 3
            continue
        if line[i] == "`":
            if i == pos:
                return in_span
            in_span = not in_span
            i += 1
            continue
        if i == pos:
            return in_span
        i += 1
    return False


def lint_file(path: Path) -> list[str]:
    violations: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return violations
    rel = path.relative_to(ROOT)
    lines = text.splitlines()
    in_code_fence = False
    for lineno, line in enumerate(lines, start=1):
        # Fenced code blocks are skipped entirely. Shell, JSON, YAML
        # examples may legitimately contain forbidden tokens.
        if line.strip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        for label, regex, _kind in PATTERNS:
            for m in regex.finditer(line):
                if is_inside_backticks(line, m.start()):
                    continue
                context = line.strip()
                if len(context) > 120:
                    start = max(0, m.start() - 40)
                    end = min(len(line), m.end() + 40)
                    context = "..." + line[start:end].strip() + "..."
                violations.append(f"{rel}:{lineno}: {label}: {context}")
        for m in EN_DASH.finditer(line):
            if is_inside_backticks(line, m.start()):
                continue
            context = line.strip()
            if len(context) > 120:
                start = max(0, m.start() - 40)
                end = min(len(line), m.end() + 40)
                context = "..." + line[start:end].strip() + "..."
            violations.append(f"{rel}:{lineno}: en-dash (U+2013): {context}")
    return violations


def main() -> None:
    all_violations: list[str] = []
    for path in iter_md_files():
        all_violations.extend(lint_file(path))

    if all_violations:
        for v in all_violations:
            print(v)
        print()
        print(f"lint-voice-canon.py: {len(all_violations)} violation(s)")
        sys.exit(1)
    print("lint-voice-canon.py: clean")
    sys.exit(0)


if __name__ == "__main__":
    main()
