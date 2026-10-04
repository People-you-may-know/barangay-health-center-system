let me = null;
let patients = [];
let services = [];

const $ = (selector) => document.querySelector(selector);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}

async function api(url, options = {}) {
  const opts = { ...options, headers: { "Content-Type": "application/json", ...(options.headers || {}) } };
  const response = await fetch(url, opts);
  const data = await response.json().catch(() => ({ error: "Invalid server response" }));
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function toast(message, bad = false) {
  const t = $("#toast");
  t.textContent = message;
  t.className = bad ? "bad show" : "show";
  setTimeout(() => { t.className = ""; }, 2800);
}

function shell(title, button = "") {
  return `
    <div class="head">
      <div><h2>${title}</h2><p class="muted">Barangay Health Center Management System</p></div>
      ${button}
    </div>`;
}

function closeModal() {
  $("#modal").className = "hidden";
  $("#modal").innerHTML = "";
}

function modal(title, html, save) {
  const m = $("#modal");
  m.className = "modal";
  m.innerHTML = `<div class="modal-box"><h2>${title}</h2>${html}</div>`;
  m.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const submit = event.submitter;
    if (submit) submit.disabled = true;
    try {
      await save(new FormData(event.target));
      closeModal();
    } catch (error) {
      toast(error.message, true);
      if (submit) submit.disabled = false;
    }
  });
}

function formData(form) {
  const result = {};
  form.forEach((value, key) => { result[key] = value; });
  return result;
}

function statCard(label, value, icon = "📌") {
  return `<div class="card stat-card"><div class="stat-icon">${icon}</div><div class="muted">${label}</div><div class="metric">${value}</div></div>`;
}

function emptyRow(columns, message = "No records found.") {
  return `<tr><td colspan="${columns}" class="empty">${message}</td></tr>`;
}

