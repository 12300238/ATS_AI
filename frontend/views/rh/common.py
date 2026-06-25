"""
Éléments partagés par toutes les pages de l'espace RH :
données mockées, style, helpers d'affichage et helper d'appel API.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:5000"

STATUSES = ["A analyser", "Entretien", "Retenu", "Refuse"]


# ---------------------------------------------------------------------------
# Données mockées (propres à l'espace RH)
# ---------------------------------------------------------------------------
def load_candidates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Candidature ID": "CAND-001", "Nom": "Amel Benali", "Offre ID": "OFF-002", "Offre postulee": "Data Analyst", "Poste": "Data Analyst", "Score": 92, "Statut": "Entretien", "Experience": "4 ans", "Localisation": "Paris", "CV": "amel_benali.pdf", "Date": "2026-06-18"},
            {"Candidature ID": "CAND-002", "Nom": "Thomas Leroy", "Offre ID": "OFF-001", "Offre postulee": "Developpeur Python", "Poste": "Developpeur Python", "Score": 86, "Statut": "A analyser", "Experience": "3 ans", "Localisation": "Lyon", "CV": "thomas_leroy.pdf", "Date": "2026-06-20"},
            {"Candidature ID": "CAND-003", "Nom": "Sarah Martin", "Offre ID": "OFF-003", "Offre postulee": "Product Owner", "Poste": "Product Owner", "Score": 78, "Statut": "A analyser", "Experience": "5 ans", "Localisation": "Nantes", "CV": "sarah_martin.pdf", "Date": "2026-06-21"},
            {"Candidature ID": "CAND-004", "Nom": "Nassim Haddad", "Offre ID": "OFF-005", "Offre postulee": "Ingenieur IA", "Poste": "Ingenieur IA", "Score": 95, "Statut": "Retenu", "Experience": "6 ans", "Localisation": "Toulouse", "CV": "nassim_haddad.pdf", "Date": "2026-06-16"},
            {"Candidature ID": "CAND-005", "Nom": "Julie Moreau", "Offre ID": "OFF-004", "Offre postulee": "UX Designer", "Poste": "UX Designer", "Score": 64, "Statut": "Refuse", "Experience": "2 ans", "Localisation": "Lille", "CV": "julie_moreau.pdf", "Date": "2026-06-19"},
        ]
    )


def load_jobs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Offre ID": "OFF-001", "Titre": "Developpeur Python", "Departement": "Tech", "Localisation": "Paris", "Contrat": "CDI", "Candidatures": 18, "Publiee": "2026-06-05", "Statut": "Ouverte"},
            {"Offre ID": "OFF-002", "Titre": "Data Analyst", "Departement": "Data", "Localisation": "Lyon", "Contrat": "CDI", "Candidatures": 12, "Publiee": "2026-06-10", "Statut": "Ouverte"},
            {"Offre ID": "OFF-003", "Titre": "Product Owner", "Departement": "Produit", "Localisation": "Nantes", "Contrat": "CDI", "Candidatures": 9, "Publiee": "2026-06-12", "Statut": "Ouverte"},
            {"Offre ID": "OFF-004", "Titre": "UX Designer", "Departement": "Design", "Localisation": "Remote", "Contrat": "Freelance", "Candidatures": 7, "Publiee": "2026-06-14", "Statut": "En pause"},
            {"Offre ID": "OFF-005", "Titre": "Ingenieur IA", "Departement": "Data", "Localisation": "Toulouse", "Contrat": "CDI", "Candidatures": 5, "Publiee": "2026-06-15", "Statut": "Ouverte"},
        ]
    )


# ---------------------------------------------------------------------------
# Appel API backend (échoue silencieusement tant qu'il n'y a pas de backend)
# ---------------------------------------------------------------------------
def api_get(path: str) -> dict[str, Any] | None:
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=2)
        response.raise_for_status()
    except requests.RequestException:
        return None
    return response.json()


# ---------------------------------------------------------------------------
# Style et helpers d'affichage
# ---------------------------------------------------------------------------
def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ats-border: #d8dee8;
            --ats-blue: #2357c6;
            --ats-green: #167a56;
            --ats-ink: #111827;
            --ats-muted: #5b6472;
            --ats-soft: #f5f7fb;
        }
        .ats-header {
            border: 1px solid var(--ats-border);
            border-radius: 8px;
            padding: 18px 20px;
            background: linear-gradient(135deg, #ffffff 0%, #f4f8ff 100%);
            margin-bottom: 18px;
        }
        .ats-header h1 {
            color: var(--ats-ink);
            font-size: 1.65rem;
            line-height: 1.2;
            margin: 0 0 6px 0;
        }
        .ats-header p { color: var(--ats-muted); margin: 0; }
        .metric-card {
            border: 1px solid var(--ats-border);
            border-radius: 8px;
            padding: 16px;
            background: #ffffff;
            min-height: 112px;
        }
        .metric-card span { color: var(--ats-blue); display: block; font-size: 0.9rem; margin-bottom: 8px; }
        .metric-card strong { color: var(--ats-ink); display: block; font-size: 1.8rem; line-height: 1.1; }
        .metric-card small { color: var(--ats-green); display: block; margin-top: 8px; }
        /* color d'origine "white" remplacée par l'encre : sinon invisible sur fond clair */
        .section-title { color: var(--ats-ink); font-size: 1.15rem; font-weight: 700; margin: 8px 0 12px 0; }
        .candidate-card {
            border: 1px solid var(--ats-border);
            border-radius: 8px;
            padding: 14px 16px;
            background: #ffffff;
            margin-bottom: 10px;
        }
        .candidate-card h3 { color: black; font-size: 1rem; margin: 0 0 4px 0; }
        .candidate-card p { color: black; margin: 0; }
        .status-pill {
            border-radius: 999px;
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 4px 10px;
            background: #eef4ff;
            color: var(--ats-blue);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str | int, helper: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{helper}</small>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="ats-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    return f'<span class="status-pill">{status}</span>'
