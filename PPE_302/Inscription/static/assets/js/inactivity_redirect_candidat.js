// Définition de la durée d'inactivité en millisecondes (par exemple, 30 minutes)
var inactivityTimeout = 10 * 60 * 1000; // 30 minutes en millisecondes

// Fonction pour effectuer la redirection vers la page de connexion
function redirectLogin() {
  window.location.href = "/Candidature/candidatLog"; // Remplacez "/login/" par l'URL réelle de votre page de connexion
}

// Fonction pour réinitialiser le minuteur d'inactivité
function resetTimer() {
  clearTimeout(timer);
  timer = setTimeout(redirectLogin, inactivityTimeout);
}

// Écouteur d'événement pour réinitialiser le minuteur lors de l'interaction de l'utilisateur
document.addEventListener("mousemove", resetTimer);
document.addEventListener("keypress", resetTimer);

// Initialiser le minuteur d'inactivité au chargement de la page
var timer = setTimeout(redirectLogin, inactivityTimeout);
