# Week 10 AI Notes

## AI scaffolding prompts
- Generate a critical-path unittest suite for the existing Flask patient API without changing application behavior.
- Build a QA matrix using happy, boundary, invalid, empty, and permissions scenarios.
- Review validation for adversarial inputs such as huge values, emoji, empty input, and script-like text.
- Identify a data-integrity bug to log during feature-freeze QA instead of fixing.
- Create a QA checklist for double-clicks, missing-record URLs, deleted records, and network failures.

## Human QA decisions
The team owns QA design and bug triage. AI was used only to scaffold the matrix and automated critical-path coverage.

The date-validation finding is intentionally left unfixed because Week 10 is a feature-freeze week. It is recorded for the next week's fix cycle.

## Review boundary
No feature implementation was added to correct the discovered date-validation problem in this Week 10 branch.
