---
name: surveillance-coordination
description: Coordinate sub rosa surveillance vendor dispatch for a disputed claim. Auto-fires on surveillance mentions.
type: auto
triggers:
  - surveillance
  - sub rosa
  - field investigation
  - activity check
  - SIU surveillance
allowed_tools:
  - scope-claims__scope_claims_status
  - scope-claims__scope_claims_join_waitlist
---

# Surveillance coordination

Surveillance vendors do field investigation and activity checks on
claimants in disputed-coverage matters. The work is sensitive: the
surveillance must comply with state-by-state privacy law, the
investigator must be licensed in the claimant's jurisdiction, and the
chain-of-custody on any video evidence must hold up at trial.

## What you collect

- Claim file ID
- Claimant name and current address
- Activity hypothesis (what the carrier expects to observe vs. what
  the claim alleges)
- Date window for the surveillance shift (specific days, hours)
- Coverage hours requested (8, 16, 24, multi-day)
- Video required yes or no
- Jurisdiction (drives licensing requirement)

## Dispatch flow (V2 preview)

V2 launches Q3 2026. Until then, the MCP exposes the same status and
waitlist tools as the IME flow. Carriers can register via
`scope_claims_join_waitlist`.

When V2 ships, the dispatch flow surfaces licensed investigators in
the claimant's MSA with prior-engagement count and chain-of-custody
track record. The carrier picks; the agent presents.

## Voice rails

Surveillance is presented from the licensed-investigator pool. The
carrier picks. Do not editorialize on whether the carrier should
surveil; that is a coverage decision. Stick to factual fields:
licensing status, prior-engagement count, MSA coverage, hours
available, rate.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
