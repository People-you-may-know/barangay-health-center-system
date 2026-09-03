Routing Table

Patient Management

| Method | Path | Handler | Story it serves |

|---|---|---|---|

| GET | /patients | listPatients | View all patient records |

| GET | /patients/:id | showPatient | View one patient |

| POST | /patients | createPatient | Create a new patient record |

| PUT | /patients/:id | updatePatient | Update patient information |

| DELETE | /patients/:id | deletePatient | Delete patient records |

Appointment Management

| Method | Path | Handler | Story it serves |

|---|---|---|---|

| GET | /appointments | listAppointments | View appointment list |

| GET | /appointments/:id | showAppointment | View one appointment |

| POST | /appointments | createAppointment | Create appointment |

| PUT | /appointments/:id | updateAppointment | Update appointment schedule |

| DELETE | /appointments/:id | deleteAppointment | Cancel/Delete appointment |

Medical Records

| Method | Path | Handler | Story it serves |

|---|---|---|---|

| GET | /medical-records | listMedicalRecords | View medical history |

| GET | /medical-records/:id | showMedicalRecord | View one medical record |

| POST | /medical-records | createMedicalRecord | Add medical record |

| PUT | /medical-records/:id | updateMedicalRecord | Update diagnosis and treatment |

| DELETE | /medical-records/:id | deleteMedicalRecord | Delete medical record |

Health Services

| Method | Path | Handler | Story it serves |

|---|---|---|---|

| GET | /health-services | listHealthServices | View health services |

| GET | /health-services/:id | showHealthService | View one health service |

| POST | /health-services | createHealthService | Add health service |

| PUT | /health-services/:id | updateHealthService | Update service information |

| DELETE | /health-services/:id | deleteHealthService | Delete health service |

User Management

| Method | Path | Handler | Story it serves |

|---|---|---|---|

| GET | /users | listUsers | View registered users |

| GET | /users/:id | showUser | View one user |

| POST | /users | createUser | Create staff account |

| PUT | /users/:id | updateUser | Update user information |

| DELETE | /users/:id | deleteUser | Delete user account |

Example Requests and Responses

Patient Management

GET /patients

Example request:


GET /patients
