"""
«component» RAG Pipeline (cf. diagramme, package BACKEND).

Pipeline partagé par l'ATS IA Engine et le Chatbot LLM. À implémenter en
Phase 6 :
- extraction de texte depuis le PDF CV (PDF CV Upload -> Extraction Texte)
- découpage en chunks (Chunking)
- génération des embeddings (Embeddings)
- stockage des vecteurs sur MongoDB Atlas Vector Search (Stockage vecteurs)
- recherche par similarité, réutilisée par ats_engine et chatbot

Signatures prévues (non implémentées) :

    def extract_text(pdf_bytes: bytes) -> str: ...
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]: ...
    def embed_chunks(chunks: list[str]) -> list[list[float]]: ...
    def store_embeddings(source_type: str, source_id: str, chunks: list[str], vectors: list[list[float]]) -> None: ...
    def similarity_search(query: str, top_k: int = 5, source_type: str | None = None) -> list[dict]: ...
"""