async function dashboard() {
  const d = (await api("/api/dashboard")).data;
  const upcoming = d.upcomingAppointments || [];
  const recentPatients = d.recentPatients || [];
  const recentRecords = d.recentRecords || [];
  const serviceSummary = d.serviceSummary || [];

  const statusTotal = d.scheduledAppointments + d.completedAppointments + d.cancelledAppointments;
  const scheduledPct = statusTotal ? Math.round(d.scheduledAppointments / statusTotal * 100) : 0;
  const completedPct = statusTotal ? Math.round(d.completedAppointments / statusTotal * 100) : 0;
  const cancelledPct = statusTotal ? Math.round(d.cancelledAppointments / statusTotal * 100) : 0;

  $("#main").innerHTML = shell("Dashboard", `<button type="button" class="primary" onclick="load('patients')">+ Add / Manage Patients</button>`) + `
    <div class="cards dashboard-stats">
      ${statCard("Total Patients", d.patients, "👥")}
      ${statCard("Appointments", d.appointments, "📅")}
      ${statCard("Medical Records", d.medicalRecords, "🩺")}
      ${statCard("Active Services", d.activeServices, "💊")}
      ${statCard("Today's Scheduled", d.todayAppointments, "⏰")}
      ${statCard("System Users", d.users, "👤")}
    </div>

    <div class="dashboard-grid">
      <section class="panel">
        <div class="section-title"><h3>Upcoming Appointments</h3><button type="button" class="secondary" onclick="load('appointments')">View all</button></div>
        <table><thead><tr><th>Date</th><th>Time</th><th>Patient</th><th>Service</th><th>Status</th></tr></thead>
        <tbody>${upcoming.length ? upcoming.map(a => `
          <tr><td>${esc(a.appointmentDate)}</td><td>${esc(a.appointmentTime)}</td><td>${esc(a.patientName)}</td><td>${esc(a.service)}</td><td><span class="status">${esc(a.status)}</span></td></tr>`).join("") : emptyRow(5, "No upcoming scheduled appointments.")}</tbody></table>
      </section>

      <section class="panel">
        <div class="section-title"><h3>Appointment Overview</h3><button type="button" class="secondary" onclick="load('appointments')">Manage</button></div>
        <div class="progress-list">
          <div><span>Scheduled</span><b>${d.scheduledAppointments}</b></div>
          <div class="progress"><i style="width:${scheduledPct}%"></i></div>
          <div><span>Completed</span><b>${d.completedAppointments}</b></div>
          <div class="progress"><i style="width:${completedPct}%"></i></div>
          <div><span>Cancelled</span><b>${d.cancelledAppointments}</b></div>
          <div class="progress"><i style="width:${cancelledPct}%"></i></div>
        </div>
        <div class="mini-stats"><div><strong>${d.appointments}</strong><span>Total</span></div><div><strong>${d.todayAppointments}</strong><span>Today</span></div></div>
      </section>
    </div>

    <div class="dashboard-grid">
      <section class="panel">
        <div class="section-title"><h3>Recently Added Patients</h3><button type="button" class="secondary" onclick="load('patients')">Patients</button></div>
        <table><thead><tr><th>Name</th><th>Gender</th><th>Contact</th><th>Added</th></tr></thead>
        <tbody>${recentPatients.length ? recentPatients.map(p => `
          <tr><td>${esc(p.name)}</td><td>${esc(p.gender)}</td><td>${esc(p.contactNumber)}</td><td>${esc(p.createdAt)}</td></tr>`).join("") : emptyRow(4, "No patients yet.")}</tbody></table>
      </section>

      <section class="panel">
        <div class="section-title"><h3>Recent Medical Records</h3><button type="button" class="secondary" onclick="load('records')">Records</button></div>
        <table><thead><tr><th>Date</th><th>Patient</th><th>Diagnosis</th></tr></thead>
        <tbody>${recentRecords.length ? recentRecords.map(r => `
          <tr><td>${esc(r.recordDate)}</td><td>${esc(r.patientName)}</td><td>${esc(r.diagnosis)}</td></tr>`).join("") : emptyRow(3, "No medical records yet.")}</tbody></table>
      </section>
    </div>

    <div class="dashboard-grid">
      <section class="panel">
        <div class="section-title"><h3>Health Service Status</h3><button type="button" class="secondary" onclick="load('services')">Services</button></div>
        <div class="service-summary">
          ${serviceSummary.length ? serviceSummary.map(s => `<div class="summary-chip"><span>${esc(s.status)}</span><strong>${s.count}</strong></div>`).join("") : '<p class="muted">No services configured.</p>'}
        </div>
      </section>

      <section class="panel">
        <div class="section-title"><h3>Quick Actions</h3></div>
        <div class="quick-actions">
          <button type="button" class="primary" onclick="patientModal()">👤 New Patient</button>
          <button type="button" class="secondary" onclick="load('appointments')">📅 Appointments</button>
          <button type="button" class="secondary" onclick="load('records')">🩺 Medical Records</button>
          <button type="button" class="secondary" onclick="load('services')">💊 Health Services</button>
          ${me.role === "Administrator" ? '<button type="button" class="secondary" onclick="load('users')">⚙ User Management</button>' : ""}
        </div>
      </section>
    </div>`;
}

async function patientsPage() {
  patients = (await api("/api/patients")).data;
  const rows = patients.map(p => `
    <tr><td>${p.id}</td><td><strong>${esc(p.firstName)} ${esc(p.lastName)}</strong></td><td>${esc(p.dateOfBirth)}</td><td>${esc(p.gender)}</td><td>${esc(p.contactNumber)}</td><td>${esc(p.address)}</td>
    <td class="actions"><button type="button" class="secondary" onclick="editPatient(${p.id})">Edit</button>${me.role === "Administrator" ? `<button type="button" class="danger" onclick="delPatient(${p.id})">Delete</button>` : ""}</td></tr>`).join("");
  $("#main").innerHTML = shell("Patients", '<button type="button" class="primary" onclick="patientModal()">+ Add Patient</button>') +
    `<div class="panel"><table><thead><tr><th>ID</th><th>Name</th><th>DOB</th><th>Gender</th><th>Contact</th><th>Address</th><th>Actions</th></tr></thead><tbody>${rows || emptyRow(7, "No patients found. Add your first patient.")}</tbody></table></div>`;
}

