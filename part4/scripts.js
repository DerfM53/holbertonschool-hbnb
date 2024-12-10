/*
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form'); // recup le login
  const emailField = document.getElementById('email'); //recup l'email
  const passwordField = document.getElementById('password'); // recup mdp

  if (form) { // Si formulaire existe
    form.addEventListener('submit', function(event) {
        let valid = true;

        if (!emailField.value) {
          emailField.setCustomValidity("Veuillez entrer votre email.");
          valid = false; //formulaire non soumis
        } else {
          emailField.setCustomValidity(""); //reset l'erreur
        }

        // validation champ mdp
        if (!passwordField.value) {
          passwordField.setCustomValidity("Veuillez entrer votre mot de passe")
          valid = false;
        } else if (passwordField.value.length < 6) {
          passwordField.setCustomValidity("Le mot de passe doit contenir au moins 6 caractères. :)");
          valid = false;
        } else {
          passwordField.setCustomValidity(""); // réinitialisation erreur
        }

         // Empêche la soumission si le formulaire n'est pas valide
         if (!valid) {
          event.preventDefault(); // empêche l'envoi du formulaire
        }
    });
  }
});
