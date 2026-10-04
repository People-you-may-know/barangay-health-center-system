# Week 7 AI Notes

## Purpose

Document the AI-assisted work used for Week 7 asynchronous form binding.

## Prompts used

- Review the existing Flask patient API and design a Fetch-based patient Create and Update form.
- Add visible loading, success, validation, 404, server, and network states.
- Disable the submit button while an asynchronous save is pending.
- Bind the patient list to GET /patients and support asynchronous DELETE.
- Create manual end-to-end test cases for the Week 7 requirements.

## Team review

The implementation was reviewed against the existing patient API routes and validation responses. The frontend uses the backend field names: firstName, lastName, dateOfBirth, gender, contactNumber, and address.

## Notes

The backend returns 422 validation responses with a field name and error message, which the form displays beside the affected field.
