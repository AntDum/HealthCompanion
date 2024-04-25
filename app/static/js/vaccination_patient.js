

// Fonction pour récupérer et afficher les médicaments et vaccinations du patient depuis le backend
function fetchVaccines() {
    axios
        .get("/api/patients/vaccine") // Assurez-vous que cette route existe dans votre backend
        .then(function (response) {
            console.log("RESPONSE", response)
            const vaccines = response.data;
            const vaccinesElement = document.getElementById("vaccines");
            vaccinesElement.innerHTML = vaccines
                .map(
                    (vaccine) =>
                        `<li class="list-group-item">${vaccine.name} - Date : ${vaccine.date}</li>`
                        // `<li class="list-group-item">${medication.name} - Dosage : ${medication.dosage}, Posologie : ${medication.schedule}</li>`
                )
                .join("");
        })
        .catch(function (error) {
            console.error("Erreur lors de la récupération des médicaments et vaccinations:", error);
        });
}


// Chargement initial des données du dashboard patient
window.onload = function () {
    fetchVaccines();
};
