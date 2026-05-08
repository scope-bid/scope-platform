---
name: bonding
description: Fast path for bonding capacity verification.
---

When the user runs `/bonding [sub name] [project value]`, fire the
bonding-capacity-check skill.

Required: subcontractor legal name, project value. Optional: bond
type, project start and completion dates.

The skill calls `scope_check_bonding` and returns the surety, total
capacity, available capacity, count of current open projects, and
recent completions.

Demo mode is live; real vendor onboarding ships with V3 (2027).
