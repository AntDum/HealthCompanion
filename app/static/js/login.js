window.onload = () => {
    console.log("login.js");
    // On récupère les éléments du formulaire
    const form = document.getElementById("login_form");
    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const flexRadioDefault1 = document.getElementById("flexRadioDefault1");
    const flexRadioDefault2 = document.getElementById("flexRadioDefault2");

    // On ajoute un écouteur d'événement sur la soumission du formulaire
    form.addEventListener("submit", (e) => {
        // On empêche l'envoi du formulaire
        e.preventDefault();


        // On récupère les valeurs des champs
        const emailValue = email.value;
        const passwordValue = password.value;
        const flexRadioDefault1Value = flexRadioDefault1.checked;
        
        const role = flexRadioDefault1Value ? "patient" : "doctor";

        axios
            .post("/auth/login", {
                email: emailValue,
                password: passwordValue,
                role: role,
            })
            .then((response) => {
                console.log(response.data);
                window.location = "/";
            })
            .catch((error) => {
                console.log(error);
                if (error.response.status === 401 && error.response.data.error === 'Invalid credentials') {
                    alert('Invalid email or password. Have you registered?');
                } else {
                    alert("An error occurred. Please try again later.");
                }
            });
    });
};