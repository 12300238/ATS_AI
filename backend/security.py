"""
Briques de sécurité partagées (Phase 1).

- hachage / vérification des mots de passe (bcrypt)
- décorateur @role_required(...) réutilisable sur les routes protégées
- helper current_user() pour récupérer le compte connecté
- sérialisation d'un document user (sans le hash du mot de passe)
- gestion de la révocation des JWT (logout réel via une collection blocklist)
- handlers JWT renvoyant du JSON propre (401/403/expiré/révoqué)
"""

from __future__ import annotations

from functools import wraps

import bcrypt
from bson import ObjectId
from bson.errors import InvalidId
from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from extensions import get_db


# ---------------------------------------------------------------------------
# Mots de passe
# ---------------------------------------------------------------------------
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except (ValueError, TypeError):
        return False


# ---------------------------------------------------------------------------
# Sérialisation
# ---------------------------------------------------------------------------
def serialize_user(doc: dict) -> dict:
    """Représentation publique d'un compte (jamais le hash du mot de passe)."""
    return {
        "id": str(doc["_id"]),
        "prenom": doc.get("prenom"),
        "nom": doc.get("nom"),
        "email": doc.get("email"),
        "role": doc.get("role"),
        "telephone": doc.get("telephone"),
        "linkedin": doc.get("linkedin"),
        "github": doc.get("github"),
        "location": doc.get("location"),
    }


# ---------------------------------------------------------------------------
# Accès au compte connecté
# ---------------------------------------------------------------------------
def current_user() -> dict | None:
    """Document du compte courant à partir de l'identité du JWT (ou None)."""
    uid = get_jwt_identity()
    if not uid:
        return None
    try:
        oid = ObjectId(uid)
    except (InvalidId, TypeError):
        return None
    return get_db().users.find_one({"_id": oid})


# ---------------------------------------------------------------------------
# Décorateur de contrôle de rôle
# ---------------------------------------------------------------------------
def role_required(*roles: str):
    """
    Protège une route : exige un JWT valide ET un rôle parmi `roles`.

    Exemple :
        @users_bp.get("")
        @role_required("Admin")
        def list_users(): ...

        @offers_bp.post("")
        @role_required("RH", "Admin")
        def create_offer(): ...
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role = get_jwt().get("role")
            if role not in roles:
                return (
                    jsonify(
                        {
                            "error": "Accès refusé : rôle insuffisant.",
                            "role_requis": list(roles),
                            "votre_role": role,
                        }
                    ),
                    403,
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Révocation des JWT (logout réel)
# ---------------------------------------------------------------------------
def revoke_token(jti: str) -> None:
    """Ajoute l'identifiant (jti) d'un token à la blocklist."""
    get_db().token_blocklist.update_one(
        {"jti": jti}, {"$set": {"jti": jti}}, upsert=True
    )


def register_jwt_handlers(jwt) -> None:
    """Branche les loaders JWT (à appeler après jwt.init_app dans la factory)."""

    @jwt.token_in_blocklist_loader
    def _check_revoked(jwt_header, jwt_payload):  # noqa: ANN001
        jti = jwt_payload.get("jti")
        return get_db().token_blocklist.find_one({"jti": jti}) is not None

    @jwt.unauthorized_loader
    def _missing_token(reason):  # noqa: ANN001
        return jsonify({"error": "Token manquant ou invalide.", "detail": reason}), 401

    @jwt.invalid_token_loader
    def _invalid_token(reason):  # noqa: ANN001
        return jsonify({"error": "Token invalide.", "detail": reason}), 401

    @jwt.expired_token_loader
    def _expired_token(jwt_header, jwt_payload):  # noqa: ANN001
        return jsonify({"error": "Token expiré, reconnectez-vous."}), 401

    @jwt.revoked_token_loader
    def _revoked_token(jwt_header, jwt_payload):  # noqa: ANN001
        return jsonify({"error": "Token révoqué (déconnecté)."}), 401
