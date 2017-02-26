from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rachetemonleasing.forms import PersonneForm, MessageForm, \
     logingForm,VoitureForm, OptionForm, UserForm, MarqueForm, AnnonceForm
from rachetemonleasing.models import UserProfile, Voiture, Option, Marque, Annonce
from django.core.mail import EmailMessage


# Create your views here.
# Home page
def home(request):
    annonces=Annonce.objects.all()
    return render(request, 'rachetemonleasing/home.html', {'annonces': annonces})


# recherche d'annonce
def rechercher(request):
    if request.method == 'GET':
        marques = Marque.objects.all()
        return render(request, 'rachetemonleasing/recherchegeneral.html', {'marques':marques})
    else:
        return redirect('/rachetemonleasing/accueil')


def contact(request):
    if request.method == 'GET':
        request.session['messageEnvoye']=''
        messageForm = MessageForm()
        return render(request, 'rachetemonleasing/contact.html', {'messageForm': messageForm})
    else:
        form = MessageForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data["nom"]
            email = form.cleaned_data["email"]
            sujet = form.cleaned_data["sujet"]
            message = form.cleaned_data["sujet"]
            emailMessage = EmailMessage(sujet, message, to=['bhoyebarry05@gmail.com'])
            emailMessage.send()
            request.session['messageEnvoye']="Votre message a bien été envoyé!"
            form = MessageForm()
            return render(request, 'rachetemonleasing/contact.html', {'messageForm': form})

        else:
            return render(request, 'rachetemonleasing/contact.html', {'messageForm': form})


# methode de connexion
def connexion(request):
    nextpage = request.GET.get('next')
    if request.user.username:
        return render(request, 'rachetemonleasing/home.html', locals())
    if request.method == "POST":
        form = logingForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["username"]
            mot_depass = form.cleaned_data["password"]
            print(user_name)
            print(mot_depass)
            user = authenticate(username=user_name, password=mot_depass)  # Nous vérifions si les données sont correctes
            print(user)
            if user is not None:  # Si l'objet renvoyé n'est pas None
                print("======== Connexion reussi=========")
                login(request, user)  # nous connectons l'utilisateur
                # return render(request, 'rachetemonleasing/home.html', locals())
                if nextpage is not None:
                    return redirect(nextpage)
                return redirect('/rachetemonleasing/accueil')
            else:  # sinon une erreur sera affichée
                form.add_error(field="" ,error="Username ou mot de passe incorect")
                return render(request, 'rachetemonleasing/connexion.html', {'logForm': form})
        else:
            return render(request, 'rachetemonleasing/connexion.html', {'logForm': form})
    else:
        form = logingForm()
    return render(request, 'rachetemonleasing/connexion.html', {'logForm': form})


# methode de deconnexion
def deconnexion(request):
    logout(request)
    # return render(request, 'rachetemonleasing/home.html', locals())
    return redirect('/rachetemonleasing/accueil')


# méthode d'inscription
def register(request):
    if request.user.username:
        print("CONNECTE")
        print(request.user.username)
        return redirect('/rachetemonleasing/accueil')
    else:
        if request.method == 'POST':  # S'il s'agit d'une requête POST
            userForm = UserForm(request.POST)
            persForm = PersonneForm(request.POST)  # Nous reprenons les données
            if persForm.is_valid() and userForm.is_valid():

                user = User.objects.create_user(username=request.POST.get('username', None),
                                                first_name=request.POST.get('first_name', None),
                                                last_name=request.POST.get('last_name', None),
                                                email=request.POST.get('email', None),
                                                password=request.POST.get('password', None))
                user.save()

                userProfile = persForm.save(commit=False)
                userProfile.user=user
                userProfile.save()


                return redirect('/rachetemonleasing/accueil')
            else:
                context = {
                    'user_form': userForm,
                    'personne_form': persForm,

                }
                return render(request, 'rachetemonleasing/register.html', context)
        else:
            context = {
                'user_form': UserForm(),
                'personne_form': PersonneForm(),

            }
            return render(request, 'rachetemonleasing/register.html', context)


# methode de création d'annonce
@login_required(login_url='/rachetemonleasing/connexion')
def annonce(request):
    if request.method == 'GET':
        context = {
            'voitureForm': VoitureForm(),
            'optionForm': OptionForm(),
            'annonceForm': AnnonceForm()
        }
        return render(request, 'rachetemonleasing/annonce.html', context)
    else:
        voitureForm = VoitureForm(request.POST)
        optionForm = OptionForm(request.POST)
        annonceForm = AnnonceForm(request.POST)
        if  voitureForm.is_valid() and optionForm.is_valid() and annonceForm.is_valid():
            print('les formulaires sont valides')

            user=request.user
            print(user)
            proprietaire=UserProfile.objects.get(pk=user.userprofile.pk)
            print(proprietaire.tel_fixe)
            # option = Option(abs=optionForm.cleaned_data['abs'], interieur_cuir=optionForm.cleaned_data['interieur_cuir'],
            #                 gps=optionForm.cleaned_data['gps'], kit_sport=optionForm.cleaned_data['kit_sport'],
            #                 phares_xenon=optionForm.cleaned_data['phares_xenon'], climatisation=optionForm.cleaned_data['climatisation'],
            #                 jantes_aliages=optionForm.cleaned_data['jantes_aliages'])
            option = optionForm.save()
            option.save()
            voiture = voitureForm.save(commit=False)
            voiture.proprietaire=proprietaire
            voiture.option=option
            voiture.save()
            annonce = annonceForm.save(commit=False)

            annonce.photo=request.FILES.get('photo')
            annonce.vehicule=voiture
            annonce.date_annonce=datetime.today()
            annonce.save()
            # voiture = Voiture(immatriculation=voitureForm.cleaned_data['immatriculation'], type=voitureForm.cleaned_data['type'],
            #                   categorie=voitureForm.cleaned_data['categorie'], transmission=voitureForm.cleaned_data['transmission'],
            #                   carburant=voitureForm.cleaned_data['carburant'],proprietaire=proprietaire, option=option,marque=voitureForm.cleaned_data['marque'])
            # voiture.save(commit=False)
            return redirect('/rachetemonleasing/accueil')
        else:
            print('les formulaires ne sont pas valides')
            context = {
                'voitureForm': voitureForm,
                'optionForm': optionForm,
                'annonceForm': AnnonceForm
            }
            return render(request, 'rachetemonleasing/annonce.html', context)


