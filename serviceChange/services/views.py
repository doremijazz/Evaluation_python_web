from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm

from .forms import InscriptionForm, RequestForm, SlotForm, SlotFormSet
from .models import User, TimeSlot


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
    template_name = "services/account.html"


class ChangePasswordView(PasswordChangeView):
    template_name = "services/change_password.html"
    form_class = PasswordChangeForm
    success_url = reverse_lazy("services:account")


def do_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        slot_form = SlotFormSet(request.POST)

        if form.is_valid() and slot_form.is_valid():
            with transaction.atomic():
                request_data = form.save(commit=False)
                request_data.user = request.user
                request_data.status = "En attente"
                request_data.save()

                for slot in slot_form:
                    if slot.cleaned_data:
                        time_slot = slot.save(commit=False)
                        time_slot.save()
                        request_data.time_slots.add(time_slot)

            return redirect("services:index")

    else:
        form = RequestForm()
        slot_form = SlotFormSet()

    return render(
        request,
        "services/request_form.html",
        {
            "form": form,
            "slot_form": slot_form
        }
    )