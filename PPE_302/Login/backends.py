from Inscription.models import Personne

class PersonneBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            user = Personne.objects.get(email=email)
            if user.password == password:
                return user
        except Personne.DoesNotExist:
            pass
        return None
    def get_user(self, user_id):
        try:
            return Personne.objects.get(pk=user_id)
        except Personne.DoesNotExist:
            return None

