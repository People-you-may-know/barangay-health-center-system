(() => {
    const tableBody = document.querySelector("#patients-body");
    const status = document.querySelector("#list-status");
    if (!tableBody) return;

    const show = (message, type = "info", retry = null) => {
        if (window.AppFeedback) {
            window.AppFeedback.show(status, message, type, retry);
        } else if (status) {
            status.textContent = message;
        }
    };

    const escapeHtml = (value) => String(value ?? "")
        .replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;").replaceAll("'", "&#039;");

    const renderPatients = (patients) => {
        if (!patients.length) {
            tableBody.innerHTML = '<tr><td colspan="8">No patients found. Add a patient to get started.</td></tr>';
            return;
        }

        tableBody.innerHTML = patients.map((patient) => `
            <tr>
                <td>${escapeHtml(patient.id)}</td><td>${escapeHtml(patient.firstName)}</td>
                <td>${escapeHtml(patient.lastName)}</td><td>${escapeHtml(patient.dateOfBirth)}</td>
                <td>${escapeHtml(patient.gender)}</td><td>${escapeHtml(patient.contactNumber)}</td>
                <td>${escapeHtml(patient.address)}</td>
                <td><div class="action-buttons">
                    <a href="edit.html?id=${encodeURIComponent(patient.id)}" class="edit-button">Edit</a>
                    <button type="button" class="delete-button" data-id="${escapeHtml(patient.id)}">Delete</button>
                </div></td>
            </tr>`
        ).join("");
    };

    const loadPatients = async () => {
        show("Loading patients...", "loading");
        tableBody.innerHTML = '<tr><td colspan="8">Loading...</td></tr>';

        try {
            const response = await fetch("/patients");
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                show("We couldn't load the patient list. Please try again.", "error", loadPatients);
                return;
            }

            renderPatients(data.data || []);
            show("Patients loaded successfully.", "success");
        } catch (error) {
            show("We couldn't connect to the server. Check your connection and try again.", "error", loadPatients);
        }
    };

    tableBody.addEventListener("click", async (event) => {
        const button = event.target.closest(".delete-button");
        if (!button) return;

        const patientId = button.dataset.id;
        if (!window.confirm(`Delete patient #${patientId}? This cannot be undone.`)) return;

        button.disabled = true;
        show("Deleting patient...", "loading");

        try {
            const response = await fetch(`/patients/${patientId}`, { method: "DELETE" });
            const data = await response.json().catch(() => ({}));

            if (response.status === 404) {
                show("Patient not found. The record may already have been removed.", "error", loadPatients);
                return;
            }

            if (!response.ok) {
                show("We couldn't delete the patient. Please try again.", "error", loadPatients);
                return;
            }

            await loadPatients();
            show("Patient deleted successfully.", "success");
        } catch (error) {
            show("We couldn't connect to the server. The patient was not confirmed as deleted.", "error", loadPatients);
        } finally {
            button.disabled = false;
        }
    });

    loadPatients();
})();