# UI Components — Deliverable 3

## Shared reusable components

- Navigation Bar — consistent movement between all modules.
- Page Header — title and primary create action.
- Data Table/List — populated asynchronously from backend controllers.
- Action Buttons — View, Edit, Delete.
- Create/Edit Form — reusable field and validation layout.
- Feedback Banner — loading, success, info, and error states.
- Inline Field Error — shows 422 validation messages beside the affected field.
- Retry Control — retries failed GET/save/delete operations.
- Empty State — explains when a collection has no records.
- Detail View — loads one record asynchronously.
- Disabled Pending Control — prevents duplicate submissions while a request is pending.

## Screen coverage

| Module | List | Detail | Create | Edit | Empty | Loading | Error |
|---|---|---|---|---|---|---|---|
| Patients | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Appointments | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Medical Records | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Health Services | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Users | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

All create/update operations use Fetch API and update the interface without a full-page form submission.