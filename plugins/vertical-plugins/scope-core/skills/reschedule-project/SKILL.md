---
name: reschedule-project
description: Reschedule an already-awarded project to a new date. Fires only when the user is asking to change the date of an active engagement (project status is active, post-award and pre-delivery). Do NOT fire when the project has already been delivered or completed, when the project is being cancelled (use a cancel tool for that, not reschedule), when the user is asking about possible dates without committing to a change, or when the project hasn't been awarded yet.
type: auto
triggers:
  - reschedule
  - push the date
  - move the date
  - change the booking
  - new date for
  - bump the depo
  - bump the ime
  - postpone
allowed_tools:
  - scope-legal__scope_reschedule_project
  - scope-claims__scope_reschedule_project
  - scope-aec__scope_reschedule_project
---

# Reschedule project

When the buyer needs to change the date of a booked engagement, you call
`scope_reschedule_project` against the relevant vertical. The platform owns
state validation - you do not need to check whether the project is in a
reschedulable state; the API returns a typed error if it is not.

## Inputs you need from the user

Before calling the tool:

- `project_id` (the PJ-XXXX identifier, or its UUID).
- `new_date` (ISO 8601, e.g. `2026-06-15T10:00:00Z`).

Optional:

- `new_duration_minutes` if the duration is also changing.
- `reason` (short, used in the vendor notification email and audit row).

If the user gives a relative date ("push it back a week"), do NOT guess the
new specific date. Ask for an absolute date and confirm before calling the
tool. Same rule as matter-intake-parsing's relative-date discipline.

## Response shape

On success:

```json
{
  "success": true,
  "new_confirmed_slot": "2026-06-15T10:00:00Z",
  "vendor_notified": true,
  "audit_log_id": "uuid"
}
```

On typed failure:

- `project_already_delivered` - the work shipped or was confirmed complete.
  Cannot reschedule. Tell the user the project is closed and offer to
  open a new dispatch if they need follow-on work.
- `project_cancelled` - the project was cancelled. Cannot reschedule. Tell
  the user the engagement is closed.
- `invalid_state` - usually means the project is in a disputed state, or
  in a state the system does not recognize. Tell the user there is a
  dispute or status issue blocking the reschedule and to resolve it
  through the portal.
- `project_not_found` - the ID didn't resolve or the user is not on the
  project's buyer org. Confirm the ID with the user.
- `vendor_declined_new_slot` - the vendor's calendar conflicts with the
  proposed date (future-state; not enforced today). Propose a different
  date or open a follow-up.
- `other` - unspecified. Surface the error and tell the user to retry or
  contact support.

## Voice rails

Do not use the words "matched" or "recommended." ASCII hyphens only. No
em-dashes, no smart quotes. The buyer chose the new date; you confirm the
booking and surface whether the vendor was notified.

## Do NOT fire when

- The project has already been delivered or marked complete.
- The project is being cancelled. Use the cancel tool, not reschedule.
- The user is exploring possible dates without committing to a change.
  Ask them to commit to one specific new date first.
- The work hasn't been awarded yet (project does not exist).
- The user is asking about a different dispatch on a different scope.
  Resolve the project_id first.
