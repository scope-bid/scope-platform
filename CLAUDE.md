# CLAUDE.md - scope-platform

This directory inherits the voice canon and ethics rails from the
parent Scope.bid repo. See `/Users/jackgillen/Scope.Bid/CLAUDE.md`
for the full non-negotiables.

## Short list (the rails the lint scripts enforce)

- ASCII hyphens only. No em-dashes (U+2014), no en-dashes (U+2013),
  no smart single quotes, no smart double quotes, no ellipsis
  character (U+2026). Use plain `-`, `'`, `"`, `...`.
- Sentence case for all eyebrows, pills, labels, slash command
  names. No all-caps decorative typography.
- "Returned" or "presented", never `matched` or `recommended`. ABA
  Model Rule 7.2 (referrals) sits underneath this.
- "Request" not "ask" in positioning copy.
- "Your firm" or "your team" in positioning copy. Avoid "buyer"
  except in marketplace-mechanic copy where it pairs with "vendor".
- Plain English. Avoid "operationalize", "structurally",
  "materially", "regulatory drag", "namespace exclusivity".
- "60-90 days" is the canonical receivables-cycle phrasing. The
  prior `60-120 days` figure is retired.

## ABA rails (specific)

- Rule 5.4 (independence of professional judgment). The lawyer's
  judgment on whom to retain stays the lawyer's. The agent surfaces
  factual fields; the lawyer weighs and decides.
- Rule 7.2 (referrals and recommendations). The agent does not
  recommend. Quotes are returned and presented. The lawyer's bar
  counsel can read every transcript without finding a Rule 7.2
  violation.

## Ship-time check

Before opening a PR, run:

```
python3 scripts/check.py
python3 scripts/lint-voice-canon.py
python3 scripts/validate.py
```

All three must exit 0.

## When in doubt

Read the live site canon at
`/Users/jackgillen/Scope.Bid/audit/agent-language-style-guide.md`.
Read the recent shipping context at
`/Users/jackgillen/Scope.Bid/audit/2026-05-08-live-site-audit.md`
and
`/Users/jackgillen/Scope.Bid/audit/login-ux-rework-spec-2026-05-08.md`.
The rails are not arbitrary. Every one of them has a reason in the
audit log.
