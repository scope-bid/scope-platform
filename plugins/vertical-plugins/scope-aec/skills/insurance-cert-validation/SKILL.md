---
name: insurance-cert-validation
description: Validate a subcontractor's certificate of insurance against project requirements. Auto-fires on COI mentions.
type: auto
triggers:
  - certificate of insurance
  - COI
  - additional insured
  - insurance certificate
  - umbrella coverage
  - workers comp coverage
  - waiver of subrogation
allowed_tools:
  - scope-aec__scope_aec_status
---

# Insurance certificate validation

Every sub on a commercial project needs a certificate of insurance
that meets the GC's minimum coverage requirements. The COI shows
GL, auto, workers comp, umbrella, and any project-specific endorsements
(additional insured, waiver of subrogation, primary and non-contributory).

## What you collect

- Subcontractor legal name
- Project ID
- Required minimum limits (typically $1M GL, $5M umbrella, statutory
  workers comp; the GC's contract specifies the exact thresholds)
- Required endorsements (additional insured, waiver of sub, primary
  and non-contributory)
- Effective date and expiration date check

## Dispatch flow (V3 preview)

V3 launches 2027. The MCP exposes `scope_aec_status` only.

When V3 ships, the flow surfaces the COI's coverage limits, named
insureds, endorsements, and expiration. If any required field is
missing or below threshold, surface that plainly with the field name
and the required vs. actual value.

## Voice rails

COI validation is presented as factual fields. Do not interpret. The
GC's risk team decides whether to accept the COI or require a revised
certificate.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
