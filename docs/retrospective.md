# Week 12 — Team Retrospective

## What went well

- The team moved from a basic Flask application toward a structured request/response workflow with controllers and API routes.
- Week 7 introduced asynchronous UI behavior and clearer loading, success, and error feedback.
- Week 8 strengthened error handling for validation, missing records, and network/server failures.
- Week 9 added code review work and automated patient API coverage, including protection against patient ID reuse after deletion.
- Week 10 added a QA matrix, critical-path tests, adversarial scenarios, and a documented P1 date-validation bug.
- Week 11 fixed the date-validation bug, added release configuration, and prepared deployment documentation and CI test automation.

## What did not go well

- Some manual browser QA remained dependent on team execution instead of being fully captured automatically.
- The project still uses in-memory Python lists, so data does not persist across application restarts and there is no database migration workflow yet.
- Deployment was prepared in the repository, but the final public hosting step still depends on the team selecting and provisioning a host.
- The project accumulated duplicated validation patterns between the application and controller layers.

## What we would change next time

1. Choose the production hosting and data-storage approach earlier instead of leaving deployment until the final weeks.
2. Introduce a persistent database and migrations before building out more CRUD modules.
3. Centralize validation rules so API behavior cannot drift between layers.
4. Run browser/manual QA continuously instead of waiting for the dedicated QA week.
5. Keep small, focused commits and PRs throughout each feature cycle.

## Lessons learned

### Technical

- A string can have the correct shape while still containing invalid domain data; date validation must check the actual calendar value.
- Automated tests are most useful when they protect a specific behavior or previously discovered bug.
- Environment-specific configuration belongs outside source code, especially for production settings.
- A release is more than working code: it also needs tests, configuration, deployment notes, and a smoke-test plan.

### Team process

- Small branches and reviewed pull requests make changes easier to understand and verify.
- A blameless retrospective should focus on the process and the next improvement, not individual fault.
- AI can accelerate scaffolding and review, but team members must understand and defend their own code.

## Final status

The repository contains the Week 12 retrospective and presentation/defense preparation materials. The team must still complete the actual live deployment, live demo, and individual unassisted defense before final sign-off.
