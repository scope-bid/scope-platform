#!/usr/bin/env python3
"""
scope-platform voice canon lint.

Walks every .md file under plugins/, managed-agent-cookbooks/,
scope-firm-routing/, and the top-level READMEs. Fails on any of:

  - Em-dash (U+2014)
  - En-dash (U+2013) outside numeric ranges (e.g., 60-90 OK, but
    "20 - 30 days" with surrounding spaces flags)
  - Smart single quote (U+2018, U+2019)
  - Smart double quote (U+201C, U+201D)
  - Ellipsis character (U+2026)
  - Words 'matched', 'matching', 'recommended', 'recommendation'
    (case-insensitive). ABA Rule 7.2 voice rails.
  - Phrase 'AI conversation' (per audit canon)
  - Phrase '60-120 days' (per audit canon - should be '60-90 days')

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
    ROOT / "README.md",
    ROOT / "CLAUDE.md",
    ROOT / "CONTRIBUTING.md",
]

# Patterns. Each is (label, regex, kind) where kind is 'unicode',
# 'word', or 'phrase'. Word matches use word boundaries; phrase
# matches are literal substring (case-insensitive); unicode matches
# are exact codepoint.
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

# En-dash needs special handling: allowed inside numeric ranges
# without surrounding spaces; flag everywhere else. We scan literally
# for U+2013 and emit a violation for any occurrence (the rules say
# "outside numeric ranges" but in practice the ASCII hyphen is
# preferred for ranges too, so any en-dash gets flagged).
EN_DASH = re.compile("–")


def iter_md_files() -> list[Path]:
    files: list[Path] = []
    for target in TARGETS:
        if target.is_file() and target.suffix == ".md":
            files.append(target)
        elif target.is_dir():
            files.extend(sorted(target.rglob("*.md")))
    return files


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
