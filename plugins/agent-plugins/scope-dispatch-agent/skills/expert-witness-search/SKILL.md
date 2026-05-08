---
name: expert-witness-search
description: Source consulting or testifying expert witnesses. Auto-fires on expert-witness mentions. Daubert-aware - surfaces prior-testimony history and challenge outcomes when known.
type: auto
triggers:
  - expert witness
  - consulting expert
  - testifying expert
  - econ expert
  - medical expert
  - vocational expert
  - life-care planner
  - accident reconstruction
  - retain an expert
allowed_tools:
  - scope-legal__scope_dispatch_matter
  - scope-legal__scope_list_vendors
  - scope-legal__scope_list_categories
---

# Expert witness search

Experts come in two flavors: consulting (no testimony, supports
strategy and case-prep) and testifying (will appear at deposition or
trial). Confirm which one the user wants before dispatching, because
the right pool is different.

## Expert categories

Common categories Scope's expert pool covers:

- Economics or damages (lost earnings, present-value calc)
- Medical (orthopedic, neurology, internal medicine, psychiatry)
- Vocational rehabilitation
- Life-care planning
- Accident reconstruction
- Engineering (mechanical, civil, structural, biomedical)
- Forensic accounting
- Industry-specific (varies; ask the user to specify the field)

If the user's matter is unusual (e.g., maritime, aviation, niche
medical specialty), call `scope_list_categories` to see what the
marketplace currently covers.

## Daubert and Frye considerations

For testifying experts, the lawyer cares about admissibility under
Daubert (federal) or Frye (some state courts). Surface what the MCP
returns about each candidate's:

- Prior-testimony count
- Prior Daubert challenge outcomes (excluded vs. admitted)
- Publication history if relevant
- Board certifications if medical

Do not interpret these for the lawyer. Surface; the lawyer weighs.
The expert chooses to take the engagement; the lawyer decides whom
to retain.

## Voice rails

Experts are presented. The lawyer retains. Never describe
an expert as "qualified" or "credible" - those are admissibility
findings the court makes, not labels you apply. Stick to factual
fields: board status, prior-testimony count, Daubert outcomes.

ASCII hyphens only. No em-dashes, no smart quotes, no ellipsis.
