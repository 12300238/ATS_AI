"""
«component» Gestion Candidatures (cf. diagramme, package BACKEND).

À implémenter en Phase 4 :
- suivi des candidatures (liste, filtres par statut/score)
- changement de statut + historique
- notifications

Signatures prévues (non implémentées) :

    def create_application(user_id: str, offer_id: str, cv_file_id) -> dict: ...
    def list_applications(filters: dict) -> list[dict]: ...
    def update_status(application_id: str, new_status: str, notes_rh: str = "") -> dict: ...
    def get_history(application_id: str) -> list[dict]: ...
"""
