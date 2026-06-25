"""
«component» Chatbot LLM (cf. diagramme, package BACKEND).

À implémenter en Phase 8, en s'appuyant sur services.rag_pipeline et sur
le LLM Provider externe (clé API dans .env, jamais en dur) :
- prompt engineering (prompt système "conseiller CV")
- RAG Engine : relit le CV du candidat via similarity_search avant de répondre
- gestion de l'historique de conversation

Signatures prévues (non implémentées) :

    def build_system_prompt() -> str: ...
    def answer(user_id: str, message: str, history: list[dict]) -> str: ...
"""
