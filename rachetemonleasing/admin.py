from django.contrib import admin

# Register your models here.
from rachetemonleasing.models import UserProfile, Annonce, Departement,Region, Voiture, Option, Marque,Modele
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Annonce)
admin.site.register(Voiture)
admin.site.register(Option)
admin.site.register(Departement)
admin.site.register(Region)
admin.site.register(Marque)
admin.site.register(Modele)

# nom d'utilisateur Bhoye05'
#mot de passe: sp.......1



from rachetemonleasing.models import UserProfile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UsersProfilesInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profiles'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsersProfilesInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)