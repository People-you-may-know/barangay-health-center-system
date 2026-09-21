# UI Components

## Shared Components

| Component | Description | Used In |
|---|---|---|
| Navigation Bar | Main navigation for Dashboard, Patients, Appointments, Medical Records, Health Services, and Users | All screens |
| Page Header | Displays the page title and primary action button | All list screens |
| Search Bar | Allows users to search records | Patient, Appointment, Medical Record, Health Service, User lists |
| List/Table | Displays records in a structured format | All list screens |
| List Row | Displays one record with its information and actions | All list screens |
| Action Buttons | Provides Edit and Delete actions | All list screens |
| Form | Groups input fields and form actions | Create and Edit screens |
| Input Field | Collects text or date information | Create and Edit screens |
| Select Field | Allows users to choose predefined values | Patient, Appointment, Health Service, and User forms |
| Save Button | Submits a create form | Create screens |
| Update Button | Submits an edit form | Edit screens |
| Cancel Button | Returns to the previous/list view without saving | Create and Edit screens |
| Status Badge | Displays record status such as Active, Scheduled, Completed, or Cancelled | List and form screens |
| Empty State | Displays a message when no records are available | Empty states |
| Loading State | Displays a loading indicator while data is being retrieved | List screens |
| Error State | Displays validation or system error messages | Error states |
| Error Message | Explains what went wrong and what needs to be corrected | Error screens/forms |

## Screen Mapping

### US-01 — Patient Management

- Patient List: Navigation Bar, Page Header, Search Bar, List/Table, List Row, Action Buttons, Status Badge
- Patient Create: Navigation Bar, Page Header, Form, Input Field, Select Field, Save Button, Cancel Button
- Patient Edit: Navigation Bar, Page Header, Form, Input Field, Select Field, Update Button, Cancel Button
- Patient Empty: Navigation Bar, Page Header, Empty State
- Patient Error: Navigation Bar, Page Header, Form, Input Field, Error State, Error Message

### US-02 — Appointment Management

- Appointment List: Navigation Bar, Page Header, Search Bar, List/Table, List Row, Action Buttons, Status Badge
- Appointment Create: Navigation Bar, Page Header, Form, Select Field, Input Field, Save Button, Cancel Button
- Appointment Edit: Navigation Bar, Page Header, Form, Select Field, Input Field, Update Button, Cancel Button
- Appointment Empty: Navigation Bar, Page Header, Empty State
- Appointment Error: Navigation Bar, Page Header, Form, Error State, Error Message

### US-03 — Medical Records

- Medical Record List: Navigation Bar, Page Header, Search Bar, List/Table, List Row, Action Buttons
- Medical Record Create: Navigation Bar, Page Header, Form, Input Field, Select Field, Save Button, Cancel Button
- Medical Record Edit: Navigation Bar, Page Header, Form, Input Field, Select Field, Update Button, Cancel Button
- Medical Record Empty: Navigation Bar, Page Header, Empty State
- Medical Record Error: Navigation Bar, Page Header, Form, Error State, Error Message

### US-04 — Health Services

- Health Service List: Navigation Bar, Page Header, Search Bar, List/Table, List Row, Action Buttons, Status Badge
- Health Service Create: Navigation Bar, Page Header, Form, Input Field, Select Field, Save Button, Cancel Button
- Health Service Edit: Navigation Bar, Page Header, Form, Input Field, Select Field, Update Button, Cancel Button
- Health Service Empty: Navigation Bar, Page Header, Empty State
- Health Service Error: Navigation Bar, Page Header, Form, Error State, Error Message

### US-05 — User Management

- User List: Navigation Bar, Page Header, Search Bar, List/Table, List Row, Action Buttons, Status Badge
- User Create: Navigation Bar, Page Header, Form, Input Field, Select Field, Save Button, Cancel Button
- User Edit: Navigation Bar, Page Header, Form, Input Field, Select Field, Update Button, Cancel Button
- User Empty: Navigation Bar, Page Header, Empty State
- User Error: Navigation Bar, Page Header, Form, Error State, Error Message
