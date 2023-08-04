from django.shortcuts import redirect, render
from django.contrib import messages
from Inscription.models import Personne

def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Vérifier si l'utilisateur existe
        try:
            user = Personne.objects.get(email=email)
        except Personne.DoesNotExist:
            user = None

        if user is not None:
            # Sauvegarder l'e-mail et le mot de passe dans une session
            request.session['reset_email'] = email
            request.session['reset_password'] = user.password

            # Rediriger l'utilisateur vers la page de modification du mot de passe
            return redirect('recuperation:change_password')

    return render(request, 'enter_email.html')


    





def change_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if  new_password1 == new_password2:
            try:
                # Rechercher l'utilisateur par email
                user = Personne.objects.get(email=email)
            except Personne.DoesNotExist:
                user = None

            if user is not None:
                # Mettre à jour le mot de passe
                user.password = new_password1  # Remplacer user.set_password(new_password1)
                user.save()

                # Supprimer les informations de réinitialisation de la session
                del request.session['reset_email']

                # Rediriger vers une page de succès
                return redirect('login:login')

        # Si les mots de passe ne correspondent pas ou l'utilisateur n'existe pas
        else:
            messages.error(request, "Le mot de passe et la confirmation du mot de passe doivent etre identique")
        return redirect('recuperation:change_password')

    return render(request, 'change_password.html')
