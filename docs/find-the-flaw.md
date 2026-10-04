# Week 9 — Find the Flaw

This document records the code-review findings required by the Week 9 lab. Each finding identifies what is wrong, why it matters, and the recommended fix.

## Finding 1 — Patient ID reuse after deletion

**Severity:** Blocking

**Flaw:** The original patient creation logic used `len(patients) + 1` for the next ID.

**Why it is wrong:** If patient 1 and patient 2 exist and patient 1 is deleted, the list length becomes 1. Creating another patient would calculate ID 2, duplicating an existing ID.

**Fix:** Generate the next ID from the highest existing ID plus one, with 0 as the empty-list default.

**Review comment:** “Blocking: Please avoid deriving the next patient ID from the collection length. After a deletion, that can reuse an existing ID. Generate the next ID from the highest current ID instead.”

**Status:** Fixed in Week 9.

## Finding 2 — Silent client failure

**Severity:** Blocking

**Flaw:** A Fetch request that only handles 200/201 can silently ignore 422, 404, 500, or network failures.

**Why it is wrong:** Users cannot tell whether their action failed or what they should do next.

**Fix:** Handle validation, not-found, server, and network branches with visible feedback and retry where safe.

**Review comment:** “Blocking: Please handle the non-success branches explicitly so a failed request never looks like a no-op.”

**Status:** Addressed in Week 8 and reviewed again in Week 9.

## Finding 3 — Destructive action without confirmation

**Severity:** Blocking

**Flaw:** A Delete button can send a destructive request immediately without confirmation.

**Why it is wrong:** An accidental click can remove a record with no opportunity to cancel.

**Fix:** Confirm before DELETE and disable the control while the request is pending.

**Review comment:** “Blocking: Add a confirmation step before DELETE and prevent duplicate submissions while the request is pending.”

**Status:** Addressed in Week 8 and reviewed again in Week 9.

## Finding 4 — Technical errors shown to users

**Severity:** Blocking

**Flaw:** Showing raw status codes or stack traces exposes implementation details and gives users no useful recovery step.

**Fix:** Convert failures into calm, specific messages and keep technical details out of the interface.

**Review comment:** “Blocking: Replace the technical response with a user-facing message that explains what happened and what the user can do next.”

**Status:** Addressed in Week 8 and reviewed again in Week 9.

## Review checklist

- [x] Correctness and edge cases considered
- [x] Readability considered
- [x] Response/error consistency checked
- [x] Validation and security considerations checked
- [x] Tests added for the reviewed patient API behavior
- [x] Findings labeled Blocking where a fix is required
- [x] Positive feedback: the API already uses a consistent JSON response shape and field-level 422 errors
