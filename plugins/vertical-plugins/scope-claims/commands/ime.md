---
name: ime
description: Fast path for IME dispatch - panel-cleared, in-network, BAA on file.
---

When the user runs `/ime [details]`, fire the ime-routing skill.

Required fields: claim file ID, claimant name, specialty, MSA or
city. Optional: in-network only, exam duration, date window.

Claims is in preview with no launch date set and does not dispatch
yet. For now, the command checks the claims status via
`scope_claims_status` and offers to add the carrier to the waitlist
via `scope_claims_join_waitlist`.

Collect the claimant's name verbatim for the claim record. Pass
quotes to quote-comparison.
