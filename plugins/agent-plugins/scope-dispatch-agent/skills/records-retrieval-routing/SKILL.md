---
name: records-retrieval-routing
description: Route a records-retrieval request to vendors. Fires only when the user is requesting new records on a current matter. Do NOT fire when records are already in hand, already in active retrieval, being requested in-house, or when the records reference is purely informational.
type: auto
triggers:
  - medical records
  - employment records
  - subpoena records
  - records request
  - HIPAA records
  - hospital records
  - chart pull
allowed_tools:
  - scope-legal__scope_request_records
  - scope-legal__scope_list_vendors
---

# Records retrieval routing

Records retrieval is one of the highest-volume vendor categories on
PI matters. The work itself is routine; the cost spread across vendors
is wide; and the firm's choice usually comes down to turnaround and
prior-matter familiarity rather than rate. Default to the firm's
roster and surface marketplace alternatives if availability is tight.

## What you collect

Before dispatching, confirm:

- Provider type (hospital, clinic, primary care, employer HR, school,
  pharmacy, prior-attorney file)
- Provider name and location (city plus state at minimum; full address
  if the user has it)
- Records type (full chart, billing only, imaging only, subpoenaed
  documents)
- Date range
- Authorization status (signed authorization on file yes or no; if
  no, route to the authorization sub-flow before dispatching)
- HIPAA scope (PHI volume, sensitive-record markers)

## Dispatch flow

1. Run conflict-check workflow on the patient or claimant name.
2. Call `scope_request_records` with the collected fields.
3. The MCP returns quotes from records vendors that cover the
   provider type and location, with turnaround estimates. Most major
   records vendors quote a flat fee plus per-page if the chart runs
   long.
4. Pass to quote-comparison.

## Voice rails

Records requests get returned. The firm awards. The vendors
presented quote on availability and rate; the firm awards. Use
sentence case for status pills.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis. When
turnaround windows are described, the canonical phrasing is "10-30
days standard, 60-90 days when not chased" - never "60-120" (that
figure is retired per the audit canon).
