def get_user():

    return {
        "nom": "Dupont",
        "prenom": "Thomas",
        "email": "thomas@email.com",
        "telephone": "0600000000",
        "linkedin": "linkedin.com/in/thomas",
        "github": "github.com/thomas"
    }


def get_jobs():

    return [
        {
            "title": "Data Scientist",
            "company": "Airbus",
            "location": "Toulouse",
            "match": 87
        },
        {
            "title": "ML Engineer",
            "company": "Capgemini",
            "location": "Paris",
            "match": 82
        },
        {
            "title": "Data Analyst",
            "company": "Orange",
            "location": "Lyon",
            "match": 76
        }
    ]


def get_applications():

    return [
        {
            "poste": "Data Scientist",
            "entreprise": "Airbus",
            "statut": "En cours"
        },
        {
            "poste": "ML Engineer",
            "entreprise": "Capgemini",
            "statut": "Entretien"
        }
    ]