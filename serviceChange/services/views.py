from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from .forms import InscriptionForm


def connexion(request):
    erreur = None
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("polls:index")
        erreur = "Identifiants incorrects."
    return render(request, "polls/login.html", {"erreur": erreur})


def deconnexion(request):
    logout(request)
    return redirect("polls:index")


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
        "polls/register.html",
        {"form": form}
    )
