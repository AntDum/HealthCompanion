// script_doctor.js
// Code JavaScript pour le dashboard doctor

// Récupérer les rappels et notifications pour le médecin
function fetchNotification() {
    axios
        .get("/api/doctor/notifications")
        .then(function (response) {
            const doctorRemindersElement = document.getElementById("doctor-reminders");
            response.data.forEach(function (notification) {
                const listItem = document.createElement("li");
                listItem.textContent = notification.message;
                doctorRemindersElement.appendChild(listItem);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
}

// Récupérer les rendez-vous avec les patients
function fetchAppointments() {
    axios
        .get("/api/appointments")
        .then(function (response) {
            const appointmentsElement = document.getElementById("appointments");
            response.data.forEach(function (appointment) {
                const listItem = document.createElement("li");
                listItem.textContent = `Rendez-vous avec ${appointment.patient} le ${appointment.date} à ${appointment.time}`;
                appointmentsElement.appendChild(listItem);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
}

// Écouteur d'événement pour soumettre le formulaire de communication avec le médecin
function makeListenerFormMessage() {
    document.getElementById("communication-form").addEventListener("submit", function (event) {
        event.preventDefault();
        const message = document.getElementById("message").value;
        axios
            .post("/api/doctor/message", { message: message })
            .then(function (response) {
                const patientMessagesElement = document.getElementById("patient-messages");
                const messageElement = document.createElement("p");
                messageElement.innerHTML = `<strong>Médecin:</strong> ${response.data.message}`;
                patientMessagesElement.appendChild(messageElement);
            })
            .catch(function (error) {
                console.log(error);
            });
    });
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
    fetchNotification();
    fetchVaccinesRef();
    // fetchAppointments();
    makeListenerFormMessage();
    makeListenerFormVaccine();
};
