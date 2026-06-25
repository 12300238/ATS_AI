"""
«component» API Auth (cf. diagramme, package BACKEND).

Squelette uniquement : la logique réelle (hash du mot de passe, vérification
des identifiants, émission du JWT) sera implémentée en Phase 1 de la
roadmap. Chaque route renvoie pour l'instant 501 Not Implemented.
"""

from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    """
    TODO (Phase 1) :
    - valider le payload avec models.schemas.UserCreate
    - vérifier l'unicité de l'email
    - hasher le mot de passe (bcrypt) avant stockage
    - insérer le compte dans la collection 'users'
    """
    request.get_json(silent=True)  # évite une erreur si pas de JSON envoyé
    return jsonify({"error": "Not implemented yet (Phase 1 - API Auth)"}), 501


@auth_bp.post("/login")
def login():
    """
    TODO (Phase 1) :
    - valider le payload avec models.schemas.UserLogin
    - vérifier l'email + le mot de passe (bcrypt.checkpw)
    - générer un JWT (flask_jwt_extended.create_access_token) avec
      les claims {user_id, role}
    """
    request.get_json(silent=True)
    return jsonify({"error": "Not implemented yet (Phase 1 - API Auth)"}), 501


@auth_bp.get("/me")
def me():
    """
    TODO (Phase 1) :
    - protéger avec @jwt_required()
    - renvoyer le compte courant (via get_jwt_identity())
    """
    return jsonify({"error": "Not implemented yet (Phase 1 - API Auth)"}), 501
