---
name: prequal
description: Fast path for subcontractor prequalification roll-up across ISN, Avetta, TradeTapp, Veriforce.
---

When the user runs `/prequal [sub name] [trade] [project]`, fire the
subcontractor-prequal skill.

The skill calls `scope_verify_prequal` and returns a normalized
prequal card across the platforms Scope knows about, plus the bond
capacity available and the safety summary (E-Mod, TRIR). If any
platform shows non-current, surface that plainly.

Demo mode is live; real vendor onboarding ships with V3 (2027).
