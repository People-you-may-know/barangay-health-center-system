# Week 7 Binding and Integration Tests

## Objective

Verify that the patient UI communicates with the Flask backend asynchronously using Fetch and handles loading, success, validation, not-found, server, and network states.

## Test cases

| Test | Action | Expected result |
| --- | --- | --- |
| 1 | Open patient list | GET /patients loads records into the table |
| 2 | Create valid patient | POST /patients returns 201 and the UI shows success |
| 3 | Create invalid patient | POST /patients returns 422 and the field error is displayed |
| 4 | Submit while saving | Save button is disabled and shows a saving state |
| 5 | Edit patient | GET /patients/{id} pre-fills the edit form |
| 6 | Update valid patient | PUT /patients/{id} returns 200 and the UI shows success |
| 7 | Edit missing patient | GET /patients/{id} returns 404 and the UI shows an error |
| 8 | Delete patient | DELETE /patients/{id} returns 200 and the list refreshes |
| 9 | Network/server failure | UI shows a visible network/server error |

## Manual run

1. Install dependencies:

   `pip install -r requirements.txt`

2. Start the Flask server:

   `python app.py`

3. Open:

   `http://127.0.0.1:5000/ui/patients/index.html`

4. Execute the test cases above and record the observed result.

## Acceptance

The Week 7 patient flow is considered complete when Create, Read, Update, and Delete actions use asynchronous requests and the UI visibly handles loading, success, validation, not-found, and network/server errors.
