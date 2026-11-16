from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    email = models.EmailField(unique=True)

    skills = models.ManyToManyField('Skill', blank=True, ralated_name="users")

    def enter_skill(self, skill):
        self.skills.add(skill)

    def enter_request(self, skill, time_slot):
        request = Request.objects.create(user=self, skill=skill, time_slot=time_slot)

        return request

    def enter_availability(self, time_slot):
        availability = Availability.objects.create(user=self)
        availability.time_slots.set(time_slot)
        return availability