function patientModal(patient = {}) {
  modal(patient.id ? "Edit Patient" : "Add Patient", `
    <form><div class="grid">
      <label>First name<input name="firstName" maxlength="50" required value="${esc(patient.firstName)}"></label>
      <label>Last name<input name="lastName" maxlength="50" required value="${esc(patient.lastName)}"></label>
      <label>Date of birth<input name="dateOfBirth" type="date" required value="${patient.dateOfBirth || ""}"></label>
      <label>Gender<select name="gender"><option ${patient.gender === "Male" ? "selected" : ""}>Male</option><option ${patient.gender === "Female" ? "selected" : ""}>Female</option><option ${patient.gender === "Other" ? "selected" : ""}>Other</option></select></label>
      <label>Contact number<input name="contactNumber" maxlength="11" pattern="09[0-9]{9}" required value="${esc(patient.contactNumber)}"></label>
      <label>Address<input name="address" maxlength="200" required value="${esc(patient.address)}"></label>
    </div><div class="modal-actions"><button type="button" class="light" onclick="closeModal()">Cancel</button><button type="submit" class="primary">Save</button></div></form>`,
    async form => { await api(patient.id ? `/api/patients/${patient.id}` : "/api/patients", { method: patient.id ? "PUT" : "POST", body: JSON.stringify(formData(form)) }); toast("Patient saved successfully"); await patientsPage(); }
  );
}
function editPatient(id) { patientModal(patients.find(p => p.id === id)); }
async function delPatient(id) { if (confirm("Delete this patient and related records?")) { await api(`/api/patients/${id}`, {method:"DELETE"}); toast("Patient deleted"); patientsPage(); } }

async function appointmentsPage() {
  const result = await Promise.all([api("/api/appointments"), api("/api/patients"), api("/api/services")]);
  const appointments = result[0].data; patients = result[1].data; services = result[2].data;
  const rows = appointments.map(a => `
    <tr><td>${esc(a.appointmentDate)}</td><td>${esc(a.appointmentTime)}</td><td>${esc(a.patientName)}</td><td>${esc(a.service)}</td><td><span class="status">${esc(a.status)}</span></td>
    <td class="actions"><button type="button" class="secondary" onclick='appointmentModal(${JSON.stringify(a).replace(/'/g, "&#39;")})'>Edit</button><button type="button" class="danger" onclick="delAppointment(${a.id})">Delete</button></td></tr>`).join("");
  $("#main").innerHTML = shell("Appointments", '<button type="button" class="primary" onclick="appointmentModal()">+ Add Appointment</button>') +
    `<div class="panel"><table><thead><tr><th>Date</th><th>Time</th><th>Patient</th><th>Service</th><th>Status</th><th>Actions</th></tr></thead><tbody>${rows || emptyRow(6, "No appointments found.")}</tbody></table></div>`;
}

function appointmentModal(item = {}) {
  modal(item.id ? "Edit Appointment" : "Add Appointment", `
    <form><div class="grid">
      <label>Patient<select name="patientId" required>${patients.map(p => `<option value="${p.id}" ${String(item.patientId) === String(p.id) ? "selected" : ""}>${esc(p.firstName + " " + p.lastName)}</option>`).join("")}</select></label>
      <label>Service<select name="service" required>${services.map(s => `<option ${item.service === s.name ? "selected" : ""}>${esc(s.name)}</option>`).join("")}</select></label>
      <label>Date<input name="appointmentDate" type="date" required value="${item.appointmentDate || ""}"></label>
      <label>Time<input name="appointmentTime" type="time" required value="${item.appointmentTime || ""}"></label>
      <label>Status<select name="status"><option ${item.status === "Scheduled" ? "selected" : ""}>Scheduled</option><option ${item.status === "Completed" ? "selected" : ""}>Completed</option><option ${item.status === "Cancelled" ? "selected" : ""}>Cancelled</option></select></label>
      <label class="full">Notes<textarea name="notes" maxlength="500">${esc(item.notes)}</textarea></label>
    </div><div class="modal-actions"><button type="button" class="light" onclick="closeModal()">Cancel</button><button type="submit" class="primary">Save</button></div></form>`,
    async form => { await api(item.id ? `/api/appointments/${item.id}` : "/api/appointments", {method:item.id?"PUT":"POST",body:JSON.stringify(formData(form))}); toast("Appointment saved successfully"); appointmentsPage(); }
  );
}
async function delAppointment(id) { if(confirm("Delete this appointment?")) { await api(`/api/appointments/${id}`,{method:"DELETE"}); toast("Appointment deleted"); appointmentsPage(); } }

