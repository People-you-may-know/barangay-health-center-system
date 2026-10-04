# Deliverable 3 Feedback Matrix

| Action | Loading | Success | 422 | 404 | 403 | 500/server | Network |
|---|---|---|---|---|---|---|---|
| List records | Loading table + status | Records render | — | Human-readable failure | Permission message | Retry message | Connection + Retry |
| Load detail | Loading detail | Detail renders | — | Record not found | Permission message | Retry message | Connection + Retry |
| Create | Button disabled + Saving... | Success then return to list | Inline field error | Human-readable failure | Permission message | Retry | Connection + Retry |
| Update | Button disabled + Updating... | Success then return to list | Inline field error | Record not found | Permission message | Retry | Connection + Retry |
| Delete | Delete button disabled + Deleting... | List refresh + confirmation | — | Record not found | Permission message | Retry | Connection + Retry |

## Messaging rules

- No raw HTTP status codes are displayed to users.
- No stack traces or internal exception text are displayed.
- 422 validation feedback is shown beside the relevant field.
- 404 explains that the requested record could not be found.
- 500/server failures explain that the server could not complete the request and provide Retry.
- Network failures explain that the application could not connect and provide Retry.
- Destructive delete actions require confirmation.
