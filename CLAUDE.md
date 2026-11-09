# CLAUDE.md - scope-platform

Notes for anyone, human or AI, editing this repo. CI runs the same
checks on every push and pull request (`.github/workflows/lint.yml`).

## Punctuation

- ASCII only. No em-dashes (U+2014), no en-dashes (U+2013), no smart
  single quotes, no smart double quotes, no ellipsis character
  (U+2026). Use plain `-`, `'`, `"`, `...`.

## House style

- Sentence case for all eyebrows, pills, labels, and slash command
  names. No all-caps decorative typography.
- Quotes are "returned" or "presented". Do not use `matched`,
  `matching`, `recommended`, or `recommendation`. Skills and agents
  present the facts; the person reviewing the quotes makes the choice.
- "Engage" is the verb for retaining a professional. Do not use
  `hire`.
- Say "professional" in prose. Identifiers, tool names, and schema
  fields that contain "vendor" stay as they are.
- "Request" not "ask" in positioning copy. "Your firm" or "your team",
  not "buyer".
- Plain English. Avoid "operationalize", "structurally",
  "materially", "regulatory drag".

`scripts/lint-voice-canon.py` holds the full list of banned
characters, words, and phrases. Wrapping a banned word in backticks
is the way to name it in documentation.

## Ship-time check

Before opening a PR, run from the repo root:

```
python3 scripts/check.py
python3 scripts/lint-voice-canon.py
python3 scripts/validate.py
```

All three must exit 0.

If you edit a skill under `plugins/vertical-plugins/` that is also
bundled into an agent plugin, run `python3 scripts/sync-agent-skills.py`
before the checks so the bundled copy stays identical to its source.
