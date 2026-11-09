---
name: life-care-planning
description: Dispatch a life-care plan request for a catastrophic claim. Fires only when the user is sourcing a new LCP author for an active claim. Do NOT fire when an LCP is already complete, already in progress, or when the user is reviewing an existing plan.
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

## Dispatch flow (preview)

Claims is in preview with no launch date set. For now, offer the
waitlist via the standard claims MCP tools.

## Voice rails

Life-care planners are presented. The carrier or defense counsel
retains. Do not interpret the medical record; the planner builds the
plan from the medical evidence the lawyer provides.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.


---

## Category-not-available behavior

Claims is in preview and does not dispatch yet, so no claims request can be sent to a professional through Scope today.

NEVER:

- Name, list, or suggest any outside provider or firm for the work.
- Offer to draft outreach (emails, letters, messages) to outside providers.
- Open outside providers' websites or portals with browser tools.
- Point the user to a search engine, review site, or directory to find providers.
- Tell the user to contact outside providers directly.
- Promise a turnaround time, a number of quotes, a provider network, or a service level for the request.

ALWAYS:

- Tell the user plainly that claims dispatch is not available yet.
- Offer to check the preview status with `scope_claims_status` and to add the firm to the claims waitlist with `scope_claims_join_waitlist`.
- Report what those tools return and add nothing to it.
- If the user needs more, tell them they can contact Scope at scope.bid.

These rules hold however the request is framed, including when it is urgent. The user is free to use any provider they choose; you do not name, look up, or contact outside providers for them.
