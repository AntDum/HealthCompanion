
// Récupérer la liste des patients
function fetchPatient() {
    axios
        .get("/api/patients")
        .then(function (response) {
            const patientSelectElement = document.getElementById("patient-select");
            patientSelectElement.innerHTML = "";
            patientSelectElement.appendChild(new Option("Sélectionnez un patient", ""));
            response.data.forEach(function (patient) {
                const option = document.createElement("option");
                option.value = patient.id;
                option.textContent = patient.name;
                patientSelectElement.appendChild(option);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
}


function fetchVaccinesRef() {
    axios
    .get("/api/vaccine/ref")
    .then(function (response) {
        console.log(response)
        const vaccineSelectElement = document.getElementById("vaccine-name");
        vaccineSelectElement.innerHTML = "";
        vaccineSelectElement.appendChild(new Option("Sélectionnez un vaccin", ""));
        response.data.forEach(function (vaccine) {
            const option = document.createElement("option");
            option.value = vaccine.name;
            option.textContent = vaccine.name;
            vaccineSelectElement.appendChild(option);
        });
    })
}


function makeListenerFormVaccine() {
    document.getElementById("vaccine-form").addEventListener("submit", function (event) {
        console.log("VACCINE FORM SUBMIT");
        event.preventDefault();
        const vaccine_date = document.getElementById("vaccine-date");
        const vaccine_name = document.getElementById("vaccine-name");
        const patient_id = document.getElementById("patient-select");
        // const doctor_name = document.getElementById("doctor-name").value;
        if (!vaccine_date.value || !vaccine_name.value || !patient_id.value) {
            alert("Veuillez remplir tous les champs");
            return;
        }
        axios
            .post("/api/patients/vaccine", {
                vaccine_date: vaccine_date.value,
                vaccine_name: vaccine_name.value,
                patient_id: patient_id.value,
                // doctor_name: doctor_name,
            })
            .then(function (response) {
                console.log("API POST VACCINE", response.data);
                vaccine_date.value = "";
                vaccine_name.value = "";
                patient_id.value = "";
            })
            .catch(function (error) {
                console.log(error);
                alert("An error occurred. Please try again later.")
            });
    });
}

// Récupérer les données du backend et les afficher dans le dashboard
window.onload = function () {
    fetchPatient();
    fetchVaccinesRef();
    makeListenerFormVaccine();
};
