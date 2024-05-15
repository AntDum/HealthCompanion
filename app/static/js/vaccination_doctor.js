
// Récupérer la liste des patients
function UpdatePatientSelect() {
    
    getOptionPatient().then(function (patients_html) {
        const patientSelectElement = $("#patient-select");
        patientSelectElement.append("<option value=''>Sélectionnez un patient</option>")
        patientSelectElement.append(patients_html);
    });
}


function UpdateVaccineList() {

    getOptionVaccines().then(function (vaccines_html) {
        const vaccineSelectElements = $(".select-vaccines");
        for (let i = 0; i < vaccineSelectElements.length; i++) {
            const vaccineSelectElement = $(vaccineSelectElements[i]);
            vaccineSelectElement.append(new Option("Sélectionnez un vaccin", ""));
            vaccineSelectElement.append(vaccines_html);
        }
    });

}


function makeListenerFormVaccine() {
    $("#vaccine-form").on("submit", function (event) {
        event.preventDefault();

        const vaccine_date = $("#vaccine-date");
        const vaccine_name = $("#vaccine-name");
        const patient_id = $("#patient-select");

        let patient_name = $("#patient-select option:selected").text();
        let patient_id_val = patient_id.val();
        // const doctor_name = $("doctor-name").value;
        if (!vaccine_date.val() || !vaccine_name.val() || !patient_id.val()) {
            alert("Veuillez remplir tous les champs");
            return;
        }
        axios
            .post("/api/patients/vaccine", {
                vaccine_date: vaccine_date.val(),
                vaccine_name: vaccine_name.val(),
                patient_id: patient_id.val(),
                // doctor_name: doctor_name,
            })
            .then(function (response) {
                console.log("API POST VACCINE", response.data);
                vaccine_date.val("");
                vaccine_name.val("");
                patient_id.val("");
            })
            .catch(function (error) {
                console.log(error);
                alert("An error occurred. Please try again later.")
            });
        
        var modal = $("#modalReminderCenter")
        modal.modal("toggle");
        const patient_name_span = modal.find('#patient-name-modal')
        patient_name_span.text(patient_name);
        patient_name_span.attr('patient-id', patient_id_val);
        modal.find('#vaccine-name-modal').val(vaccine_name.val());

    });
}

function addVaccineReminderListener(){
    $("#vaccine-reminder-form").on("submit", function (event) {
        event.preventDefault();
        
        const modal = $("#modalReminderCenter");
        const patient_name_span = $('#patient-name-modal');
        const patient_name = patient_name_span.text();
        const patient_id = patient_name_span.attr('patient-id');
        // get form input by id
        const vaccine_reminder_date = $("#vaccine-reminder-date");
        const vaccine_name = $("#vaccine-name-modal");

        console.log({
            "vaccine_reminder_date": vaccine_reminder_date.val(),
            "vaccine_name": vaccine_name.val(),
            "patient_name": patient_name,
            "patient_id": patient_id
        })

        axios
            .post("/api/patients/vaccine_reminders", {
                // TODO (Béa) : TQT je t'en laisse un peu
                vaccine_reminder_date: vaccine_reminder_date.val(),
                vaccine_name: vaccine_name.val(),
                patient_name: patient_name,
                patient_id: patient_id,
                // doctor_name: doctor_name,
            })
            .then(function (response) {
                console.log("API POST VACCINE REMINDER", response.data);
                vaccine_reminder_date.val("");
                vaccine_name.val("");
                modal.modal("toggle");
            })
            .catch(function (error) {
                console.log(error);
                alert("An error occurred. Please try again later.")
            });
    });
}

// Récupérer les données du backend et les afficher dans le dashboard
window.onload = function () {
    UpdatePatientSelect();
    UpdateVaccineList();
    makeListenerFormVaccine();
    addVaccineReminderListener();
    var today = new Date().toISOString().split('T')[0];
    document.getElementById('vaccine-date').value = today;
};
