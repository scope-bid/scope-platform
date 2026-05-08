---
name: bonding-capacity-check
description: Verify a subcontractor's bonding capacity for a project. Auto-fires on bonding mentions.
type: auto
triggers:
  - bonding capacity
  - performance bond
  - payment bond
  - surety capacity
  - bondable
  - aggregate bonding
allowed_tools:
  - scope-aec__scope_aec_status
---

# Bonding capacity check

Bonding capacity tells the GC whether a sub can be bonded for a
specific project value. Subs work with a surety; the surety sets a
single-project limit and an aggregate-program limit. The GC's risk
team confirms the sub is in good standing with the surety before
awarding.

## What you collect

- Subcontractor legal name
- Project value (the bid value plus any change-order headroom)
- Bond type (performance, payment, both)
- Bond form (AIA, ConsensusDocs, custom GC form)
- Project start and completion dates

## Dispatch flow (V3 preview)

V3 launches 2027. The MCP exposes `scope_aec_status` only.

When V3 ships, the flow surfaces the sub's surety relationship,
single-project limit, aggregate available capacity, and surety
quality (AM Best rating). If the sub does not have surety capacity
for the project, surface that plainly. The GC decides what to do.

## Voice rails

Bonding capacity is presented as factual fields. Do not interpret
whether the GC should award. Stick to the surety's stated capacity
and rating.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