async function recordsPage() {
  const result = await Promise.all([api("/api/medical-records"), api("/api/patients")]);
  const records = result[0].data; patients = result[1].data;
  const rows = records.map(r => `
    <tr><td>${esc(r.recordDate)}</td><td>${esc(r.patientName)}</td><td>${esc(r.diagnosis)}</td><td>${esc(r.treatment)}</td><td>${esc(r.notes || "")}</td>
    <td class="actions"><button type="button" class="secondary" onclick='recordModal(${JSON.stringify(r).replace(/'/g, "&#39;")})'>Edit</button>${me.role === "Administrator" ? `<button type="button" class="danger" onclick="delRecord(${r.id})">Delete</button>` : ""}</td></tr>`).join("");
  $("#main").innerHTML = shell("Medical Records", '<button type="button" class="primary" onclick="recordModal()">+ Add Record</button>') +
    `<div class="panel"><table><thead><tr><th>Date</th><th>Patient</th><th>Diagnosis</th><th>Treatment</th><th>Notes</th><th>Actions</th></tr></thead><tbody>${rows || emptyRow(6, "No medical records found.")}</tbody></table></div>`;
}

function recordModal(item = {}) {
  modal(item.id ? "Edit Medical Record" : "Add Medical Record", `
    <form><div class="grid">
      <label>Patient<select name="patientId" required>${patients.map(p => `<option value="${p.id}" ${String(item.patientId) === String(p.id) ? "selected" : ""}>${esc(p.firstName + " " + p.lastName)}</option>`).join("")}</select></label>
      <label>Date<input name="recordDate" type="date" required value="${item.recordDate || ""}"></label>
      <label class="full">Diagnosis<input name="diagnosis" maxlength="500" required value="${esc(item.diagnosis)}"></label>
      <label class="full">Treatment<textarea name="treatment" maxlength="500" required>${esc(item.treatment)}</textarea></label>
      <label class="full">Notes<textarea name="notes" maxlength="500">${esc(item.notes)}</textarea></label>
    </div><div class="modal-actions"><button type="button" class="light" onclick="closeModal()">Cancel</button><button type="submit" class="primary">Save</button></div></form>`,
    async form => { await api(item.id ? `/api/medical-records/${item.id}` : "/api/medical-records",{method:item.id?"PUT":"POST",body:JSON.stringify(formData(form))}); toast("Medical record saved successfully"); recordsPage(); }
  );
}
async function delRecord(id) { if(confirm("Delete this medical record?")) { await api(`/api/medical-records/${id}`,{method:"DELETE"}); toast("Medical record deleted"); recordsPage(); } }

async function servicesPage() {
  services = (await api("/api/services")).data;
  $("#main").innerHTML = shell("Health Services", me.role === "Administrator" ? '<button type="button" class="primary" onclick="serviceModal()">+ Add Service</button>' : "") +
    `<div class="service-grid">${services.length ? services.map(s => `
      <div class="card service-card"><div class="section-title"><h3>${esc(s.name)}</h3><span class="status">${esc(s.status)}</span></div><p class="muted">${esc(s.description)}</p>
      <div class="actions">${me.role === "Administrator" ? `<button type="button" class="secondary" onclick='serviceModal(${JSON.stringify(s).replace(/'/g,"&#39;")})'>Edit</button><button type="button" class="danger" onclick="delService(${s.id})">Delete</button>` : ""}</div></div>`).join("") : '<div class="panel"><p class="empty">No health services configured.</p></div>'}</div>`;
}
function serviceModal(item = {}) {
  modal(item.id ? "Edit Health Service" : "Add Health Service", `
    <form><label>Name<input name="name" maxlength="100" required value="${esc(item.name)}"></label>
    <label>Description<textarea name="description" maxlength="500" required>${esc(item.description)}</textarea></label>
    <label>Status<select name="status"><option ${item.status !== "Inactive" ? "selected" : ""}>Active</option><option ${item.status === "Inactive" ? "selected" : ""}>Inactive</option></select></label>
    <div class="modal-actions"><button type="button" class="light" onclick="closeModal()">Cancel</button><button type="submit" class="primary">Save</button></div></form>`,
    async form => { await api(item.id ? `/api/services/${item.id}` : "/api/services",{method:item.id?"PUT":"POST",body:JSON.stringify(formData(form))}); toast("Health service saved successfully"); servicesPage(); }
  );
}
async function delService(id) { if(confirm("Delete this health service?")) { await api(`/api/services/${id}`,{method:"DELETE"}); toast("Health service deleted"); servicesPage(); } }

