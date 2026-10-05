# Production Manual QA Record

Public application:

**https://web-production-64a9f1.up.railway.app**

> Fill this record only after directly executing the test. Do not mark a case PASS from documentation alone.

| ID | Tester | Date/Time | Result | Evidence / Notes |
|---|---|---|---|---|
| PROD-01 | | | ⬜ | Public URL loads |
| PROD-02 | | | ⬜ | Login + dashboard |
| PROD-03 | | | ⬜ | Create patient |
| PROD-04 | | | ⬜ | View patient |
| PROD-05 | | | ⬜ | Edit patient + refresh persistence |
| PROD-06 | | | ⬜ | Delete patient |
| PROD-07 | | | ⬜ | Create appointment |
| PROD-08 | | | ⬜ | Edit/delete appointment |
| PROD-09 | | | ⬜ | Create medical record |
| PROD-10 | | | ⬜ | Edit/delete medical record |
| PROD-11 | | | ⬜ | View health services |
| PROD-12 | | | ⬜ | Create/edit/delete service |
| PROD-13 | | | ⬜ | User management |
| PROD-14 | | | ⬜ | Invalid data / 422 feedback |
| PROD-15 | | | ⬜ | Missing record / 404 feedback |
| PROD-16 | | | ⬜ | Recoverable network/server failure |
| PROD-17 | | | ⬜ | Refresh and verify persisted data |

## Adversarial QA

| Scenario | Result | Notes |
|---|---|---|
| Very large input | ⬜ | |
| Emoji/unusual text | ⬜ | |
| Script-like input | ⬜ | |
| Double-click submit | ⬜ | |
| Refresh/back during request | ⬜ | |
| Deleted/missing record | ⬜ | |
| Slow/offline network | ⬜ | |

## Release sign-off

- [ ] All required production CRUD paths directly tested.
- [ ] Invalid input behavior directly tested.
- [ ] Missing-record behavior directly tested.
- [ ] Failure/retry behavior directly tested.
- [ ] Evidence screenshots saved.
- [ ] Tester and date/time recorded.
