# Week 12 / Deliverable 4 — Team Retrospective

## What went well

- The team moved from a basic Flask application toward a structured request/response workflow with controllers and API routes.
- Asynchronous UI behavior and clearer loading, success, and error feedback were introduced.
- Error handling was strengthened for validation, missing records, and network/server failures.
- Code review work and automated API coverage were added.
- QA work added critical-path tests, adversarial scenarios, and date-validation coverage.
- The interface work added reusable loading, success, error, retry, detail, create, and edit patterns.
- The production application was deployed on Railway and connected to Railway MySQL.
- The team kept work visible through branches, pull requests, commits, and documentation.

## What did not go well

- Some manual browser QA still needs to be captured as explicit evidence rather than inferred from documentation.
- Production deployment required a separate database initialization step because the Railway MySQL database initially existed without the application's tables.
- The project contains historical in-memory implementation files/commits alongside the current MySQL-backed release path, so the release configuration needs to be kept consistent.
- Some validation patterns are duplicated between application/controller layers.

## What we learned

1. Build reusable UI behavior instead of repeating request logic in every screen.
2. Test invalid input, missing resources, and permission failures—not only the happy path.
3. A string can have the correct shape while still containing invalid domain data; date validation must check the actual calendar value.
4. Automated tests are most useful when they protect a specific behavior or previously discovered bug.
5. Treat deployment configuration as code and verify it before presentation day.
6. Keep an explicit release gate for unresolved P0/P1 issues.
7. Each member should understand and be able to explain their own committed work.
8. A production web deployment and its database schema must be verified together.

## What we would change next time

1. Choose the production hosting and data-storage approach earlier.
2. Introduce and standardize the persistent database/migration workflow before final deployment.
3. Centralize validation rules so API behavior cannot drift between layers.
4. Run browser/manual QA continuously instead of waiting for the dedicated QA period.
5. Keep small, focused commits and PRs throughout each feature cycle.
6. Rehearse the live demo with a tested backup path.

## What we will improve before final sign-off

- Complete and document the full production CRUD smoke test.
- Run and record the final automated suite result.
- Verify the remaining production failure paths.
- Resolve all P0/P1 release blockers.
- Prepare a backup demo and rehearse the individual defense.

## Blameless note

Issues are treated as system/process problems rather than individual failures. The focus is on making validation, testing, review, deployment, and documentation repeatable.

## Final status

The application is deployed on Railway with a Railway MySQL database, and login/dashboard access has been verified. The final release still requires explicit production CRUD/failure-path evidence, final QA sign-off, a rehearsed demo, and the individual unassisted defense.
