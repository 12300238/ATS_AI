"""
«component» API Offres (cf. diagramme, package BACKEND).

Squelette uniquement : la logique réelle sera implémentée en Phase 3 de
la roadmap (CRUD + filtres).
"""

from flask import Blueprint, jsonify, request

offers_bp = Blueprint("offers", __name__, url_prefix="/offers")


@offers_bp.get("")
def list_offers():
    """TODO (Phase 3) : filtres ?department=&location=&status=, pagination."""
    request.args.get("status")
    return jsonify({"error": "Not implemented yet (Phase 3 - API Offres)"}), 501


@offers_bp.post("")
def create_offer():
    """TODO (Phase 3) : protéger RH/Admin, valider avec OfferCreate."""
    request.get_json(silent=True)
    return jsonify({"error": "Not implemented yet (Phase 3 - API Offres)"}), 501


@offers_bp.get("/<offer_id>")
def get_offer(offer_id):
    """TODO (Phase 3) : récupérer une offre par son id."""
    return jsonify({"error": "Not implemented yet (Phase 3 - API Offres)", "id": offer_id}), 501


@offers_bp.patch("/<offer_id>")
def update_offer(offer_id):
    """TODO (Phase 3) : modifier une offre (protéger RH/Admin)."""
    request.get_json(silent=True)
    return jsonify({"error": "Not implemented yet (Phase 3 - API Offres)", "id": offer_id}), 501


@offers_bp.delete("/<offer_id>")
def delete_offer(offer_id):
    """TODO (Phase 3) : supprimer une offre (protéger RH/Admin)."""
    return jsonify({"error": "Not implemented yet (Phase 3 - API Offres)", "id": offer_id}), 501


@offers_bp.post("/<offer_id>/apply")
def apply_to_offer(offer_id):
    """
    TODO (Phase 4 - Gestion Candidatures) :
    - récupérer le fichier CV envoyé en multipart/form-data
    - le stocker dans GridFS (extensions.get_gridfs_bucket)
    - créer le document 'application' (offer_id, user_id, cv_file_id)
    """
    return jsonify({"error": "Not implemented yet (Phase 4 - Gestion Candidatures)", "offer_id": offer_id}), 501
