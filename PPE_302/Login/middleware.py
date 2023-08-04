from django.shortcuts import redirect

class SessionExpirationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Si l'utilisateur n'est pas authentifié, pas besoin de vérifier la session
            return self.get_response(request)

        # Vérifie si la session a expiré
        if request.session.get_expiry_age() <= 0:
            # La session a expiré, redirige vers la page de connexion
            return redirect('login.html')

        return self.get_response(request)
