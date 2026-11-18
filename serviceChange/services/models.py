from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Représente un utilisateur Django et les compétences qu’il possède."""

    # Chaque adresse e-mail doit être unique dans la base de données.
    email = models.EmailField(unique=True)

    # Un utilisateur peut posséder plusieurs compétences
    skills = models.ManyToManyField('Skill', blank=True, verbose_name="users")

    def enter_skill(self, skill):
        """Associe une compétence existante à cet utilisateur.

        Args:
        skill (Skill): Compétence à ajouter.
        """
        self.skills.add(skill)

    def enter_request(self, skill, time_slot):
        """Crée une demande pour une compétence et un créneau donnés.

        Args:
            skill (Skill): Compétence demandée.
            time_slot (TimeSlot): Créneau transmis à la création.

        Returns:
            Request: Demande créée"""

        request = Request.objects.create(user=self, skill=skill, time_slot=time_slot)

        return request

    def enter_availability(self, time_slot):
        """Crée une disponibilité pour cet utilisateur.

        Args:
            time_slot: Créneau(x) à associer à la disponibilité.

        Returns:
            Availability: Disponibilité créée."""
        availability = Availability.objects.create(user=self)
        availability.time_slots.set(time_slot)
        return availability


class Skill(models.Model):
    """Décrit une compétence et sa catégorie."""
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def belongs(self, category):
        """Vérifie l’appartenance à une catégorie, sans tenir compte de la casse.

        Args:
            category (str): Catégorie recherchée.

        Returns:
            bool: True si les catégories correspondent.
        """
        return self.category.lower() == category.lower()

    def __str__(self):
        return self.name


class Request(models.Model):
    """Représente une demande de service avec ses créneaux et son statut."""
    en_attente = "En Attente"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requests")
    skill = models.ForeignKey("Skill", on_delete=models.PROTECT, related_name="requests")
    time_slots = models.ManyToManyField('TimeSlot', related_name="requests")
    status = models.CharField(max_length=20,
                              choices=[("En attente", en_attente), ("aceptée", "Acceptée")], default=en_attente)
    description = models.TextField()

    def approve(self):
        """Accepte la demande si son statut correspond au statut initial.

        Returns:
            bool: True si la demande est enregistrée comme acceptée,
            False si elle ne pouvait pas être acceptée."""
        if self.status != self.en_attente:
            return False
        else:
            self.status = "Acceptée"
            self.save(update_fields=["status"])
            return True

    def __str__(self):
        return (
            f"Demande {self.pk}, demandée par "
            f"{self.user.username}, pour {self.skill}"
        )


class Availability(models.Model):
    """Regroupe les créneaux et compétences proposés par un utilisateur."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="availability")
    time_slots = models.ManyToManyField('TimeSlot')
    skills = models.ManyToManyField('Skill')

    def is_available(self, time_slot):
        """Recherche les créneaux couvrant entièrement le créneau demandé.

        Args:
            time_slot (TimeSlot): Créneau à vérifier.

        Returns:
            QuerySet[TimeSlot]: Créneaux correspondants (pas un booléen)."""
        return self.time_slots.filter(
            start_time__lte=time_slot.start_time,
            end_time__gte=time_slot.end_time
        )

    def __str__(self):
        return self.time_slots


class TimeSlot(models.Model):
    """Représente un créneau défini par une date-heure de début et de fin."""

    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def belongs(self, start_time, end_time):
        """Vérifie qu’un intervalle est inclus dans ce créneau.

        Args:
            start_time (datetime): Début de l’intervalle à tester.
            end_time (datetime): Fin de l’intervalle à tester.

        Returns:
            bool: True si l’intervalle est entièrement inclus."""
        return self.start_time <= start_time <= end_time <= self.end_time
