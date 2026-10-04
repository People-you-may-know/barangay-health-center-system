# Week 11 AI Notes

## Prompts used

- Review the Week 10 P1 finding and propose a small, testable fix for invalid calendar dates.
- Add automated tests for impossible dates, non-leap-year February 29, and a valid leap-day date.
- Review the Flask app for a small meaningful cleanup related to production configuration.
- Prepare environment-variable and deployment documentation without adding secrets to the repository.

## Human review decisions

- The Week 10 P1 date-validation issue was reproduced from the existing length-only validation and fixed with real calendar parsing.
- The fix is covered by automated tests before it is considered ready for merge.
- Production debug behavior is now controlled by `APP_DEBUG` instead of being hard-coded on.
- The current app has no persistent database or migration system, so deployment documentation records that limitation rather than inventing a migration command.
- The team must still choose a host, deploy, and record the real public URL before final sign-off.

## Release boundary

No new application feature was added. Week 11 focuses on fixing the P1 QA bug, paying down small release-readiness debt, documenting configuration, and preparing the application for deployment.
