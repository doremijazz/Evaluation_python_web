"""Formulaires Django pour les comptes, demandes, créneaux et compétences."""

from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm, Select, Textarea, formset_factory

from services.models import Request, Skill, TimeSlot
from django import forms


class InscriptionForm(UserCreationForm):
    """Formulaire de création d'un compte utilisateur.

    Hérite de UserCreationForm, qui gère notamment les champs et la
    validation du mot de passe. Les champs supplémentaires viennent de User."""
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class SlotForm(ModelForm):
    """Formulaire de saisie des dates et heures d'un créneau."""
    class Meta:
        model = TimeSlot
        fields = ["start_time", "end_time"]

        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "step": "900"
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "end_time": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "step": "900"
                },
                format="%Y-%m-%dT%H:%M"
            ),
        }


class RequestForm(ModelForm):
    """Formulaire permettant de saisir une demande de service.

    L'utilisateur choisit une compétence et décrit son besoin.
    Les créneaux sont saisis séparément via SlotFormSet.
    """
    template_name = "services/request_form.html"

    class Meta:
        model = Request
        fields = ["skill", "description"]
        widgets = {
            "skill": Select(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"cols": 200, "rows": 5}),
        }


class SkillForm(forms.Form):
    """Formulaire de sélection d'une ou plusieurs compétences."""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Compétences"
    )

# Groupe de cinq formulaires SlotForm pour saisir plusieurs créneaux.
SlotFormSet = formset_factory(
    SlotForm,
    extra=5,
    max_num=5,
    validate_max=True
)
