---
name: safety-record-pull
description: Pull a subcontractor's OSHA and safety record. Auto-fires on safety-record or EMR mentions.
type: auto
triggers:
  - OSHA record
  - safety record
  - EMR
  - experience modification rate
  - DART rate
  - TRIR
  - safety incidents
allowed_tools:
  - scope-aec__scope_aec_status
---

# Safety record pull

A sub's safety record drives prequal eligibility on most large
commercial projects. The GC's risk team checks EMR (experience
modification rate), DART rate, TRIR (total recordable incident
rate), and recent OSHA citations.

## What you collect

- Subcontractor legal name
- DUNS or EIN if available (helps disambiguate national subs)
- Time window for the record pull (typically last 3 years)

## Dispatch flow (V3 preview)

V3 launches 2027. The MCP exposes `scope_aec_status` only.

When V3 ships, the flow surfaces EMR, DART, TRIR, and a list of OSHA
citations in the time window with severity classification. The GC
decides whether to bid or reject.

## Voice rails

Safety records are presented as factual fields. Do not interpret
risk. The GC's safety officer decides.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
