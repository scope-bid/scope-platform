---
name: conflict-check-workflow
description: Run a conflict check before dispatching any matter. Auto-fires when matter intake includes party names. Halts dispatch if a conflict is found.
type: auto
triggers:
  - conflict check
  - check conflicts
  - run conflicts
  - parties to the dispute
  - opposing party
  - claimant identity
allowed_tools:
  - scope-legal__scope_get_matter
---

# Conflict check workflow

Every matter has a `conflict_check_required` field. If true, you must
run a conflict check before any dispatch tool can fire. This protects
the firm and the lawyer from inadvertent representation against an
existing client or any party the firm has flagged.

## What you check

Take every party name the intake skill captured (plaintiffs,
defendants, claimants, counterparties, named experts, related
entities). For each name, query the firm's conflict database via the
appropriate MCP tool. If any name returns a hit:

- Halt dispatch immediately.
- Surface the hit to the user with the matter ID, the conflict source,
  and the date of the prior representation if known.
- Wait for the user to either clear the conflict (informed-consent
  workflow, separate from this skill) or abandon the matter.

If no hit, mark the conflict_check_required field as cleared with a
short audit note ("Conflict check cleared <timestamp> against parties
<list>") and return control to the dispatch flow.

## What you do not do

Do not interpret the conflict or advise on whether the lawyer can
proceed. That is a legal-ethics judgment the lawyer makes, not the
agent. You surface; the lawyer decides.

Do not bypass the check, even if the user asks you to. The check is
not optional. If the user wants to dispatch without a conflict check
on a matter where it is required, halt and explain that the firm's
conflict policy gates the dispatch and that you cannot override it.

## Voice rails

When a conflict is found, use plain English. No legalese beyond what
the lawyer needs to act. ASCII hyphens only. No em-dashes, no smart
quotes, no ellipsis character. Sentence case for any pill or status
label.

When the check clears, say so once and move on. Do not editorialize.
