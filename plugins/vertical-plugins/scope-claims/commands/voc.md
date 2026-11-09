---
name: voc
description: Fast path for vocational rehabilitation expert dispatch.
---

When the user runs `/voc [details]`, fire the voc-rehab-routing skill.

Required fields: claim file ID, claimant name, age, education, work
history, MSA. Optional: engagement type (RTW, TSA, placement plan).

Claims is in preview. Waitlist behavior same as `/ime` for now.
