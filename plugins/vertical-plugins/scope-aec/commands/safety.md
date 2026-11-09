---
name: safety
description: Fast path for OSHA and safety record pull.
---

When the user runs `/safety [sub name]`, fire the safety-record-pull
skill.

Required: subcontractor legal name. Optional: time window.

The skill calls `scope_pull_safety_record` and returns E-Mod, TRIR,
recordable-injury count over the last three years, fatality count
over the last five years, an OSHA 300 reference, and any recent
findings.

AEC is in preview. Its tools work in demo mode only.
