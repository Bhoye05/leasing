from django import forms
from django.forms import ModelForm, TextInput, DateField, CharField, EmailInput, PasswordInput
from django.contrib.auth.hashers import check_password
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.forms import EmailField, PasswordInput, DateInput
from django.utils.translation import ugettext_lazy as _


from rachetemonleasing.models import UserProfile, Departement, Marque, Voiture, Option, Annonce


class DepartementForm(forms.ModelForm):
    nom_departement = forms.ModelChoiceField(label='Département', queryset=Departement.objects.all())
    code_departement = forms.HiddenInput()

    class Meta:
        model = Departement
        exclude = ('region', 'code_departement',)

#Formulaire de User
class UserForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput, label='Pseudo', max_length=15, required=True,)
    first_name=forms.CharField(widget=forms.TextInput, label='Prénom', max_length=30, required=True)
    last_name=forms.CharField(widget=forms.TextInput, label='Nom', max_length=15, required=True)
    email = forms.EmailField(widget=forms.EmailInput, label='Adresse mail',required=True)

    class Meta:
        model = User
        #champs de formulaire
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        widgets = {
            'password': PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

#formulaire Personne
class PersonneForm(forms.ModelForm):
    date_de_naissance = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1930, 2050)]))
    class Meta:
        model = UserProfile
        fields = ('date_de_naissance','tel_fixe', 'tel_mobile','adresse','code_postale','department','commune')


    def clean(self):
        cleaned_data = super(PersonneForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if username:
            result = UserProfile.objects.filter(username=username)
            if len(result) > 0:
                raise forms.ValidationError("Pseudo déja choisi")
        if email:
            result = UserProfile.objects.filter(email=email)
            if len(result) > 0:
                raise forms.ValidationError("Adresse email deja utilisée")

#formulaire de login
class logingForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label="Nom d'utilisateur", required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe', required=True)

    def clean(self):
        cleaned_data = super(logingForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        user = User(username=username,password=password)

        # verife que les deux champs sont valides
        if not username or not password:
            raise forms.ValidationError("Courriel ou mot de passe incorect")


# formulaire de création de voiture
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        exclude = ('nom_marque',)


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        exclude = ('nom_option',)


class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        exclude = ('proprietaire', 'option')

class AnnonceForm(forms.ModelForm):
    class Meta:
        model=Annonce
        exclude=('vehicule','date_annonce')



#formulaire d'envoit deenvoi de message
class MessageForm(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Votre nom'}),label='',required=True, min_length=4)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'Votre email'}), label='', required=True)
    sujet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Sujet du message'}),label='', required=True, min_length=4)
    message = forms.CharField(widget=forms.widgets.Textarea(attrs={'class': 'form-group', 'placeholder': 'Message'}),label='' ,required=True, min_length=10, max_length=1500)

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        nom = cleaned_data.get("nom")
        email = cleaned_data.get("email")
        sujet = cleaned_data.get("sujet")
        message=cleaned_data


