---
name: life-care-planning
description: Dispatch a life-care plan request for a catastrophic claim. Auto-fires on life-care mentions.
type: auto
triggers:
  - life-care plan
  - LCP
  - life care planner
  - future medical costs
  - catastrophic claim
  - lifetime care
allowed_tools:
  - scope-claims__scope_claims_status
  - scope-claims__scope_claims_join_waitlist
---

# Life-care planning

Life-care planners build out the projected lifetime medical and
support costs for a catastrophically injured claimant. The plan
becomes a damages anchor at trial or settlement and gets weighed in
reserve setting.

## What you collect

- Claim file ID
- Claimant name, age, life expectancy estimate (from medical record
  or actuarial baseline)
- Diagnosis and prognosis (from treating physician notes plus IME if
  available)
- Required care categories (medical, attendant care, home
  modifications, equipment, medications, therapies)
- Plan horizon (typically lifetime; some plans truncate at 10 or 20
  years for settlement frame)
- Plan format (long-form narrative vs. cost-summary table; some
  jurisdictions prefer one over the other)

## Dispatch flow (V2 preview)

V2 launches Q3 2026. Until then, waitlist via the standard claims
MCP tools.

When V2 ships, the dispatch flow surfaces life-care planners with
certifications (CLCP, CCM), prior-plan count, and average plan
turnaround time.

## Voice rails

Life-care planners are presented. The carrier or defense counsel
retains. Do not interpret the medical record; the planner builds the
plan from the medical evidence the lawyer provides.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
