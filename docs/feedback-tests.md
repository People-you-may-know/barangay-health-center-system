# Week 8 Feedback Tests

## Manual failure-path checklist

| Test | Steps | Expected result |
|---|---|---|
| 422 validation | Submit a patient form with invalid/missing data | Field-level error appears beside the affected field; no silent failure |
| 404 edit | Open `edit.html?id=999999` | Clear “Patient not found” message and Retry action |
| 404 delete | Delete a record that no longer exists | Clear not-found message and Retry action |
| Server failure | Make the API unavailable or return a non-2xx response | Human-readable error appears; Retry is available where the action can safely repeat |
| Network failure | Stop the server, then load the list | Connection message and Retry appear; page remains usable |
| Slow request | Delay the API response | Loading message remains visible and controls are disabled while pending |
| Delete confirmation | Click Delete | Confirmation appears before the destructive request |
| Helpful messages | Inspect all failure messages | No raw status codes or stack traces are shown to users |

## Run

1. Install dependencies with `pip install -r requirements.txt`.
2. Start the Flask app with `python app.py`.
3. Open `http://127.0.0.1:5000/ui/patients/index.html`.
4. Run each failure-path test and record the observed result.

## Acceptance

Every patient action has visible loading, success, and error feedback. 422 errors are inline, 404 errors are explicit, server/network errors offer a helpful next step, and delete requires confirmation.
