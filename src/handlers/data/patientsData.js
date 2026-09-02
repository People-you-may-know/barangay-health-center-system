
let patients = [];

function savePatient(data) {
  const patient = {
    id: patients.length + 1,
    ...data
  };

  patients.push(patient);
  return patient;
}

function getPatients() {
  return patients;
}

function getPatientById(id) {
  return patients.find(patient => patient.id === Number(id));
}

function updatePatientById(id, data) {
  const index = patients.findIndex(patient => patient.id === Number(id));

  if (index === -1) {
    return null;
  }

  patients[index] = {
    ...patients[index],
    ...data
  };

  return patients[index];
}

function deletePatientById(id) {
  const index = patients.findIndex(patient => patient.id === Number(id));

  if (index === -1) {
    return null;
  }

  const deletedPatient = patients.splice(index, 1)[0];
  return deletedPatient;
}

module.exports = {
  savePatient,
  getPatients,
  getPatientById,
  updatePatientById,
  deletePatientById
};
