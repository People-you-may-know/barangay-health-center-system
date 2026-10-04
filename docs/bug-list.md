# Deliverable 4 — Triaged Bug List

| ID | Priority | Issue | Status | Evidence / resolution |
|---|---|---|---|---|
| BUG-001 | P1 | Invalid calendar/date values need explicit validation beyond string length | Resolved in Week 11 | Week 11 fix and automated validation tests |
| BUG-002 | P1 | UI previously lacked consistent loading/success/error feedback | Resolved in Deliverable 3 branch | Shared async feedback binding added |
| BUG-003 | P1 | UI needed graceful 422/404/500/network handling | Resolved in Deliverable 3 branch | Reusable feedback + retry behavior added |
| BUG-004 | P1 | CRUD needed expanded automated coverage | In progress | `tests/test_deliverable4.py` added; run in CI/local |
| BUG-005 | P1 | No public production deployment URL yet | Open | Deployment must be completed and URL recorded before final submission |
| BUG-006 | P2 | Presentation/live demo backup not yet recorded | Open | Prepare backup screenshots/video/local fallback |
| BUG-007 | P2 | Final retrospective and deployment evidence were missing | Resolved | Deliverable 4 documentation added |

### Release gate

P0/P1 items must be resolved before claiming the final release. In particular, BUG-005 remains open until a real public deployment is completed and verified.
