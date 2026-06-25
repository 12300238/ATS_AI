"""
Données mockées (aucun backend pour l'instant).
Quand le vrai backend arrivera, ce sont ces fonctions qu'il faudra
remplacer par des appels HTTP / requêtes base de données.
"""

# Rôles possibles d'un compte. L'ordre sert aussi aux menus déroulants.
ROLES = ["Utilisateur", "RH", "Admin"]


# ---------------------------------------------------------------------------
# Comptes (utilisés pour la connexion ET pour la page d'administration)
# ---------------------------------------------------------------------------
def comptes_initiaux():
    """
    Liste de comptes de démonstration.

    ⚠️ Mock uniquement : les mots de passe sont en clair ici pour la démo.
    Un vrai backend ne doit JAMAIS stocker un mot de passe en clair :
    il faut le hasher côté serveur (bcrypt, argon2…).

    Identifiants de test :
        user@ats.fr  / user123   -> espace candidat
        rh@ats.fr    / rh123      -> espace RH
        admin@ats.fr / admin123   -> espace administration
    """
    return [
        {"id": 1, "prenom": "Thomas", "nom": "Dupont", "email": "user@ats.fr", "mdp": "user123", "role": "Utilisateur"},
        {"id": 2, "prenom": "Sophie", "nom": "Bernard", "email": "rh@ats.fr", "mdp": "rh123", "role": "RH"},
        {"id": 3, "prenom": "Alice", "nom": "Durand", "email": "admin@ats.fr", "mdp": "admin123", "role": "Admin"},
        {"id": 4, "prenom": "Bruno", "nom": "Martin", "email": "bruno.martin@ats.fr", "mdp": "bruno123", "role": "Utilisateur"},
        {"id": 5, "prenom": "Chloé", "nom": "Petit", "email": "chloe.petit@ats.fr", "mdp": "chloe123", "role": "Utilisateur"},
        {"id": 6, "prenom": "Farid", "nom": "Moreau", "email": "farid.moreau@ats.fr", "mdp": "farid123", "role": "RH"},
    ]


# ---------------------------------------------------------------------------
# Données candidat (déjà présentes dans votre projet)
# ---------------------------------------------------------------------------
def get_user():
    return {
        "nom": "Dupont",
        "prenom": "Thomas",
        "email": "thomas@email.com",
        "telephone": "0600000000",
        "linkedin": "linkedin.com/in/thomas",
        "github": "github.com/thomas",
    }


def get_jobs():
    return [
        {"title": "Data Scientist", "company": "Airbus", "location": "Toulouse", "match": 87},
        {"title": "ML Engineer", "company": "Capgemini", "location": "Paris", "match": 82},
        {"title": "Data Analyst", "company": "Orange", "location": "Lyon", "match": 76},
    ]


def get_applications():
    return [
        {"poste": "Data Scientist", "entreprise": "Airbus", "statut": "En cours", "candidat": "Thomas Dupont"},
        {"poste": "ML Engineer", "entreprise": "Capgemini", "statut": "Entretien", "candidat": "Bruno Martin"},
        {"poste": "Data Analyst", "entreprise": "Orange", "statut": "Refusé", "candidat": "Chloé Petit"},
    ]
