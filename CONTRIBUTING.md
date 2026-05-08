# Contributing to scope-platform

Two contribution paths:

1. First-party plugin work (Scope team). Edit any plugin under
   `plugins/vertical-plugins/` or `plugins/agent-plugins/`, run the
   lint locally, open a PR.
2. Partner-plugin work (vendor agencies). Add a new plugin under
   `plugins/partner-built/<your-slug>/`. See
   `plugins/partner-built/_README.md` for the full contract.

Both paths share the same lint stack and the same review process.

## Lint locally

Run from the repo root:

```
python3 scripts/check.py
python3 scripts/lint-voice-canon.py
python3 scripts/validate.py
```

All three must exit 0.

`check.py` validates plugin manifest shape, skill frontmatter, and
the bundled-skill drift between agent plugins and their source
verticals.

`lint-voice-canon.py` walks every markdown file and fails on
em-dashes, en-dashes, smart quotes, the ellipsis character, the
forbidden words (`matched`, `matching`, `recommended`,
`recommendation`), and the retired phrases (`AI conversation`,
`60-120 days`).

`validate.py` validates `.mcp.json` shape and `agent.yaml`
references.

## Sync bundled skills

If you edit a skill in `plugins/vertical-plugins/<vertical>/skills/`
that is also bundled into an agent plugin, run:

```
python3 scripts/sync-agent-skills.py
```

This copies the source skill into every agent plugin that bundles
it. Without this, `check.py` will flag drift on the next lint run.

## PR review SLA

- First-party PRs: reviewed within 2 business days.
- Partner-plugin PRs: reviewed within 5 business days. Re-reviews
  on revision are 2 business days.

## What gets reviewed

- Voice canon compliance (auto-checked by lint).
- Skill body quality (200-400 words, plain English, no consultant
  jargon).
- Slash command behavior (does the command's body match the
  skill's behavior?).
- ABA-rails respect (no `matched`, no `recommended`, no judgment
  labels on vendors, no bypassing of conflict-check).
- Security model for partner plugins (auth, rate limit, the
  partner's stated coverage).
