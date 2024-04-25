window.onload = () => {
    console.log("register.js");
    // On récupère les éléments du formulaire
    const form = document.getElementById("register_form");
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const birthdate = document.getElementById("birthdate");
    const flexRadioDefault1 = document.getElementById("flexRadioDefault1");
    const flexRadioDefault2 = document.getElementById("flexRadioDefault2");

    // On ajoute un écouteur d'événement sur la soumission du formulaire
    form.addEventListener("submit", (e) => {
        // On empêche l'envoi du formulaire
        e.preventDefault();


        // On récupère les valeurs des champs
        const usernameValue = username.value;
        const emailValue = email.value;
        const passwordValue = password.value;
        const birthdateValue = birthdate.value;
        const flexRadioDefault1Value = flexRadioDefault1.checked;

        const role = flexRadioDefault1Value ? "patient" : "doctor";

        axios
            .post("/auth/register", {
                name: usernameValue,
                email: emailValue,
                password: passwordValue,
                birthdate: birthdateValue,
                role: role,
            })
            .then((response) => {
                console.log(response.data);
                window.location = "/";
            })
            .catch((error) => {
                console.log(error);
                alert("An error occurred. Please try again later.")
            });
    });
};