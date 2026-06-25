"""
Extensions partagées par l'application.

Le client MongoDB n'est initialisé que lorsque init_mongo(app) est appelé
depuis la factory (app.py) : ainsi l'app peut démarrer (et ses routes ne
dépendant pas de la base, comme /health, répondre) même si Atlas n'est pas
encore configuré — pratique pendant le développement du scaffold.
"""

from __future__ import annotations

import gridfs
from flask import Flask, current_app, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import PyMongoError

jwt = JWTManager()
cors = CORS()

# Client Mongo conservé au niveau du module : une seule connexion, réutilisée
# par tous les workers du process (pattern recommandé par PyMongo).
_mongo_client: MongoClient | None = None


def init_mongo(app: Flask) -> None:
    """Crée le client Mongo (connexion paresseuse, ne bloque pas le démarrage)."""
    global _mongo_client
    _mongo_client = MongoClient(app.config["MONGO_URI"], serverSelectionTimeoutMS=5000)


def get_db() -> Database:
    """Renvoie la base de données configurée (MONGO_DBNAME)."""
    if _mongo_client is None:
        raise RuntimeError("Mongo n'est pas initialisé : appelez init_mongo(app) dans la factory.")
    return _mongo_client[current_app.config["MONGO_DBNAME"]]


def get_gridfs_bucket() -> gridfs.GridFSBucket:
    """Bucket GridFS pour stocker/lire les CV PDF (« Stockage PDF CV » du diagramme)."""
    return gridfs.GridFSBucket(get_db(), bucket_name=current_app.config["GRIDFS_BUCKET_NAME"])


def ping_mongo() -> bool:
    """Utilisé par /health/db pour vérifier que Atlas répond."""
    try:
        get_db().command("ping")
        return True
    except PyMongoError:
        return False
