# Deliverable 4 — Retrospective

## What went well

- The project progressed from API/controller work to reusable interface feedback and view binding.
- CRUD validation and not-found cases have automated coverage.
- Deliverable 3 introduced reusable loading, success, error, and retry behavior instead of duplicating feedback logic.
- The team kept work visible through branches, pull requests, commits, and documentation.

## What was difficult

- Connecting separate views to consistent backend behavior required reusable conventions.
- Error handling had to cover more than the successful path.
- Deployment is a separate release concern from local development; a working localhost demo is not enough for this deliverable.

## What we learned

1. Build reusable UI behavior instead of repeating request logic in every screen.
2. Test invalid input and missing resources, not only valid CRUD.
3. Treat deployment configuration as code and verify it before presentation day.
4. Keep an explicit release gate for unresolved P0/P1 issues.
5. Each member should understand and be able to explain their own committed work.

## What we will improve

- Complete and verify the public deployment before final submission.
- Run the full automated suite in CI and record the result.
- Perform the remaining manual UI/production matrix.
- Prepare a backup demo and rehearse the individual defense.

## Blameless note

Issues were treated as system/process problems rather than individual failures. The focus is on making validation, testing, review, deployment, and documentation repeatable.
