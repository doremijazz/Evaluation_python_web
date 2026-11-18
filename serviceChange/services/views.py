from datetime import timedelta, datetime

from django.http import JsonResponse
from django.utils import timezone
from typing import Optional

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm

from .forms import InscriptionForm, RequestForm, SlotForm, SlotFormSet, WeekForm
from .models import User, TimeSlot, Availability, Request


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

def is_available(request):
    if request.method == "POST":
        form = SlotFormSet(request.POST)
        if form.is_valid():
            data : Optional[Availability] = None
            data.user = request.user
            data.skills = request.user.skills.all()

            for solt in form:
                if solt.cleaned_data:
                    time_slot = solt.save(commit=False)
                    time_slot.save()
                    data.time_slots.add(time_slot)

        return redirect("services:index")
    else:
        form = SlotFormSet()

    return render(request, "services/availability.html", {"form": form})

def planning_test(request):
    # Date de référence
    today = timezone.localdate()

    if request.method == "POST":
        form = WeekForm(request.POST)

        if form.is_valid():
            selected_date = form.cleaned_data["start_time"]
        else:
            selected_date = today
    else:
        form = WeekForm()
        selected_date = today

    # Premier jour de la semaine : lundi
    start_week = selected_date - timedelta(
        days=selected_date.weekday()
    )

    # Dernier jour : dimanche
    end_week = start_week + timedelta(days=6)

    # Créneaux qui chevauchent la semaine
    time_slots = TimeSlot.objects.filter(
        start_time__date__lte=end_week,
        end_time__date__gte=start_week,
        requests__isnull=False
    ).distinct().prefetch_related("requests")

    # Organisation par jours
    planning = {}

    for i in range(7):
        jour = start_week + timedelta(days=i)

        planning[jour] = [
            slot
            for slot in time_slots
            if (
                    timezone.localtime(slot.start_time).date()
                    <= jour
                    <= timezone.localtime(slot.end_time).date()
            )
        ]

    return render(
        request,
        "services/planning.html",
        {
            "planning": planning,
            "form": form,
            "start_week": start_week,
            "end_week": end_week,
        }
    )

def planning(request):
    return render(request, "services/planning.html")

def planning_events(request):
    reservations = Request.objects.all()

    events = []

    for reservation in reservations:
        for slot in reservation.time_slots.all():
            events.append({
                "title": reservation.skill.name,
                "start": slot.start_time.isoformat(),
                "end": slot.end_time.isoformat(),
                "extendedProps": {"username" : reservation.user.username, "email" : reservation.user.email}
            })

    return JsonResponse(events, safe=False)