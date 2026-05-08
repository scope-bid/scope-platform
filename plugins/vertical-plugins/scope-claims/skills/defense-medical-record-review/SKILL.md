---
name: defense-medical-record-review
description: Dispatch a claims-side medical record review - chronology, prior-condition analysis, causation assessment. Auto-fires on record-review mentions in a claims context.
type: auto
triggers:
  - record review
  - medical chronology
  - prior conditions
  - causation review
  - claims medical review
  - peer review
allowed_tools:
  - scope-claims__scope_claims_status
  - scope-claims__scope_claims_join_waitlist
---

# Defense medical record review

A defense medical record review is a structured read of the
claimant's medical chart by a board-certified physician or nurse
reviewer. The goal: build a chronology, flag prior conditions, and
support a causation position.

## What you collect

- Claim file ID
- Volume of records (number of pages, number of providers)
- Specialty of the reviewer needed (typically matches the alleged
  injury - ortho for orthopedic claims, neuro for head injuries,
  internal med for systemic complaints)
- Output type: chronology only, chronology plus opinion, peer review
  with full report
- Turnaround window

## Dispatch flow (V2 preview)

V2 launches Q3 2026. Until then, waitlist.

When V2 ships, the flow surfaces board-certified reviewers with
prior-review count, average turnaround, and rate.

## Voice rails

Reviewers are presented. The carrier picks. The reviewer's opinion is
the reviewer's; the claims VP or defense counsel decides what weight
to give it.

Do not editorialize on causation. Surface what the reviewer's prior
work shows; let the lawyer weigh.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
