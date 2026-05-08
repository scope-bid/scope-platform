---
name: ime-routing
description: Route an independent medical exam request to in-network examiners. Auto-fires on IME mentions. Panel-cleared and BAA-aware.
type: auto
triggers:
  - IME
  - independent medical exam
  - 5806 exam
  - DME
  - schedule a medical exam
  - panel examiner
  - in-network ortho
allowed_tools:
  - scope-claims__scope_claims_status
  - scope-claims__scope_claims_join_waitlist
---

# IME routing

Independent medical exams are the highest-volume claims vendor
category. Carriers and TPAs need a panel-cleared examiner in the
right specialty, in the claimant's MSA, with a HIPAA BAA on file.

## What you collect

- Claim file ID
- Claimant name (for the conflict-check workflow and for the
  examiner's intake)
- Specialty (ortho, neuro, internal med, psychiatry, occupational,
  pain management)
- Body part or injury type
- MSA or city plus state of the claimant
- In-network requirement yes or no
- Exam duration estimate (60 min, 90 min, 120 min)
- Date window the claimant is available

## Dispatch flow (V2 preview)

V2 launches Q3 2026. Until then, the MCP exposes
`scope_claims_status` (current waitlist position and timeline) and
`scope_claims_join_waitlist` (puts the carrier on the founding-cohort
list). For waitlisted carriers, surface the waitlist position
plainly and offer to register the carrier if not yet on the list.

When V2 ships, the dispatch flow will be:

1. Run conflict-check on the claimant.
2. Call the V2 IME dispatch tool with the collected fields.
3. Quotes return from panel-cleared examiners with named providers,
   dates, rates, and BAA status.
4. Pass to quote-comparison.

## Voice rails

The HIPAA BAA badge, the in-network status, the panel-clearance flag
are all factual fields the MCP returns. Surface them. Do not
interpret. The carrier picks the examiner; you do not pick.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
Sentence case for status pills.
