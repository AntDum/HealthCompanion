
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

//  https://www.w3schools.com/howto/howto_js_filter_table.asp
function filter_vaccines_ref(column_idx) {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput"); // retrieve the input from the search bar
    filter = input.value.toUpperCase();
    table = document.getElementById("table-ref");
    tr = table.getElementsByTagName("tr");
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[column_idx];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }

function filter_vaccines_ref_by(){
    input = document.getElementById("search_type").value;
    // console.log("input", input)
    switch(input) {
    case "vaccine":
        filter_vaccines_ref(0);
        break;
    case "disease":
        filter_vaccines_ref(1);
        break;
    case "mandatory":
        filter_vaccines_ref(2);
        break;
    case "free":
        filter_vaccines_ref(3);
        break;
    default:
        filter_vaccines_ref(1);
    }

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
