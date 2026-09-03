Routing Table

This routing table defines the API endpoints for the Barangay Health Center Patient Record and Appointment Management System. Each route corresponds to a specific CRUD operation and supports the system’s user stories.

1. Patient Management

HTTP Method	Endpoint	Handler	Description
GET	/patients	list_patients	Retrieve and display all patient records.
GET	/patients/<id>	show_patient	Retrieve and display a specific patient record.
POST	/patients	create_patient	Create and save a new patient record.
PUT	/patients/<id>	update_patient	Update an existing patient’s information.
DELETE	/patients/<id>	delete_patient	Delete an existing patient record.

2. Appointment Management

HTTP Method	Endpoint	Handler	Description
GET	/appointments	list_appointments	Retrieve and display all appointments.
GET	/appointments/<id>	show_appointment	Retrieve and display a specific appointment.
POST	/appointments	create_appointment	Schedule a new patient appointment.
PUT	/appointments/<id>	update_appointment	Update an existing appointment.
DELETE	/appointments/<id>	delete_appointment	Cancel or remove an appointment.

3. Medical Records

HTTP Method	Endpoint	Handler	Description
GET	/medical-records	list_medical_records	Retrieve and display all medical records.
GET	/medical-records/<id>	show_medical_record	Retrieve a specific medical record.
POST	/medical-records	create_medical_record	Create a new medical record.
PUT	/medical-records/<id>	update_medical_record	Update an existing medical record.
DELETE	/medical-records/<id>	delete_medical_record	Delete a medical record.

4. Health Services

HTTP Method	Endpoint	Handler	Description
GET	/health-services	list_health_services	Retrieve and display all available health services.
GET	/health-services/<id>	show_health_service	Retrieve information about a specific health service.
POST	/health-services	create_health_service	Add a new health service.
PUT	/health-services/<id>	update_health_service	Update information about an existing health service.
DELETE	/health-services/<id>	delete_health_service	Remove a health service from the system.

5. User Management

HTTP Method	Endpoint	Handler	Description
GET	/users	list_users	Retrieve and display all system users.
GET	/users/<id>	show_user	Retrieve information about a specific user.
POST	/users	create_user	Create a new system user account.
PUT	/users/<id>	update_user	Update an existing user’s information.
DELETE	/users/<id>	delete_user	Delete a system user account.

HTTP Method Summary

* GET — Retrieve existing records.
* POST — Create new records.
* PUT — Update existing records.
* DELETE — Remove existing records.

Implementation Note

The Patient Management routes have been implemented in the current Flask application. The remaining resource routes are documented as part of the system’s planned routing structure and will be implemented as their corresponding features are developed.
