const patientHandlers = require("../patientHandlers");

const listPatients = (req, res) => {
  return patientHandlers.listPatients(req, res);
};

const showPatient = (req, res) => {
  return patientHandlers.showPatient(req, res);
};

const createPatient = (req, res) => {
  return patientHandlers.createPatient(req, res);
};

const updatePatient = (req, res) => {
  return patientHandlers.updatePatient(req, res);
};

const deletePatient = (req, res) => {
  return patientHandlers.deletePatient(req, res); 
};

module.exports = {
  listPatients,
  showPatient,
  createPatient,
  updatePatient,
  deletePatient
};
