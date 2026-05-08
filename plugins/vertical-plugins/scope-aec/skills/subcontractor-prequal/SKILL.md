---
name: subcontractor-prequal
description: Run subcontractor prequalification - dispatch and roll up status from ISN, Avetta, TradeTapp, Veriforce. Auto-fires on prequal mentions. Cross-platform aware.
type: auto
triggers:
  - prequal
  - prequalify
  - prequalification
  - ISN
  - Avetta
  - TradeTapp
  - Veriforce
  - sub onboarding
allowed_tools:
  - scope-aec__scope_aec_status
---

# Subcontractor prequalification

A general contractor's risk team typically pays for two or three
prequalification platforms (ISN, Avetta, TradeTapp, Veriforce) plus
their own internal database. Prequal status is fragmented across
those platforms; the GC's compliance officer has to log into each one
to confirm a sub is current. The Scope AEC layer rolls those up.

## What you collect

- Subcontractor legal name and DBA
- Trade or CSI division (electrical, MEP, structural, civil, geotech,
  facade, etc.)
- Project ID (the GC's internal project reference)
- Required compliance fields (insurance min, EMR threshold, OSHA
  record requirement, financial threshold)
- Time window (current snapshot vs. validity through the project end
  date)

## Dispatch flow (V3 preview)

V3 launches 2027. Until then, the MCP exposes `scope_aec_status` only
(reserved namespace, waitlist).

When V3 ships, the dispatch flow surfaces a sub's prequal status
across all the platforms the GC subscribes to, normalized into a
single status card. If any platform shows non-current, surface that
plainly with the platform name and the failing field.

## Voice rails

Prequal status is presented as factual fields per platform. Do not
interpret. The GC's risk team decides whether to bid or reject.

Sub-receivables financing (the V3 headline product) is not part of
prequal. Keep that flow separate.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
