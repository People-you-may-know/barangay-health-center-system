(() => {
    const form = document.querySelector("#patient-form");
    if (!form) return;

    const status = document.querySelector("#form-status");
    const submitButton = form.querySelector('button[type="submit"]');
    const patientId = new URLSearchParams(window.location.search).get("id");
    const isEdit = Boolean(patientId);

    const setStatus = (message, type = "") => {
        if (!status) return;
        status.textContent = message;
        status.className = `form-status ${type}`;
    };

    const clearErrors = () => {
        form.querySelectorAll(".field-error").forEach((element) => {
            element.textContent = "";
        });
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

    const parseResponse = async (response) => {
        const data = await response.json().catch(() => ({}));
        return { response, data };
    };

    const loadPatient = async () => {
        if (!isEdit) return;

        setStatus("Loading patient...", "loading");

        try {
            const { response, data } = await parseResponse(
                await fetch(`/patients/${patientId}`)
            );

            if (!response.ok) {
                if (response.status === 404) {
                    setStatus("Patient not found.", "error");
                } else {
                    setStatus(data.error || "Unable to load patient.", "error");
                }
                return;
            }

            const patient = data.data;
            for (const [field, value] of Object.entries(patient)) {
                const input = form.elements[field];
                if (input && field !== "id") input.value = value ?? "";
            }

            const idDisplay = document.querySelector("#patient-id");
            if (idDisplay) idDisplay.textContent = patient.id;

            setStatus("Patient loaded.", "success");
        } catch (error) {
            setStatus("Network error. Could not load the patient.", "error");
        }
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearErrors();
        setSaving(true);
        setStatus(isEdit ? "Updating patient..." : "Saving patient...", "loading");

        const payload = Object.fromEntries(new FormData(form).entries());

        try {
            const response = await fetch(
                isEdit ? `/patients/${patientId}` : "/patients",
                {
                    method: isEdit ? "PUT" : "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                }
            );

            const { data } = await parseResponse(response);

            if (response.status === 422) {
                showFieldError(data.field, data.error || "Invalid value.");
                setStatus("Please correct the highlighted field.", "error");
                return;
            }

            if (response.status === 404) {
                setStatus("Patient not found.", "error");
                return;
            }

            if (!response.ok) {
                setStatus(data.error || "The server could not save the patient.", "error");
                return;
            }

            setStatus(
                isEdit ? "Patient updated successfully." : "Patient created successfully.",
                "success"
            );

            setTimeout(() => {
                window.location.href = "index.html";
            }, 500);
        } catch (error) {
            setStatus("Network error. Please check that the server is running.", "error");
        } finally {
            setSaving(false);
        }
    });

    loadPatient();
})();