from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    # URLS pour la gestion utilisatuer
    path("connexion/", views.connexion, name="connexion"),
    path("inscription/", views.register, name="inscription"),
    path("deconnexion/", views.deconnexion, name="deconnexion"),

    # URL du profil
    path("account/<int:pk>/", views.UserView.as_view(), name="account"),

    # URL de lapage de changment de mot de passe
    path("password/", views.ChangePasswordView.as_view(), name="change_password"),

    # URL du formulaire de dmande
    path("request/", views.do_request, name="request"),

    # URL de déclaration de créneaux disponible
    path("availability/", views.is_available, name="availability"),

    #URL des vues de planning
    path("planning/", views.planning, name="planning"),
    path("planning/events/", views.planning_events, name="planning_events"),

    path("", views.IndexView.as_view(), name="index"),

    path("confirm-action/", views.confirm_action, name="confirm_action"),

    path("skill_form/", views.select_skills, name="skill_form"),

    path('skills/', views.list_skills, name='skills'),
]
