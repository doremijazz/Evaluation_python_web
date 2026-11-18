import json
from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.http import JsonResponse
from django.utils import timezone
from typing import Optional

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import InscriptionForm, RequestForm, SlotForm, SlotFormSet, WeekForm, SkillForm
from .models import User, TimeSlot, Availability, Request, Skill


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
            return redirect("connexion")
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

        print("Formulaire réservation valide :", form.is_valid())
        print("Erreurs réservation :", form.errors)

        print("Formulaire créneaux valide :", slot_form.is_valid())
        print("Erreurs créneaux :", slot_form.errors)
        print("Erreurs générales :", slot_form.non_form_errors())

        if form.is_valid() and slot_form.is_valid():
            with transaction.atomic():
                request_data = form.save(commit=False)
                request_data.user = request.user
                request_data.status = "En attente"
                request_data.save()

                print("Réservation créée :", request_data.pk)

                for slot in slot_form:
                    if slot.cleaned_data and not slot.cleaned_data.get("DELETE", False):
                        time_slot = slot.save(commit=False)
                        time_slot.save()
                        request_data.time_slots.add(time_slot)

                        print(
                            "Créneau créé :",
                            time_slot.start_time,
                            time_slot.end_time
                        )

                print(
                    "Nombre de créneaux associés :",
                    request_data.time_slots.count()
                )

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
            data = Availability.objects.create(
                user=request.user
            )
            data.save()
            data.skills.set(request.user.skills.all())

            for solt in form:
                if solt.cleaned_data:
                    time_slot = solt.save(commit=False)
                    time_slot.save()
                    data.time_slots.add(time_slot)

            return redirect("services:index")
    else:
        form = SlotFormSet()

    return render(request, "services/availability.html", {"form": form})

def planning(request):
    return render(request, "services/planning.html")


from django.http import JsonResponse

def planning_events(request):
    reservations = Request.objects.all()
    availabilitys = Availability.objects.all()

    events = []

    for reservation in reservations:
        for slot in reservation.time_slots.all():

            matching = False

            if request.user.is_authenticated:

                autre_utilisateur = reservation.user_id != request.user.id

                competence = request.user.skills.filter(
                    pk=reservation.skill_id
                ).exists()

                disponibilite = Availability.objects.filter(
                    user=request.user,
                    time_slots__start_time__lte=slot.start_time,
                    time_slots__end_time__gte=slot.end_time
                ).exists()

                en_attente = reservation.status == "En attente"

                matching = (
                        autre_utilisateur
                        and competence
                        and disponibilite
                        and en_attente
                )

                print(
                    f"\nDemande {reservation.pk} : {reservation.skill.name}",
                    f"\nAutre utilisateur : {autre_utilisateur}",
                    f"\nCompétence possédée : {competence}",
                    f"\nDisponibilité horaire : {disponibilite}",
                    f"\nEn attente : {en_attente}",
                    f"\nMATCHING : {matching}\n"
                )

            else:
                matching = False

            if reservation.status != "En attente":
                color = "#FF0000"  # Rouge : demande traitée
                text_color = "white"

            elif matching:
                color = "#87E990"  # Vert : demande compatible
                text_color = "black"

            else:
                color = "#FD3F92"  # Rose : autre demande
                text_color = "white"

            events.append({
                "title": reservation.skill.name,
                "start": slot.start_time.isoformat(),
                "end": slot.end_time.isoformat(),
                "backgroundColor": color,
                "borderColor": color,
                "textColor": text_color,
                "extendedProps": {
                    "matching": matching,
                    "type": "request",
                    "username": reservation.user.username,
                    "email": reservation.user.email,
                    "status": reservation.status,
                    "reservationId": reservation.pk,
                    "slotId": slot.pk,
                    "description": reservation.description,
                },
            })

    for availability in availabilitys:
        for slot in availability.time_slots.all():
            autre_utilisateur = availability.user_id != request.user.id
            if autre_utilisateur:
                events.append({
                    "title": availability.user.username,
                    "start": slot.start_time.isoformat(),
                    "end": slot.end_time.isoformat(),
                    "backgroundColor": "#25FDE9",
                    "borderColor": "#25FDE9",
                    "textColor": "black",
                    "extendedProps": {
                        "type": "availability",
                        "username": availability.user.username,
                        "email": availability.user.email,
                        "skills": list(
                            availability.skills.values_list(
                                "name", flat=True
                            )
                        ),
                    },
                })

    return JsonResponse(events, safe=False)


class IndexView(generic.ListView):
    model = Request
    template_name = "services/index.html"
    context_object_name = "reservations"

@login_required
@require_POST
def confirm_action(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"success": False, "error": "Données invalides"},
            status=400
        )

    reservation = get_object_or_404(
        Request,
        pk=data.get("reservation_id")
    )

    # À adapter à tes règles d'autorisation :
    # seuls les utilisateurs habilités peuvent confirmer.
    if not request.user.is_staff:
        return JsonResponse(
            {"success": False, "error": "Accès refusé"},
            status=403
        )

    reservation.status = "confirmed"
    reservation.save(update_fields=["status"])

    return JsonResponse({"success": True})

@login_required
def select_skills(request):
    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
            skills = form.cleaned_data["skills"]

            for skill in skills:
                request.user.skills.add(skill)

            return redirect("services:index")

    else:
        form = SkillForm()

    return render(
        request,
        "services/skill_form.html",
        {"form": form}
    )

def list_skills(request):
    skills = Skill.objects.all().order_by("category", "name")

    return render(request, "services/skills.html", {
        "skills": skills
    })