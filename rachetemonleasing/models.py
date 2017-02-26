from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.template.defaultfilters import default
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
#contrainte adresse email unique
from rachetemonleasing.choices import TYPEBAIL_CHOICE

User._meta.get_field('email')._unique = True

class Region(models.Model):
    code_region = models.CharField(max_length=2)
    nom_region = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_region


class Departement(models.Model):
    code_departement = models.CharField(max_length=3)
    nom_departement = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_departement



class UserProfile(models.Model):
    # username, firs_name, last_name, email, password, is_staff, is_activate
    # is_superuser, last_loging, last_joigned
    user = models.OneToOneField(User)
    date_de_naissance = models.DateField(blank=True,null=True)
    tel_fixe = models.CharField(max_length=20)
    tel_mobile = models.CharField(max_length=20)
    adresse = models.CharField(max_length=30)
    department=models.ForeignKey(Departement, null=True, blank=True)
    code_postale = models.CharField(max_length=5)
    commune = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username + " " + self.user.last_name

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)


class Option(models.Model):
    nom_option = models.CharField(max_length=200, blank=True, null=True,default='option')
    abs = models.BooleanField(blank=True)
    interieur_cuir = models.BooleanField(blank=True)
    gps = models.BooleanField(blank=True)
    kit_sport = models.BooleanField(blank=True)
    phares_xenon = models.BooleanField(blank=True)
    climatisation = models.BooleanField(blank=True)
    jantes_aliages = models.BooleanField(blank=True)

    def __str__(self):
        return self.nom_option

class Modele(models.Model):
    nom_model=models.CharField(max_length=30)


class Marque(models.Model):
    nom_marque = models.CharField(max_length=20)
    modele = models.CharField(max_length=20)

    def __str__(self):
        return self.nom_marque

class Voiture(models.Model):
    immatriculation = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    categorie = models.CharField(max_length=15)
    transmission = models.CharField(max_length=15)
    carburant = models.CharField(max_length=15)
    proprietaire = models.ForeignKey(UserProfile)
    option = models.ForeignKey(Option)
    marque = models.ForeignKey(Marque)

    def __str__(self):
        return self.type + " " + self.immatriculation


class Annonce(models.Model):
    vehicule = models.ForeignKey(Voiture, blank=True, null=True)
    date_annonce = models.DateField(blank=True,null=True)
    type_bail = models.IntegerField(choices=TYPEBAIL_CHOICE, default=1)
    mois_restants = models.IntegerField()
    paiement_restant = models.FloatField()
    frais = models.FloatField()
    photo=models.ImageField(blank=True, null=True,upload_to='media/images/%Y/%m/%d')

    def __str__(self):
        return self.vehicule.immatriculation

