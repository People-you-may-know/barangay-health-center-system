# Week 8 AI Notes

## AI-generated prompts

- Review the Week 7 patient Fetch binding and extend it to cover loading, success, 422, 404, 500/server, and network states.
- Create one shared feedback helper so patient screens use consistent status messages and Retry controls.
- Rewrite technical errors into specific, calm, actionable messages without exposing status codes or stack traces.
- Add delete confirmation and disable destructive controls while a request is pending.
- Create a failure-path test matrix covering validation, not-found, server, network, and slow requests.

## Hand-written review notes

- The backend's patient controller returns 422 for validation failures and 404 when a patient does not exist.
- The frontend treats other non-2xx responses as server failures and shows a human-readable retry message.
- Network exceptions are caught separately and show a connection message with Retry.
- Delete uses confirmation before sending the DELETE request.
- The shared `AppFeedback` helper keeps loading, success, and error presentation consistent.

## Review status

AI-generated scaffolding was reviewed against the Week 8 requirements and the existing patient API. The implementation keeps field-level validation inline and global failures in the shared feedback area.
