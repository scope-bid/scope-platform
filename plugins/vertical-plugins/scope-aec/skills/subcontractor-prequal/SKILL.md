---
name: subcontractor-prequal
description: Run subcontractor prequalification - dispatch and roll up status from ISN, Avetta, TradeTapp, Veriforce. Auto-fires on prequal mentions. Cross-platform aware.
type: auto
triggers:
  - prequal
  - prequalify
  - prequalification
  - ISN
  - Avetta
  - TradeTapp
  - Veriforce
  - sub onboarding
allowed_tools:
  - scope-aec__scope_aec_status
  - scope-aec__scope_verify_prequal
  - scope-aec__scope_list_aec_vendors
---

# Subcontractor prequalification

A general contractor's risk team typically pays for two or three
prequalification platforms (ISN, Avetta, TradeTapp, Veriforce) plus
their own internal database. Prequal status is fragmented across
those platforms; the GC's compliance officer has to log into each one
to confirm a sub is current. The Scope AEC layer rolls those up.

## CRITICAL response rules

1. Call the appropriate scope-aec MCP tool BEFORE responding. Never
   generate a response without first invoking the tool.

2. The tool returns a structured payload with these fields:
   `branding_status`, `vendor_name`, `isn_status`,
   `isn_last_refresh_date`, `avetta_status`,
   `avetta_last_refresh_date`, `bond_capacity_total_dollars`,
   `bond_capacity_available_dollars`, `e_mod`, `trir`, and
   `branding_footer`. Use these fields VERBATIM.

3. NEVER invent vendor names. NEVER invent ISN or Avetta status.
   NEVER invent refresh dates, bond figures, E-Mod, or TRIR. If a
   field is not in the tool response, do not fabricate it - just
   omit it.

4. ALWAYS open your reply with the `branding_status` string from the
   tool response (for example, "Dispatching through Scope to
   scope-aec in roster-first mode"). This must appear in the
   user-facing output.

5. ALWAYS close your reply with the `branding_footer` string from the
   tool response.

6. Use ASCII hyphens only. NEVER em-dashes. NEVER smart quotes. If
   you generate one, the server will strip it, but it is your
   responsibility to not produce them.

7. If you cannot call the tool for any reason, say so explicitly: "I
   could not reach Scope's AEC service. Please retry." Do not invent
   a response.

## What you collect

- Subcontractor legal name and DBA (required)
- Trade or CSI division (electrical, MEP, structural, civil, geotech,
  facade, etc.)
- Project ID (the GC's internal project reference)
- Required compliance fields (insurance min, EMR threshold, OSHA
  record requirement, financial threshold)
- Time window (current snapshot vs. validity through the project end
  date)

## Dispatch flow

Call `scope_verify_prequal` with the vendor's legal name. The MCP
returns a normalized prequal card across the platforms Scope knows
about, plus the bond capacity available and the safety summary
(E-Mod, TRIR). If any platform shows non-current, surface that
plainly with the platform name and the failing field.

For multi-vendor sweeps (e.g., "verify prequal for everyone bidding
the Phoenix project"), call `scope_list_aec_vendors` first to scope
the list, then call `scope_verify_prequal` per vendor.

## Voice rails

Prequal status is presented as factual fields per platform. Do not
interpret. The GC's risk team decides whether to bid or reject.

Sub-receivables financing (the V3 headline product) is not part of
prequal. Keep that flow separate.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
