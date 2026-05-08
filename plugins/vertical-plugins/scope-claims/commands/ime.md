---
name: ime
description: Fast path for IME dispatch - panel-cleared, in-network, BAA on file.
---

When the user runs `/ime [details]`, fire the ime-routing skill.

Required fields: claim file ID, claimant name, specialty, MSA or
city. Optional: in-network only, exam duration, date window.

V2 launches Q3 2026. Until then, the command surfaces the carrier's
waitlist position via `scope_claims_status` and offers to register
the carrier via `scope_claims_join_waitlist` if not yet on the list.

Run conflict-check on the claimant before any dispatch. Pass quotes
to quote-comparison.
