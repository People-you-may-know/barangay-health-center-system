# Week 8 Feedback Matrix

| Action | Loading | Success | Error |
|---|---|---|---|
| Create patient | Save button disabled and “Saving...” shown | Success message, then return to list | Inline 422 field errors; helpful retry for server/network errors |
| Load patient list | Loading message and table placeholder | Rows render and success feedback | Helpful error with Retry |
| Load patient for edit | Loading message | Form is populated | 404 not-found message or Retry for server/network failure |
| Update patient | Update button disabled and “Updating...” shown | Success message, then return to list | Inline 422 errors; 404 not-found; Retry for server/network failure |
| Delete patient | Delete button disabled and “Deleting...” shown | List refreshes and deletion is confirmed | 404 message or Retry for server/network failure |

## Shared behavior

All patient screens use the shared `AppFeedback` helper for consistent loading, success, and error presentation. Destructive delete actions require confirmation before the request is sent.
