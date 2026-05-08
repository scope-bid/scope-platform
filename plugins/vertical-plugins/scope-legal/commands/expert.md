---
name: expert
description: Fast path for expert witness search - consulting or testifying.
---

When the user runs `/expert [type] [matter context]`, fire the
expert-witness-search skill.

Required fields: expert category (econ, medical, voc, life-care,
accident reconstruction, engineering, forensic accounting,
industry-specific), engagement type (consulting or testifying), brief
matter context.

Surface prior-testimony count, prior Daubert challenge outcomes, board
status, and rate. The lawyer retains.

If the user passes a line like `/expert testifying ortho, soft tissue
PI matter, neck injury`, parse the fields. If anything required is
missing, ask once.

Pass quotes to quote-comparison.
