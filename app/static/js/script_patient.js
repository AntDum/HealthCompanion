// script_patient.js
// Code JavaScript pour le dashboard patient

// Fonction pour récupérer et afficher les données de santé du patient depuis le backend
function fetchHealthData() {
    axios
        .get("/api/patients/health-data") // Assurez-vous que cette route existe dans votre backend
        .then(function (response) {
            const healthData = response.data;
            const healthDataElement = document.getElementById("health-data");
            healthDataElement.innerHTML = `
                <div class="card-body">
                    <p class="card-text">Température : ${healthData.temperature} °C</p>
                    <p class="card-text">Fréquence Cardiaque : ${healthData.heartRate} bpm</p>
                    <p class="card-text">Pression Artérielle : ${healthData.bloodPressure}</p>
                    <p class="card-text">Poids : ${healthData.weight} kg</p>
                    <p class="card-text">Taille : ${healthData.height} cm</p>
                </div>
            `;
        })
        .catch(function (error) {
            console.error("Erreur lors de la récupération des données de santé:", error);
        });
}

// Fonction pour récupérer et afficher les rappels et notifications du patient depuis le backend
function fetchReminders() {
    axios
        .get("/api/patients/reminders") // Assurez-vous que cette route existe dans votre backend
        .then(function (response) {
            const reminders = response.data;
            const remindersElement = document.getElementById("reminders");
            remindersElement.innerHTML = reminders
                .map(
                    (reminder) =>
                        `<li class="list-group-item">${reminder.type}: ${reminder.message}</li>`
                )
                .join("");
        })
        .catch(function (error) {
            console.error("Erreur lors de la récupération des rappels et notifications:", error);
        });
}

// Écouteur d"événement pour soumettre le formulaire de communication avec le médecin
document.getElementById("communication-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const message = document.getElementById("message").value;
    axios
        .post("/api/doctor/message", { message: message })
        .then(function (response) {
            const doctorMessagesElement = document.getElementById("doctor-messages");
            doctorMessagesElement.innerHTML += `<p class="card-text"><strong>Vous:</strong> ${message}</p>`;
        })
        .catch(function (error) {
            console.error("Erreur lors de l'envoi du message:", error);
        });
});

// Chargement initial des données du dashboard patient
window.onload = function () {
    fetchHealthData();
    // fetchReminders();
};
