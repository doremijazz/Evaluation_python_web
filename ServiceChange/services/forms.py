from random import choice

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Select, SplitHiddenDateTimeWidget, Textarea, SplitDateTimeWidget, SplitDateTimeField, formset_factory, modelformset_factory, DateTimeInput

from services.models import Request, Skill, TimeSlot
from django import forms


class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class SlotForm(ModelForm):
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
    template_name = "services/request_form.html"

    class Meta:
        model = Request
        fields = ["skill", "description"]
        widgets = {
            "skill": Select(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"cols": 200, "rows": 5}),
        }

class WeekForm(ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["start_time"]
        widgets = {
            "start_time": forms.DateInput(
                attrs={
                    "type": "date-local",
                    "class": "form-control",
                },
                format="%Y-%m-%d"
            )
        }
SlotFormSet = formset_factory(
    SlotForm,
    extra=5,
    max_num=5,
    validate_max=True
)