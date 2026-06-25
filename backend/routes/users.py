"""
«component» API Utilisateurs (cf. diagramme, package BACKEND).

Squelette uniquement : la logique réelle sera implémentée en Phase 2 de
la roadmap (CRUD complet, recherche, changement de rôle).
"""

from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("")
def list_users():
    """
    TODO (Phase 2) :
    - protéger (Admin uniquement)
    - lire les query params ?q=... pour filtrer par nom/prénom/id
      (reprendre la logique déjà écrite côté front : filtrer_comptes)
    """
    request.args.get("q")
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)"}), 501


@users_bp.post("")
def create_user():
    """TODO (Phase 2) : valider avec UserCreate, vérifier l'email, hasher le mdp."""
    request.get_json(silent=True)
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)"}), 501


@users_bp.get("/me")
def get_me():
    """TODO (Phase 2) : protéger avec @jwt_required(), renvoyer le profil courant."""
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)"}), 501


@users_bp.get("/<user_id>")
def get_user(user_id):
    """TODO (Phase 2) : récupérer un utilisateur par son id."""
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)", "id": user_id}), 501


@users_bp.patch("/<user_id>")
def update_user(user_id):
    """TODO (Phase 2) : changer le rôle / les infos (protéger Admin uniquement)."""
    request.get_json(silent=True)
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)", "id": user_id}), 501


@users_bp.delete("/<user_id>")
def delete_user(user_id):
    """TODO (Phase 2) : supprimer un compte (protéger Admin uniquement)."""
    return jsonify({"error": "Not implemented yet (Phase 2 - API Utilisateurs)", "id": user_id}), 501
