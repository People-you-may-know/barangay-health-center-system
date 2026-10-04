(() => {
  const feedback = (el, message, type = "info", retry = null) => {
    if (!el) return;
    el.className = `feedback feedback-${type}`;
    el.textContent = message;
    if (retry) {
      const b = document.createElement("button");
      b.type = "button"; b.className = "retry-button"; b.textContent = "Retry";
      b.addEventListener("click", retry, { once: true });
      el.appendChild(b);
    }
  };

  const json = async (response) => {
    const data = await response.json().catch(() => ({}));
    return { response, data };
  };

  const friendly = (response, fallback) => {
    if (response.status === 404) return "We couldn't find that record. It may have been removed.";
    if (response.status === 403) return "You don't have permission to perform this action.";
    if (response.status >= 500) return "The server couldn't complete that request. Please try again.";
    return fallback;
  };

  const escapeHtml = (v) => String(v ?? "").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;");

  const list = document.querySelector("[data-crud-list]");
  if (list) {
    const endpoint = list.dataset.endpoint;
    const body = list.querySelector("tbody");
    const status = document.querySelector("#list-status");
    const columns = JSON.parse(list.dataset.columns || "[]");
    const load = async () => {
      feedback(status, `Loading ${list.dataset.label || "records"}...`, "loading");
      if (body) body.innerHTML = `<tr><td colspan="${columns.length + 1}">Loading...</td></tr>`;
      try {
        const {response, data} = await json(await fetch(endpoint));
        if (!response.ok) {
          feedback(status, friendly(response, "We couldn't load the records. Please try again."), "error", load);
          return;
        }
        const rows = data.data || [];
        if (!rows.length) {
          body.innerHTML = `<tr><td colspan="${columns.length + 1}">No records found. Add a record to get started.</td></tr>`;
          feedback(status, "There are no records yet.", "info");
          return;
        }
        body.innerHTML = rows.map(item => {
          const cells = columns.map(c => {
            const value = item[c.key];
            return `<td>${escapeHtml(value)}</td>`;
          }).join("");
          return `<tr>${cells}<td class="action-buttons"><a class="edit-button" href="edit.html?id=${encodeURIComponent(item.id)}">Edit</a><button class="delete-button" data-id="${escapeHtml(item.id)}">Delete</button></td></tr>`;
        }).join("");
        feedback(status, "Records loaded successfully.", "success");
      } catch {
        feedback(status, "We couldn't connect to the server. Check your connection and try again.", "error", load);
      }
    };
    body?.addEventListener("click", async (event) => {
      const button = event.target.closest(".delete-button");
      if (!button) return;
      const id = button.dataset.id;
      if (!confirm(`Delete record #${id}? This cannot be undone.`)) return;
      button.disabled = true;
      feedback(status, "Deleting record...", "loading");
      try {
        const {response} = await json(await fetch(`${endpoint}/${encodeURIComponent(id)}`, {method:"DELETE"}));
        if (!response.ok) {
          feedback(status, friendly(response, "We couldn't delete the record. Please try again."), "error", load);
          return;
        }
        await load();
        feedback(status, "Record deleted successfully.", "success");
      } catch {
        feedback(status, "We couldn't connect to the server. The record was not confirmed as deleted.", "error", load);
      } finally { button.disabled = false; }
    });
    load();
  }

  const form = document.querySelector("[data-crud-form]");
  if (!form) return;
  const endpoint = form.dataset.endpoint;
  const id = new URLSearchParams(location.search).get("id");
  const edit = Boolean(id);
  const status = document.querySelector("#form-status");
  const submit = form.querySelector('button[type="submit"]');
  const fields = (form.dataset.fields || "").split(",").filter(Boolean);

  const clearErrors = () => form.querySelectorAll(".field-error").forEach(e => e.textContent = "");
  const fieldError = (field, message) => {
    const target = form.querySelector(`[data-error-for="${field}"]`);
    if (target) target.textContent = message;
  };

  const loadRecord = async () => {
    if (!edit) { feedback(status, "Ready to save a new record.", "info"); return; }
    feedback(status, "Loading record...", "loading");
    try {
      const {response, data} = await json(await fetch(`${endpoint}/${encodeURIComponent(id)}`));
      if (!response.ok) {
        feedback(status, friendly(response, "We couldn't load this record. Please try again."), "error", loadRecord);
        return;
      }
      const record = data.data || {};
      fields.forEach(name => { if (form.elements[name]) form.elements[name].value = record[name] ?? ""; });
      const idField = form.elements.id;
      if (idField) idField.value = record.id ?? id;
      feedback(status, "Record loaded.", "success");
    } catch {
      feedback(status, "We couldn't connect to the server. Check your connection and try again.", "error", loadRecord);
    }
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); clearErrors();
    if (!form.reportValidity()) return;
    submit.disabled = true;
    submit.textContent = edit ? "Updating..." : "Saving...";
    feedback(status, edit ? "Updating record..." : "Saving record...", "loading");
    const payload = {};
    fields.forEach(name => payload[name] = form.elements[name]?.value ?? "");
    try {
      const {response, data} = await json(await fetch(edit ? `${endpoint}/${encodeURIComponent(id)}` : endpoint, {
        method: edit ? "PUT" : "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
      }));
      if (response.status === 422) {
        fieldError(data.field, data.error || "Please correct this field.");
        feedback(status, "Please correct the highlighted field and try again.", "error");
        return;
      }
      if (!response.ok) {
        feedback(status, friendly(response, "We couldn't save the record. Please try again."), "error", () => form.requestSubmit());
        return;
      }
      feedback(status, edit ? "Record updated successfully." : "Record created successfully.", "success");
      setTimeout(() => location.href = "index.html", 700);
    } catch {
      feedback(status, "We couldn't connect to the server. Check your connection and try again.", "error", () => form.requestSubmit());
    } finally {
      submit.disabled = false;
      submit.textContent = edit ? "Update Record" : "Save Record";
    }
  });
  loadRecord();
})();

(() => {
  const detail = document.querySelector("[data-crud-detail]");
  if (!detail) return;
  const endpoint = detail.dataset.endpoint;
  const id = new URLSearchParams(location.search).get("id");
  const status = document.querySelector("#detail-status");
  const target = document.querySelector("#detail-content");
  const fields = JSON.parse(detail.dataset.fields || "[]");
  const load = async () => {
    if (!id) { status.textContent = "A record ID is required."; status.className = "feedback feedback-error"; return; }
    status.textContent = "Loading record..."; status.className = "feedback feedback-loading";
    try {
      const response = await fetch(endpoint + "/" + encodeURIComponent(id));
      const data = await response.json().catch(() => ({}));
      if (!response.ok) { status.textContent = response.status === 404 ? "We couldn't find that record." : "We couldn't load this record. Please try again."; status.className = "feedback feedback-error"; return; }
      const record = data.data || {};
      target.innerHTML = fields.map(f => '<div class="detail-row"><strong>' + escapeHtml(f.label) + '</strong><span>' + escapeHtml(record[f.key]) + '</span></div>').join("");
      status.textContent = "Record loaded successfully."; status.className = "feedback feedback-success";
    } catch { status.textContent = "We couldn't connect to the server. Check your connection and try again."; status.className = "feedback feedback-error"; }
  };
  load();
})();
