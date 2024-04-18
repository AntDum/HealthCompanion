// script_doctor.js
// Code JavaScript pour le dashboard doctor

// Récupérer la liste des patients
function fetchPatient() {
    axios
        .get("/api/patients")
        .then(function (response) {
            const patientListElement = document.getElementById("patient-list");
            response.data.forEach(function (patient) {
                const listItem = document.createElement("li");
                listItem.textContent = `Nom: ${patient.name} | Date de naissance: ${patient.birthdate} | Dernière consultation: ${patient.last_visit}`;
                patientListElement.appendChild(listItem);
            });
        })
        .catch(function (error) {
            console.log(error);
        });
}

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
function makeListenerForm() {
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

// Récupérer les données du backend et les afficher dans le dashboard
window.onload = function () {
    fetchPatient();
    fetchNotification();
    fetchAppointments();
    makeListenerForm();
};
