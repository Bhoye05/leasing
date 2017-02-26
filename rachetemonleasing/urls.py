from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from leasing import settings


urlpatterns = patterns('rachetemonleasing.views',
    url(r'^$', 'home'),
    url(r'^accueil$', 'home'),
    url(r'^register$','register'),
    url(r'^connexion$','connexion'),
    url(r'^deconnexion$','deconnexion'),
    url(r'^annonce$','annonce'),
    url(r'^rechercher','rechercher'),
    url(r'^contact', 'contact')
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()