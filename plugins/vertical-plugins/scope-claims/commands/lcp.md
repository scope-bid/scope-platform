---
name: lcp
description: Fast path for life-care plan dispatch on a catastrophic claim.
---

When the user runs `/lcp [details]`, fire the life-care-planning
skill.

Required fields: claim file ID, claimant name and age, diagnosis,
care categories needed. Optional: plan horizon, format preference.

Claims is in preview. Waitlist behavior same as `/ime` for now.
