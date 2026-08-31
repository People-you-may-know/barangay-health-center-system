function listPatients(req, res) {
  res.status(200).json({
    message: "listPatients stub"
  });
}
function showPatient(req, res) {
  const id = req.params.id;

  res.status(200).json({
    message: "showPatient stub",
    id: id
  });
}
function createPatient(req, res) {
  res.status(201).json({
    message: "createPatient stub"
  });
}
function updatePatient(req, res) {
  const id = req.params.id;

  res.status(200).json({
    message: "updatePatient stub",
    id: id
  });
}
function deletePatient(req, res) {
  const id = req.params.id;

  res.status(200).json({
    message: "deletePatient stub",
    id: id
  });
}
module.exports = {
  listPatients,
  showPatient,
  createPatient,
  updatePatient,
  deletePatient
};
