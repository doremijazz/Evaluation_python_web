from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    # URLS pour la gestion utilisatuer
    path("connexion/", views.connexion, name="connexion"),
    path("inscription/", views.register, name="inscription"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),
    # bbbbb
    ]
