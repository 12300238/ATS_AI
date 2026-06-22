import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# creation de la base de données
user = myclient["user"]

# creation des collections
comptes = user["comptes"] #les comptes

offres = user["offres"] #les offres

postulation = user["postulation"] #les postualtion au offres