from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class PersonneManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


class Personne(AbstractBaseUser):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    age = models.IntegerField()
    fonction = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    valide = models.BooleanField(null=True, default=True)
    date_inscription = models.DateTimeField(null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    
    objects = PersonneManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'age', 'fonction']

    


    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"

    def get_short_name(self):
        return self.prenom

    def __str__(self):
        return self.email
    



class Comptable(Personne):
    # Les champs spécifiques au comptable peuvent être ajoutés ici
    pass



class Employeur(Personne):
    # Les champs spécifiques à l'employeur peuvent être ajoutés ici
    pass


class Recruteur(Personne):
    # Les champs spécifiques au recruteur peuvent être ajoutés ici
    pass
class Candidat(Personne):
    # Les champs spécifiques au recruteur peuvent être ajoutés ici
    pass
