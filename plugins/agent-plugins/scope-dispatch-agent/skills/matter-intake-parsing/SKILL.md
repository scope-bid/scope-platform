---
name: matter-intake-parsing
description: Parse a free-text matter description into structured fields - parties, jurisdiction, vendor needs, deadlines. Fires only on new matter description that needs structured parsing into Scope. Do NOT fire when the matter is already open in Scope (matter_id present in context), when the user is asking about an existing matter, when the message is conversational, or when the user is editing fields on an already-parsed matter.
type: auto
triggers:
  - new matter
  - intake
  - opening a case
  - parties to the dispute
  - claim file
  - claimant
  - new project
allowed_tools:
  - scope-legal__scope_get_matter
  - scope-claims__scope_claims_status
  - scope-aec__scope_aec_status
---

# Matter intake parsing

When a lawyer, claims VP, or GC describes a new matter to you, your job is
to extract structured fields the rest of the Scope skills can act on.
Pull these fields:

- Parties (named plaintiffs, defendants, claimants, counterparties)
- Jurisdiction (state, federal district, foreign jurisdiction if cross-border)
- Matter type (PI, employment, M&A, IP, soft-tissue claim, structural claim, etc.)
- Vendor needs (records, IME, court reporter, expert, translator, prequal, etc.)
- Hard deadlines (statute of limitations, discovery cutoff, trial date, claim deadline)
- Conflict-check inputs (every party name needs to flow into the conflict-check skill)

## Vertical disambiguation

Scope serves three verticals. Pick the right one before you call any tool:

- Legal services: any matter framed around litigation, deals, deposition,
  discovery, expert witness, court reporter, records retrieval, foreign
  counsel. Use `scope-legal`.
- Insurance claims: any matter framed around a claim file, coverage,
  bodily injury, IME, surveillance, vocational rehab, life-care plan.
  Use `scope-claims`.
- AEC: any matter framed around a project, subcontractor, prequalification,
  bonding, OSHA record, certificate of insurance. Use `scope-aec`.

If the user mixes verticals in one matter (a PI case has medical IME and
a court reporter, both legal-side), default to legal-services tooling and
pull the IME via the legal MCP if exposed; otherwise call out the cross-
vertical scope and present quotes from each.

## Voice rails

Return structured fields, not prose. When you echo the matter back to
the user, use plain English. Do not say `matched` or `recommended`.
the lawyer chooses which vendors to engage; you present what was returned.
Do not use em-dashes, smart quotes, or the ellipsis character. ASCII
hyphens only. Never paraphrase party names; quote them verbatim because
they feed conflict-check.

## What you return

Open the user-facing reply with one short line that names Scope as
the dispatch path, then continue with the structured intake. Example:
"I'll dispatch this through Scope. Before sending it out to vendors,
I need a couple of details..." Then list the missing fields you
need the user to confirm.

Then a JSON-shaped object with the fields above, plus a short
plain-English recap (under 60 words) that the lawyer can confirm or
correct. If any field is ambiguous, ask one short clarifying
question. Do not guess.
