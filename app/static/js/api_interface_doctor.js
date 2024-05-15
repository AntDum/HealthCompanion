// Return a promise that resolves to the patient data
function fetchPatient() {
    return axios
        .get("/api/patients")
        .then(function (response) {
            return (response.data);
        });
}

// Return a promise that resolves to the vaccine data
function fetchVaccinesRef() {
    return axios
        .get("/api/vaccine/ref")
        .then(function (response) {
            return response.data;
        });
}


// Return a promise that contains the data of the vaccine ref in option (vaccines_name). 
function getOptionVaccines() {
    return fetchVaccinesRef().then(function (vaccines) {
        return vaccines.map(function (vaccine) {
            return `<option value="${vaccine.vaccines_name}">${vaccine.vaccines_name}</option>`;
        }).join("");
    });
}

// Return a promise that contains the data of the patient in option (id and name).
function getOptionPatient() {
    return fetchPatient().then(function (patients) {
        return patients.map(function (patient) {
            return `<option value="${patient.id}">${patient.name}</option>`;
        }).join("");
    });
}