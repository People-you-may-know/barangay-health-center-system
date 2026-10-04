(() => {
    const tableBody = document.querySelector("#patients-body");
    const status = document.querySelector("#list-status");

    if (!tableBody) return;

    const setStatus = (message, type = "") => {
        if (!status) return;
        status.textContent = message;
        status.className = `info-message ${type}`;
    };

    const escapeHtml = (value) => String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

    const renderPatients = (patients) => {
        if (!patients.length) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="8">No patients found.</td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = patients.map((patient) => `
            <tr>
                <td>${escapeHtml(patient.id)}</td>
                <td>${escapeHtml(patient.firstName)}</td>
                <td>${escapeHtml(patient.lastName)}</td>
                <td>${escapeHtml(patient.dateOfBirth)}</td>
                <td>${escapeHtml(patient.gender)}</td>
                <td>${escapeHtml(patient.contactNumber)}</td>
                <td>${escapeHtml(patient.address)}</td>
                <td>
                    <div class="action-buttons">
                        <a href="edit.html?id=${encodeURIComponent(patient.id)}" class="edit-button">Edit</a>
                        <button type="button" class="delete-button" data-id="${escapeHtml(patient.id)}">Delete</button>
                    </div>
                </td>
            </tr>
        `).join("");
    };

    const loadPatients = async () => {
        setStatus("Loading patients...", "loading");

        try {
            const response = await fetch("/patients");
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                setStatus(data.error || "Unable to load patients.", "error");
                return;
            }

            renderPatients(data.data || []);
            setStatus("Patients loaded successfully.", "success");
        } catch (error) {
            setStatus("Network error. Please check that the server is running.", "error");
        }
    };

    tableBody.addEventListener("click", async (event) => {
        const button = event.target.closest(".delete-button");
        if (!button) return;

        const patientId = button.dataset.id;
        if (!window.confirm(`Delete patient #${patientId}?`)) return;

        button.disabled = true;
        setStatus("Deleting patient...", "loading");

        try {
            const response = await fetch(`/patients/${patientId}`, {
                method: "DELETE"
            });
            const data = await response.json().catch(() => ({}));

            if (response.status === 404) {
                setStatus("Patient not found.", "error");
                return;
            }

            if (!response.ok) {
                setStatus(data.error || "Unable to delete patient.", "error");
                return;
            }

            setStatus("Patient deleted successfully.", "success");
            await loadPatients();
        } catch (error) {
            setStatus("Network error. Please check that the server is running.", "error");
        } finally {
            button.disabled = false;
        }
    });

    loadPatients();
})();