---
name: voc-rehab-routing
description: Route a vocational rehabilitation expert request - return-to-work assessment, job placement, transferable-skills analysis. Auto-fires on voc-rehab mentions.
type: auto
triggers:
  - vocational rehab
  - voc rehab
  - return to work
  - transferable skills
  - vocational expert
  - job placement assessment
allowed_tools:
  - scope-claims__scope_claims_status
  - scope-claims__scope_claims_join_waitlist
---

# Vocational rehabilitation routing

Vocational rehabilitation experts assess return-to-work potential,
transferable skills, and job placement options for a claimant. They
get retained on bodily injury claims where the claim alleges loss of
earning capacity.

## What you collect

- Claim file ID
- Claimant name, age, education level, work history (the voc expert
  needs the work-history detail to do a transferable-skills analysis)
- Injury type and current functional limitations (from the IME or
  treating physician)
- Engagement type: return-to-work assessment, transferable-skills
  analysis, job-placement plan, all of the above
- MSA or region (for labor-market data)

## Dispatch flow (V2 preview)

V2 launches Q3 2026. The MCP currently exposes the waitlist tools.
When V2 ships, the dispatch flow surfaces voc experts in the
claimant's MSA with prior-engagement count, certifications (CRC,
CDMS), and rate.

## Voice rails

Voc experts are presented. The carrier or defense counsel retains.
Do not interpret functional limitations; the IME report does that.
Surface the voc expert's certifications and prior-engagement count;
let the lawyer or claims VP weigh.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
