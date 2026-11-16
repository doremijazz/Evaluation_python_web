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


class Skill(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def belongs(self,category):
        return self.category.lower() == category.lower()

class Request(models.Model):
    user = models.ForeignKey(User)
    skill = models.ForeignKey(Skill)
    time_slots = models.ManyToManyField('TimeSlot')
    status = models.CharField(max_length=20, choices=["En Attente", "Acceptée"], default="En Attente")

    def approve(self):
        if self.status != "En Attente":
            return False
        else:
            self.status = "Acceptée"
            self.save(update_fields=["status"])
            return True

    def __str__(self):
        return (f"Damnde {self.pk}, demandé par {self.user.username}, pour {self.skill} \n Quand ? : {self.time_slots} \n Status: {self.status}")

class Availability(models.Model):
    user = models.ForeignKey(User)
    time_slots = models.ManyToManyField('TimeSlot')
    def is_available(self, time_slot):
        return self.time_slots.filter(time_slot=time_slot).exists()
    
    def __str__(self):
        return self.time_slots