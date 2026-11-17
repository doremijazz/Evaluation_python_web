from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    skills = models.ManyToManyField('Skill', blank=True, verbose_name="users")

    def enter_skill(self, skill):
        self.skills.add(skill)

    def enter_request(self, skill, time_slot):
        request = Request.objects.create(user=self, skill=skill, time_slot=time_slot)

        return request

    def enter_availability(self, time_slot):
        availability = Availability.objects.create(user=self)
        availability.time_slots.set(time_slot)
        return availability


class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def belongs(self, category):
        return self.category.lower() == category.lower()

    def __str__(self):
        return self.name


class Request(models.Model):
    en_attente = "En Attente"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requests")
    skill = models.ForeignKey("Skill", on_delete=models.PROTECT, related_name="requests")
    time_slots = models.ManyToManyField('TimeSlot', related_name="requests")
    status = models.CharField(max_length=20,
                              choices=[("En attente", en_attente), ("aceptée", "Acceptée")], default=en_attente)
    description = models.TextField()

    def approve(self):
        if self.status != self.en_attente:
            return False
        else:
            self.status = "Acceptée"
            self.save(update_fields=["status"])
            return True

    def __str__(self):
        output = ""
        if self.time_slots:
            for t in self.time_slots.all():
                output += ' | ' + str(t)
        else:
            "Aucun créneau"
        to_print = ("Damnde" + self.pk + ", demandé par " + self.user.username + ", pour " + self.skill + " \n"
                    + " Quand ? : " + output + " \n"
                    + " Status: " + self.status)
        return to_print


class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="availability")
    time_slots = models.ManyToManyField('TimeSlot')
    skills = models.ManyToManyField('Skill')
    def is_available(self, time_slot):
        return self.time_slots.filter(time_slot=time_slot).exists()

    def __str__(self):
        return self.time_slots


class TimeSlot(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def belongs(self, start_time, end_time):
        return self.start_time <= start_time <= end_time <= self.end_time
