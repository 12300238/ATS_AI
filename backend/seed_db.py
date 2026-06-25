"""
Charge les données mockées (mock_data/) dans MongoDB Atlas :
- comptes (mots de passe hashés avant insertion)
- offres
- candidatures, avec upload des CV PDF fournis dans GridFS

Prérequis : avoir configuré .env (MONGO_URI au minimum) — voir .env.example
et le README.

Usage :
    python seed_db.py            # insère les données (ignore si déjà présentes)
    python seed_db.py --reset    # vide d'abord les collections concernées
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import bcrypt
import gridfs
from pymongo import MongoClient

from config import Config

BASE_DIR = Path(__file__).parent
MOCK_DIR = BASE_DIR / "mock_data"


def load_json(filename: str) -> list[dict]:
    with open(MOCK_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def seed_users(db, reset: bool) -> dict[str, object]:
    if reset:
        db.users.delete_many({})

    mock_id_to_real_id = {}
    for raw in load_json("users.json"):
        mock_id = raw.pop("_mock_id")
        raw.pop("_source_note", None)

        existing = db.users.find_one({"email": raw["email"]})
        if existing:
            mock_id_to_real_id[mock_id] = existing["_id"]
            continue

        doc = {
            **raw,
            "mdp_hash": hash_password(raw.pop("mdp")),
            "date_creation": datetime.now(timezone.utc),
        }
        result = db.users.insert_one(doc)
        mock_id_to_real_id[mock_id] = result.inserted_id

    print(f"  users : {len(mock_id_to_real_id)} comptes prêts.")
    return mock_id_to_real_id


def seed_offers(db, reset: bool) -> dict[str, object]:
    if reset:
        db.offers.delete_many({})

    mock_id_to_real_id = {}
    for raw in load_json("offers.json"):
        mock_id = raw.pop("_mock_id")
        raw.pop("_source_note", None)

        existing = db.offers.find_one({"title": raw["title"], "company": raw["company"]})
        if existing:
            mock_id_to_real_id[mock_id] = existing["_id"]
            continue

        doc = {**raw, "created_by": None, "date_creation": datetime.now(timezone.utc)}
        result = db.offers.insert_one(doc)
        mock_id_to_real_id[mock_id] = result.inserted_id

    print(f"  offers : {len(mock_id_to_real_id)} offres prêtes.")
    return mock_id_to_real_id


def seed_applications(
    db,
    bucket: gridfs.GridFSBucket,
    users_map: dict[str, object],
    offers_map: dict[str, object],
    reset: bool,
) -> None:
    if reset:
        db.applications.delete_many({})

    count = 0
    for raw in load_json("applications.json"):
        raw.pop("_mock_id", None)
        raw.pop("_source_note", None)

        user_id = users_map[raw.pop("user_mock_id")]
        offer_id = offers_map[raw.pop("offer_mock_id")]

        if db.applications.find_one({"user_id": user_id, "offer_id": offer_id}):
            continue  # déjà candidaté, on ne duplique pas

        cv_path = MOCK_DIR / "cvs" / raw.pop("cv_filename")
        with open(cv_path, "rb") as f:
            cv_file_id = bucket.upload_from_stream(cv_path.name, f, metadata={"content_type": "application/pdf"})

        doc = {
            "user_id": user_id,
            "offer_id": offer_id,
            "cv_file_id": cv_file_id,
            # ⚠️ Placeholder : le vrai score viendra de l'ATS IA Engine (Phase 7).
            "score": raw.pop("ats_score_placeholder", None),
            "status": raw.pop("status", "A analyser"),
            "notes_rh": raw.pop("notes_rh", ""),
            "historique": [],
            "date_creation": datetime.now(timezone.utc),
        }
        db.applications.insert_one(doc)
        count += 1

    print(f"  applications : {count} candidature(s) insérée(s) (CV uploadés dans GridFS).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed la base avec les données mockées.")
    parser.add_argument("--reset", action="store_true", help="Vide les collections avant de les remplir.")
    args = parser.parse_args()

    client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[Config.MONGO_DBNAME]
    bucket = gridfs.GridFSBucket(db, bucket_name=Config.GRIDFS_BUCKET_NAME)

    # Vérifie la connexion tout de suite (message clair plutôt qu'une stacktrace)
    try:
        db.command("ping")
    except Exception as exc:  # noqa: BLE001 - message volontairement large pour l'utilisateur
        raise SystemExit(
            "Impossible de joindre MongoDB Atlas. Vérifiez MONGO_URI dans votre .env.\n"
            f"Erreur : {exc}"
        )

    print(f"Connexion OK -> base '{Config.MONGO_DBNAME}'. Insertion des données mockées…")
    users_map = seed_users(db, args.reset)
    offers_map = seed_offers(db, args.reset)
    seed_applications(db, bucket, users_map, offers_map, args.reset)
    print("Terminé.")


if __name__ == "__main__":
    main()
