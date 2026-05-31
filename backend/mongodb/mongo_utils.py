from pymongo import MongoClient
from pymongo.database import Database
from pymongo.results import InsertOneResult
from class_utils import user

def connexion_user() -> Database :
    """Retourne l'instance du client mongo DB pour accéder a la base user"""
    return MongoClient("mongodb://localhost:27017/")["user"]

def add_user(utilisateur: user, instance:Database):
    """ajoute un user a la base mongodb"""
    print("la")
    res = instance["comptes"].insert_one({"name": utilisateur.name, "mdp": utilisateur.mdp, "cv_path": utilisateur.cv_path, "rh": utilisateur.rh})
    print("fait")
    return res

def del_user(name:str, instance:Database):
    """suprime un utilisateur a la base mongodb"""

me = user("m", "m", "m")
print(type(add_user(me, connexion_user())))