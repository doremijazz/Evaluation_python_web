# ServiceChange

## Présentation
ServiceChange est une plateform d'échange de services entre particulier

## Objectif
Permettre aux particulier de trouver des personnes prétes à les aider dans un certains nombre de services proposé sur la plateforme

## Fonctionalitées

- [x] Fonctionnalité terminée
- [ ] Fonctionnalité à venir


[x] Faire une demande d'aide

[X] Saisier ses disponibilités pour aider dans les domaines de compétences que nous avons

[x] Visionner le planning des demandes et des disponibilitées des autres utilisateur ayant un compte

[x] Visionner les informations de contact d'une personne a aider ou disponible pour aider

[x] Accepter un demande d'aide car on est disponible et compétant

[x] Filtrer le planning en créneaux pourvu, compatible, en attente

[ ] Filtrer par catégorie de compétence le  planning


## Technologies utilisées

- **Langage :** Python 3.14
- **Framework :** Django 5.2
- **Base de données :** SQLite / MySQL
- **Frontend :** HTML, CSS, JavaScript
- **Versionnement :** Git

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/doremijazz/Evaluation_python_web.git
cd Evaluation_python_web
```

### 2. Environnement virtuel

2.1. Verifier l'instalation de python
```bash
py -3.14 --version
```

2.2 Créer l'environement virtuel
```bash
py -3.14 -m venv .venv
```

2.3 Activer l'environement
```bash
.\.venv\Scripts\Activate.ps1
```

2.3 Installer django
```bash
python -m pip install Django==5.2.12
```

2.4 Verfifier l'instalation de django

```bash
python -m django --version
```
### 3. Ce placer dans le projet
```bash
cd ServicesChange
```

### 4. Appliquer les migrations

```bash
python manage.py migrate
```
### 5. Démarrer le serveur

```bash
python manage.py runserver
```

Accéder à l'application :

http://127.0.0.1:8000/services