from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Select, SplitHiddenDateTimeWidget, Textarea

from services.models import Request, Skill


class InscriptionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class RequestForm(ModelForm):
    template_name = "services/request_form.html"

    class Meta:
        model = Request
        fields = ["skill", "time_slot", "description"]
        choices = Skill.objects.all()
        widgets = {
            "skill": Select(attrs={"class": "form-control"}, choices=choices),
            "time_slot": [SplitHiddenDateTimeWidget(attrs={"class": "form-control", "step": "11200"}),],
            "descritption": Textarea(attrs={"class": "form-control"}),
        }
        