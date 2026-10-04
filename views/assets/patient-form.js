(() => {
    const form = document.querySelector("#patient-form");
    if (!form) return;

    const status = document.querySelector("#form-status");
    const submitButton = form.querySelector('button[type="submit"]');
    const patientId = new URLSearchParams(window.location.search).get("id");
    const isEdit = Boolean(patientId);

    const show = (message, type = "info", retry = null) => {
        if (window.AppFeedback) {
            window.AppFeedback.show(status, message, type, retry);
        } else if (status) {
            status.textContent = message;
        }
    };

    const clearErrors = () => {
        form.querySelectorAll(".field-error").forEach((element) => element.textContent = "");
    };

    const showFieldError = (field, message) => {
        const error = form.querySelector(`[data-error-for="${field}"]`);
        if (error) error.textContent = message;
    };

    const setSaving = (saving) => {
        submitButton.disabled = saving;
        submitButton.textContent = saving
            ? (isEdit ? "Updating..." : "Saving...")
            : (isEdit ? "Update Patient" : "Save Patient");
    };

    const request = async (url, options = {}) => {
        const response = await fetch(url, options);
        const data = await response.json().catch(() => ({}));
        return { response, data };
    };

    const loadPatient = async () => {
        if (!isEdit) return;

        show("Loading patient...", "loading");

        try {
            const { response, data } = await request(`/patients/${patientId}`);

            if (response.status === 404) {
                show("Patient not found. Check the patient ID and try again.", "error", loadPatient);
                return;
            }

            if (!response.ok) {
                show("We couldn't load this patient. Please try again.", "error", loadPatient);
                return;
            }

            const patient = data.data;
            for (const [field, value] of Object.entries(patient)) {
                const input = form.elements[field];
                if (input && field !== "id") input.value = value ?? "";
            }

            const idDisplay = document.querySelector("#patient-id");
            if (idDisplay) idDisplay.textContent = patient.id;
            show("Patient loaded.", "success");
        } catch (error) {
            show("We couldn't connect to the server. Check your connection and try again.", "error", loadPatient);
        }
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearErrors();

        if (!form.reportValidity()) return;

        setSaving(true);
        show(isEdit ? "Updating patient..." : "Saving patient...", "loading");

        const payload = Object.fromEntries(new FormData(form).entries());
        const url = isEdit ? `/patients/${patientId}` : "/patients";
        const options = {
            method: isEdit ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        };

        try {
            const { response, data } = await request(url, options);

            if (response.status === 422) {
                showFieldError(data.field, data.error || "Please correct this field.");
                show("Please correct the highlighted field and try again.", "error");
                return;
            }

            if (response.status === 404) {
                show("Patient not found. The record may have been removed.", "error");
                return;
            }

            if (!response.ok) {
                show("We couldn't save the patient. Please try again.", "error", () => form.requestSubmit());
                return;
            }

            show(isEdit ? "Patient updated successfully." : "Patient created successfully.", "success");
            setTimeout(() => { window.location.href = "index.html"; }, 700);
        } catch (error) {
            show("We couldn't connect to the server. Check your connection and try again.", "error", () => form.requestSubmit());
        } finally {
            setSaving(false);
        }
    });

    loadPatient();
})();