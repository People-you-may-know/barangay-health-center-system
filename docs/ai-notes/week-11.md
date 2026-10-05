# Week 11 AI Notes

## Prompts used

- Review the Week 10 P1 finding and propose a small, testable fix for invalid calendar dates.
- Add automated tests for impossible dates, non-leap-year February 29, and a valid leap-day date.
- Review the Flask app for a small meaningful cleanup related to production configuration.
- Prepare environment-variable and deployment documentation without adding secrets to the repository.
- Review and update the Week 11 deployment documentation to match the team's actual Railway production deployment and clearly separate verified checks from remaining release-gate checks.

## Human review decisions

- The Week 10 P1 date-validation issue was reproduced from the existing length-only validation and fixed with real calendar parsing.
- The fix is covered by automated tests before it is considered ready for merge.
- Production debug behavior is controlled by `APP_DEBUG`.
- The application is deployed on Railway with a Railway MySQL service.
- The public application URL was opened successfully, login succeeded, and the dashboard opened against the Railway database.
- The Railway MySQL schema was initialized in the `railway` database and the required application tables were verified.
- The final production CRUD and failure-path smoke tests must still be completed before declaring the full release gate complete.

## Release boundary

No new application feature was added. This Week 11 contribution updates deployment documentation to reflect the actual production environment and records which release checks have been verified versus which still require final smoke testing.
