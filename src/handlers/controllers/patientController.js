const patientsData = require("../../data/patientsData");

function listPatients(req, res) {
  const patients = patientsData.getPatients();

  return res.status(200).json({
    status: 200,
    data: patients
  });
}

function showPatient(req, res) {
  const patient = patientsData.getPatientById(req.params.id);

  if (!patient) {
    return res.status(404).json({
      status: 404,
      error: "Patient not found"
    });
  }

  return res.status(200).json({
    status: 200,
    data: patient
  });
}

function createPatient(req, res) {
  const patient = patientsData.savePatient(req.body);

  return res.status(201).json({
    status: 201,
    data: patient
  });
}

function updatePatient(req, res) {
  const patient = patientsData.updatePatientById(
    req.params.id,
    req.body
  );

  if (!patient) {
    return res.status(404).json({
      status: 404,
      error: "Patient not found"
    });
  }

  return res.status(200).json({
    status: 200,
    data: patient
  });
}

function deletePatient(req, res) {
  const patient = patientsData.deletePatientById(req.params.id);

  if (!patient) {
    return res.status(404).json({
      status: 404,
      error: "Patient not found"
    });
  }

  return res.status(200).json({
    status: 200,
    data: patient
  });
}

module.exports = {
  listPatients,
  showPatient,
  createPatient,
  updatePatient,
  deletePatient
};
