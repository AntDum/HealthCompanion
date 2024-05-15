
function updateTableVaccineRef() {
    fetchVaccinesRef().then(function (vaccines) {
        console.log(vaccines);
        $("#table-ref tbody").html(vaccines.map(function (vaccine, index) {

            const against_list = vaccine.against.map(function (against) {
                return `<li>${against}</li>`;
            }).join("");
            
            const mandatory = vaccine.mandatory.Belgique ? "Oui" : "Non";

            const free = vaccine.free === true ? "Oui" : "Non";

            return `<tr>
                <th scope="row">${index + 1}</td>
                <td>${vaccine.vaccines_name}</td>
                <td><ul>${against_list}</ul></td>
                <td>${mandatory}</td>
                <td>${free}</td>
            </tr>`;
        }).join(""));
    }
    )
}

function makeListenerFormVaccine() {
    // TODO (Béa) : C'est ici que tu vas mettre l'event $(#id).on("submit", function)
    $("#add-vaccine-ref-btn").on("click", function (event) {
        event.preventDefault();

        const vaccine_name = $("#vaccine-name");
        const against = $("#against");
        const mandatory = $("input[name=vaccineMandatory]:checked");
        const free = $("input[name=vaccineFree]:checked");

        console.log(vaccine_name.val(), against.val(), mandatory.val(), free.val());

        if (!vaccine_name.val() || !against.val() || !mandatory.val() || !free.val()) {
            alert("Veuillez remplir tous les champs");
            return;
        }

        axios
            .post("/api/vaccine/ref", {
                vaccine_name: vaccine_name.val(),
                against: against.val(),
                mandatory: mandatory.val() === "true" ? true : false,
                free: free.val() === "true" ? true : false,
            })
            .then(function (response) {
                console.log("API POST VACCINE REF", response.data);
                vaccine_name.val("");
                against.val("");
                updateTableVaccineRef();
            })
            .catch(function (error) {
                console.log(error);
                alert("An error occurred. Please try again later.")
            });
    });

}

// Récupérer les données du backend et les afficher dans le dashboard
window.onload = function () {
    makeListenerFormVaccine();
    updateTableVaccineRef();
};
