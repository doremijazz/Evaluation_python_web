# Evaluation python web



## Création du projet

1. Création du dossier dans le répertoire utilisatuer
2. Créartion de l'environement virtuel et activation
3. Installation de Django
4. création et ajout du fichier .gitignore
5. Intialisation du projet avec git
6. Création du répertoire github
7. Liaison dépot local et distant


## Source pour le calendrier Django

### Installer et afficher le calendrier

- [Documentation FullCalendar](https://fullcalendar.io/docs)
- [Mettre FullCalendar dans le HTML](https://fullcalendar.io/docs/initialize-globals)
- [Exemple de calendrier](https://fullcalendar.io/demos)

### Modifier l'affichage du calendrier

- [Afficher les semaine et les heures](https://fullcalendar.io/docs/timegrid-view)
- [Afficher le mois](https://fullcalendar.io/docs/daygrid-view)
- [Les bouton pour changer de semaine ou de mois](https://fullcalendar.io/docs/headerToolbar)
- [Mettre le calendrier en français](https://fullcalendar.io/docs/locale)
- [Choisir les heures afficher](https://fullcalendar.io/docs/slotMinTime)

### Afficher les réservation

- [Comment sont fait les evenement](https://fullcalendar.io/docs/event-object)
- [Récupérer les réservation avec du JSON](https://fullcalendar.io/docs/events-json-feed)
- [Format des date et heures](https://fullcalendar.io/docs/date-parsing)
- [Changer la couleur des evenement](https://fullcalendar.io/docs/eventColor)

### Autre tuto

- [Tuto Django avec FullCalendar](https://tutorial101.blogspot.com/2022/05/python-django-ajax-fullcalender-crud.html)
- [Documentation FullCalendar version 6](https://legacy.fullcalendar.io/v6/)

## Problèmes rencontrés

### Enregistrement des créneaux

Lors de la création des demandes et des disponibilités, les créneaux ne s'enregistraient pas correctement. Le problème provenait notamment de l'absence du champ management_form dans le template HTML et de la création incorrecte des objets Availability.

### Gestion des relations ManyToMany

Les modèles Request et Availability utilisent des relations ManyToManyField pour associer plusieurs créneaux et compétences. Il a fallu utiliser les méthodes .set() et .add() après l'enregistrement des objets, car Django n'autorise pas l'affectation directe à ces relations.

### Calcul des compatibilités

La première méthode comparait les identifiants des créneaux, alors qu'une disponibilité peut être plus longue que le créneau demandé.

La comparaison a été corrigée avec :

start_time__lte : la disponibilité commence avant ou au début de la demande.

end_time__gte : la disponibilité se termine après ou à la fin de la demande.

Des affichages de débogage avec print() ont permis de vérifier séparément les compétences, les horaires, le statut et l'utilisateur à l'origine de la demande.

### Affichage et filtrage du planning

Les premiers filtres masquaient également les disponibilités ou laissaient apparaître des événements vides. Le filtrage a donc été réalisé sur les données JSON avant leur affichage dans FullCalendar.

## Choix d'architecture et d'implementation

### Utilisation de Django

Django a été choisi pour gérer les modèles, les formulaire, l'authentification et les interactions avec la base de données.

### Utilisation de FullCalendar

La bibliothèque JavaScript FullCalendar permet de représenter les demandes et les disponibilités dans un planning hebdomadaire interactif, sans développer entièrement un composant calendrier.

### Séparation des responsabilité

models.py : définit les données et leurs relation.

views.py : récupère les données, calcule les compatibilités et prépare les événements.

urls.py : associe les adresses aux vues.

Templates HTML : définissent la structure des pages.

JavaScript : affiche le calendrier et gère les interactions.

CSS : personnalise l'apparence des pages et des événements.

### Communication entre Django et FullCalendar

Une vue dédiée, planning_events(), transmet les événements au format JSON grâce à JsonResponse. Les propriétés supplémentaires sont regroupées dans extendedProps.

### Identification visuelle des événements

Un code couleur permet de distinguer les demandes pourvues, les demandes en attente, les demandes compatibles et les disponibilités.

## Améliorations à prévoir

Filtrer le planning par catégorie de compétence : permettre aux utilisateurs de sélectionner une catégorie afin d'afficher uniquement les demandes et les disponibilités correspondant à celle-ci.



