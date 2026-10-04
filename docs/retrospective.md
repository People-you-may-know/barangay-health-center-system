# Week 12 / Deliverable 4 — Team Retrospective

## What went well

- The team moved from a basic Flask application toward a structured request/response workflow with controllers and API routes.
- Asynchronous UI behavior and clearer loading, success, and error feedback were introduced.
- Error handling was strengthened for validation, missing records, and network/server failures.
- Code review work and automated patient API coverage were added, including protection against patient ID reuse after deletion.
- QA work added critical-path tests, adversarial scenarios, and date-validation coverage.
- The interface work added reusable loading, success, error, retry, detail, create, and edit patterns.
- The team kept work visible through branches, pull requests, commits, and documentation.

## What did not go well

- Some manual browser QA remained dependent on team execution instead of being fully captured automatically.
- Deployment was prepared in the repository, but the final public hosting step still depends on the team selecting and provisioning a host.
- The project has had both in-memory and MySQL-backed development variants, so the release branch must be chosen carefully and its runtime configuration verified before deployment.
- Some validation patterns are duplicated between application/controller layers.

## What we learned

1. Build reusable UI behavior instead of repeating request logic in every screen.
2. Test invalid input, missing resources, and permission failures—not only the happy path.
3. A string can have the correct shape while still containing invalid domain data; date validation must check the actual calendar value.
4. Automated tests are most useful when they protect a specific behavior or previously discovered bug.
5. Treat deployment configuration as code and verify it before presentation day.
6. Keep an explicit release gate for unresolved P0/P1 issues.
7. Each member should understand and be able to explain their own committed work.

## What we would change next time

1. Choose the production hosting and data-storage approach earlier.
2. Introduce and standardize the persistent database/migration workflow before final deployment.
3. Centralize validation rules so API behavior cannot drift between layers.
4. Run browser/manual QA continuously instead of waiting for the dedicated QA period.
5. Keep small, focused commits and PRs throughout each feature cycle.
6. Rehearse the live demo with a tested backup path.

## What we will improve before final sign-off

- Complete and verify the public deployment.
- Run the full automated suite in CI and record the result.
- Perform the remaining manual UI/production matrix.
- Resolve all P0/P1 release blockers.
- Prepare a backup demo and rehearse the individual defense.

## Blameless note

Issues are treated as system/process problems rather than individual failures. The focus is on making validation, testing, review, deployment, and documentation repeatable.

## Final status

The repository contains the QA, deployment, retrospective, and presentation preparation materials. The team must still complete the actual live deployment, live demo, and individual unassisted defense before final sign-off.
