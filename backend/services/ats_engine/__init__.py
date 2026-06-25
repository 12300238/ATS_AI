"""
«component» ATS IA Engine (cf. diagramme, package BACKEND).

À implémenter en Phase 7, en s'appuyant sur services.rag_pipeline :
- parsing / extraction structurée du CV (compétences, expériences)
- matching offre <-> CV (recherche vectorielle)
- scoring & ranking
- filtrage automatique (seuil configurable)

Signatures prévues (non implémentées) :

    def parse_cv(pdf_bytes: bytes) -> dict: ...
    def match_offer_cv(offer_id: str, application_id: str) -> float: ...
    def rank_applications(offer_id: str) -> list[dict]: ...
    def auto_filter(offer_id: str, min_score: float = 60.0) -> list[dict]: ...
"""