async function usersPage() {
  const users = (await api("/api/users")).data;
  $("#main").innerHTML = shell("User Management", '<button type="button" class="primary" onclick="userModal()">+ Add User</button>') +
    `<div class="panel"><table><thead><tr><th>Username</th><th>Name</th><th>Role</th><th>Created</th><th>Actions</th></tr></thead><tbody>${users.map(u => `
      <tr><td>${esc(u.username)}</td><td>${esc(u.fullName)}</td><td><span class="status">${esc(u.role)}</span></td><td>${esc(String(u.created_at).slice(0,16))}</td>
      <td class="actions">${u.id === me.id ? "<span class='muted'>Current account</span>" : `<button type="button" class="secondary" onclick='userModal(${JSON.stringify(u).replace(/'/g,"&#39;")})'>Edit</button><button type="button" class="danger" onclick="delUser(${u.id})">Delete</button>`}</td></tr>`).join("")}</tbody></table></div>`;
}
function userModal(item = {}) {
  modal(item.id ? "Edit User" : "Create User", `
    <form><div class="grid">
      <label>Username<input name="username" minlength="3" maxlength="50" required value="${esc(item.username)}"></label>
      <label>Full name<input name="fullName" maxlength="100" required value="${esc(item.fullName)}"></label>
      <label>Password<input name="password" type="password" minlength="8" ${item.id ? "" : "required"} placeholder="${item.id ? "Leave blank to keep current password" : ""}"></label>
      <label>Role<select name="role"><option ${item.role === "Administrator" ? "selected" : ""}>Administrator</option><option ${item.role !== "Administrator" ? "selected" : ""}>Staff</option></select></label>
    </div><div class="modal-actions"><button type="button" class="light" onclick="closeModal()">Cancel</button><button type="submit" class="primary">Save</button></div></form>`,
    async form => { await api(item.id ? `/api/users/${item.id}` : "/api/users",{method:item.id?"PUT":"POST",body:JSON.stringify(formData(form))}); toast("User saved successfully"); usersPage(); }
  );
}
async function delUser(id) { if(confirm("Delete this user?")) { await api(`/api/users/${id}`,{method:"DELETE"}); toast("User deleted"); usersPage(); } }

async function load(page) {
  document.querySelectorAll("nav button").forEach(b => b.classList.toggle("active", b.dataset.page === page));
  try {
    if (page === "dashboard") await dashboard();
    if (page === "patients") await patientsPage();
    if (page === "appointments") await appointmentsPage();
    if (page === "records") await recordsPage();
    if (page === "services") await servicesPage();
    if (page === "users") await usersPage();
  } catch (error) {
    toast(error.message, true);
  }
}

document.querySelectorAll("nav button").forEach(button => {
  button.addEventListener("click", () => {
    if (button.id === "usersNav" && me?.role !== "Administrator") return;
    load(button.dataset.page);
  });
});

$("#loginForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const submit = event.submitter;
  submit.disabled = true;
  try {
    me = (await api("/api/login", {
      method: "POST",
      body: JSON.stringify({ username: $("#username").value, password: $("#password").value })
    })).data;
    $("#login").className = "hidden";
    $("#app").className = "";
    $("#who").textContent = me.fullName + " • " + me.role;
    $("#usersNav").className = me.role === "Administrator" ? "" : "hidden";
    await load("dashboard");
  } catch (error) {
    toast(error.message, true);
  } finally {
    submit.disabled = false;
  }
});

$("#logout").addEventListener("click", async (event) => {
  event.preventDefault();
  const button = $("#logout");
  if (button.disabled) return;
  button.disabled = true;
  try { await api("/api/logout", { method: "POST" }); }
  finally {
    me = null;
    $("#app").className = "hidden";
    $("#login").className = "login";
    $("#password").value = "";
    button.disabled = false;
    $("#username").focus();
  }
});

(async () => {
  try {
    me = (await api("/api/me")).data;
    $("#login").className = "hidden";
    $("#app").className = "";
    $("#who").textContent = me.fullName + " • " + me.role;
    $("#usersNav").className = me.role === "Administrator" ? "" : "hidden";
    await load("dashboard");
  } catch (_) {}
})();