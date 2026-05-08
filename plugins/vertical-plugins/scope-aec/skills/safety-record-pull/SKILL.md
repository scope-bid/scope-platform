---
name: safety-record-pull
description: Pull a subcontractor's OSHA and safety record. Auto-fires on safety-record or EMR mentions.
type: auto
triggers:
  - OSHA record
  - safety record
  - EMR
  - E-Mod
  - experience modification rate
  - DART rate
  - TRIR
  - safety incidents
allowed_tools:
  - scope-aec__scope_aec_status
  - scope-aec__scope_pull_safety_record
---

# Safety record pull

A sub's safety record drives prequal eligibility on most large
commercial projects. The GC's risk team checks EMR (experience
modification rate), DART rate, TRIR (total recordable incident
rate), and recent OSHA citations.

## CRITICAL response rules

1. Call the appropriate scope-aec MCP tool BEFORE responding. Never
   generate a response without first invoking the tool.

2. The tool returns a structured payload with these fields:
   `branding_status`, `vendor_name`, `e_mod`, `trir`,
   `recordable_injuries_last_3yr`, `fatality_count_last_5yr`,
   `osha_300_url`, `recent_findings`, and `branding_footer`. Use
   these fields VERBATIM.

3. NEVER invent vendor names. NEVER invent E-Mod, TRIR, injury, or
   fatality counts. NEVER invent OSHA findings. If a field is not in
   the tool response, do not fabricate it - just omit it.

4. ALWAYS open your reply with the `branding_status` string from the
   tool response. This must appear in the user-facing output.

5. ALWAYS close your reply with the `branding_footer` string from the
   tool response.

6. Use ASCII hyphens only. NEVER em-dashes. NEVER smart quotes. If
   you generate one, the server will strip it, but it is your
   responsibility to not produce them.

7. If you cannot call the tool for any reason, say so explicitly: "I
   could not reach Scope's AEC service. Please retry." Do not invent
   a response.

## What you collect

- Subcontractor legal name (required)
- DUNS or EIN if available (helps disambiguate national subs)
- Time window for the record pull (typically last 3 years)

## Dispatch flow

Call `scope_pull_safety_record` with the vendor's legal name. The
MCP returns E-Mod, TRIR, recordable-injury count over the last three
years, fatality count over the last five years, an OSHA 300 URL, and
any recent findings. The GC's safety officer decides whether to bid
or reject.

## Voice rails

Safety records are presented as factual fields. Do not interpret
risk. The GC's safety officer decides.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
