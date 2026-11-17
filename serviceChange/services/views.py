from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import generic

from .forms import InscriptionForm
from .models import User


def connexion(request):
    erreur = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("services:index")
        erreur = "Identifiants incorrects."
    return render(request, "services/login.html", {"erreur": erreur})


def deconnexion(request):
    logout(request)
    return redirect("services:index")


def register(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = InscriptionForm()

    return render(
        request,
        "services/register.html",
        {"form": form}
    )

class UserView(generic.DetailView):
    model = User
    template_name = "polls/account.html"
