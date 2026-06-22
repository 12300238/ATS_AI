from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd
import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:5000"


st.set_page_config(
    page_title="ATS AI - Espace RH",
    page_icon="ATS",
    layout="wide",
    initial_sidebar_state="expanded",
)


STATUSES = ["A analyser", "Entretien", "Retenu", "Refuse"]


def load_candidates() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Candidature ID": "CAND-001",
                "Nom": "Amel Benali",
                "Offre ID": "OFF-002",
                "Offre postulee": "Data Analyst",
                "Poste": "Data Analyst",
                "Score": 92,
                "Statut": "Entretien",
                "Experience": "4 ans",
                "Localisation": "Paris",
                "CV": "amel_benali.pdf",
                "Date": "2026-06-18",
            },
            {
                "Candidature ID": "CAND-002",
                "Nom": "Thomas Leroy",
                "Offre ID": "OFF-001",
                "Offre postulee": "Developpeur Python",
                "Poste": "Developpeur Python",
                "Score": 86,
                "Statut": "A analyser",
                "Experience": "3 ans",
                "Localisation": "Lyon",
                "CV": "thomas_leroy.pdf",
                "Date": "2026-06-20",
            },
            {
                "Candidature ID": "CAND-003",
                "Nom": "Sarah Martin",
                "Offre ID": "OFF-003",
                "Offre postulee": "Product Owner",
                "Poste": "Product Owner",
                "Score": 78,
                "Statut": "A analyser",
                "Experience": "5 ans",
                "Localisation": "Nantes",
                "CV": "sarah_martin.pdf",
                "Date": "2026-06-21",
            },
            {
                "Candidature ID": "CAND-004",
                "Nom": "Nassim Haddad",
                "Offre ID": "OFF-005",
                "Offre postulee": "Ingenieur IA",
                "Poste": "Ingenieur IA",
                "Score": 95,
                "Statut": "Retenu",
                "Experience": "6 ans",
                "Localisation": "Toulouse",
                "CV": "nassim_haddad.pdf",
                "Date": "2026-06-16",
            },
            {
                "Candidature ID": "CAND-005",
                "Nom": "Julie Moreau",
                "Offre ID": "OFF-004",
                "Offre postulee": "UX Designer",
                "Poste": "UX Designer",
                "Score": 64,
                "Statut": "Refuse",
                "Experience": "2 ans",
                "Localisation": "Lille",
                "CV": "julie_moreau.pdf",
                "Date": "2026-06-19",
            },
        ]
    )


def load_jobs() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Offre ID": "OFF-001",
                "Titre": "Developpeur Python",
                "Departement": "Tech",
                "Localisation": "Paris",
                "Contrat": "CDI",
                "Candidatures": 18,
                "Publiee": "2026-06-05",
                "Statut": "Ouverte",
            },
            {
                "Offre ID": "OFF-002",
                "Titre": "Data Analyst",
                "Departement": "Data",
                "Localisation": "Lyon",
                "Contrat": "CDI",
                "Candidatures": 12,
                "Publiee": "2026-06-10",
                "Statut": "Ouverte",
            },
            {
                "Offre ID": "OFF-003",
                "Titre": "Product Owner",
                "Departement": "Produit",
                "Localisation": "Nantes",
                "Contrat": "CDI",
                "Candidatures": 9,
                "Publiee": "2026-06-12",
                "Statut": "Ouverte",
            },
            {
                "Offre ID": "OFF-004",
                "Titre": "UX Designer",
                "Departement": "Design",
                "Localisation": "Remote",
                "Contrat": "Freelance",
                "Candidatures": 7,
                "Publiee": "2026-06-14",
                "Statut": "En pause",
            },
            {
                "Offre ID": "OFF-005",
                "Titre": "Ingenieur IA",
                "Departement": "Data",
                "Localisation": "Toulouse",
                "Contrat": "CDI",
                "Candidatures": 5,
                "Publiee": "2026-06-15",
                "Statut": "Ouverte",
            },
        ]
    )


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

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            
        }

        [data-testid="stSidebar"] {
            background: #f7f9fc;
            border-right: 1px solid var(--ats-border);
            
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: var(--ats-ink) !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            color: var(--ats-ink) !important;
            font-weight: 600;
        }

        [data-testid="stSidebar"] [data-baseweb="radio"] div {
            color: var(--ats-ink) !important;
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
            letter-spacing: 0;
            
        }

        .ats-header p {
            color: var(--ats-muted);
            margin: 0;
        }

        .metric-card {
            border: 1px solid var(--ats-border);
            border-radius: 8px;
            padding: 16px;
            background: #ffffff;
            min-height: 112px;
        }

        .metric-card span {
            color: blue;
            display: block;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .metric-card strong {
            color: var(--ats-ink);
            display: block;
            font-size: 1.8rem;
            line-height: 1.1;
        }

        .metric-card small {
            color: var(--ats-green);
            display: block;
            margin-top: 8px;
        }

        .section-title {
            color: white;
            font-size: 1.15rem;
            font-weight: 700;
            margin: 8px 0 12px 0;
        }

        .candidate-card {
            border: 1px solid var(--ats-border);
            border-radius: 8px;
            padding: 14px 16px;
            background: #ffffff;
            margin-bottom: 10px;
        }

        .candidate-card h3 {
            color: black;
            font-size: 1rem;
            margin: 0 0 4px 0;
            letter-spacing: 0;
        }

        .candidate-card p {
            color: black;
            margin: 0;
        }

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


def api_get(path: str) -> dict[str, Any] | None:
    try:
        response = requests.get(f"{API_BASE_URL}{path}", timeout=2)
        response.raise_for_status()
    except requests.RequestException:
        return None
    return response.json()


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


def sidebar() -> str:
    st.sidebar.title("ATS AI")
    st.sidebar.caption("Espace RH")
    

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard RH",
            "Gestion des candidats",
            "Gestion des offres",
            "Analytique / Rapports",
            "Creation compte RH",
        ],
    )

    st.sidebar.divider()
    health = api_get("/")
    if health:
        st.sidebar.success("API backend connectee")
    return page


def dashboard(candidates: pd.DataFrame, jobs: pd.DataFrame) -> None:
    header(
        "Dashboard RH",
        "Vue d'ensemble des candidatures, scores IA et offres actives.",
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Candidatures", len(candidates), "+5 cette semaine")
    with col2:
        metric_card("Score moyen", f"{candidates['Score'].mean():.0f}%", "Matching IA")
    with col3:
        metric_card("Offres ouvertes", len(jobs[jobs["Statut"] == "Ouverte"]), "A pourvoir")
    with col4:
        metric_card("Entretiens", len(candidates[candidates["Statut"] == "Entretien"]), "En cours")

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="section-title">Pipeline de candidatures</div>', unsafe_allow_html=True)
        status_counts = candidates["Statut"].value_counts().reindex(STATUSES, fill_value=0)
        st.bar_chart(status_counts)

    with right:
        st.markdown('<div class="section-title">Top profils</div>', unsafe_allow_html=True)
        for _, row in candidates.sort_values("Score", ascending=False).head(3).iterrows():
            st.markdown(
                f"""
                <div class="candidate-card">
                    <h3>{row['Nom']} - {row['Score']}%</h3>
                    <p>{row['Offre postulee']} · {row['Experience']} · {status_badge(row['Statut'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Candidatures</div>', unsafe_allow_html=True)
    activity = candidates[
        ["Date", "Candidature ID", "Nom", "Offre ID", "Offre postulee", "Statut", "Score"]
    ].sort_values("Date", ascending=False)
    st.dataframe(activity, use_container_width=True, hide_index=True)


def candidates_view(candidates: pd.DataFrame, jobs: pd.DataFrame) -> None:
    header(
        "Gestion des candidats",
        "Filtrer, prioriser et suivre les candidatures recues par offre.",
    )

    job_options = ["Toutes les offres"] + [
        f"{row['Offre ID']} - {row['Titre']}" for _, row in jobs.sort_values("Titre").iterrows()
    ]

    col1, col2, col3 = st.columns([1.2, 1, 1])
    with col1:
        job_filter = st.selectbox("Offre postulee", job_options)
    with col2:
        status_filter = st.selectbox("Statut", ["Tous"] + STATUSES)
    with col3:
        min_score = st.slider("Score IA minimum", 0, 100, 60, 5)

    filtered = candidates[candidates["Score"] >= min_score]
    if job_filter != "Toutes les offres":
        selected_offer_id = job_filter.split(" - ", maxsplit=1)[0]
        filtered = filtered[filtered["Offre ID"] == selected_offer_id]
    if status_filter != "Tous":
        filtered = filtered[filtered["Statut"] == status_filter]

    st.dataframe(
        filtered[
            [
                "Candidature ID",
                "Nom",
                "Offre ID",
                "Offre postulee",
                "Poste",
                "Score",
                "Statut",
                "Date",
                "CV",
            ]
        ].sort_values("Score", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                help="Score de matching entre le CV et l'offre",
                format="%d%%",
                min_value=0,
                max_value=100,
            )
        },
    )

    st.markdown('<div class="section-title">Dossier candidat</div>', unsafe_allow_html=True)
    selected_application = st.selectbox(
        "Candidature",
        (
            [
                f"{row['Candidature ID']} - {row['Nom']} - {row['Offre postulee']}"
                for _, row in filtered.sort_values("Date", ascending=False).iterrows()
            ]
            if not filtered.empty
            else ["Aucune"]
        ),
    )
    if selected_application != "Aucune":
        selected_application_id = selected_application.split(" - ", maxsplit=1)[0]
        selected = filtered[filtered["Candidature ID"] == selected_application_id].iloc[0]
        col1, col2 = st.columns([1, 1])
        with col1:
            st.text_input("Candidature", selected["Candidature ID"])
            st.text_input("Nom", selected["Nom"])
            st.text_input("Offre postulee", f"{selected['Offre ID']} - {selected['Offre postulee']}")
            st.text_input("Poste cible", selected["Poste"])
            st.text_input("Localisation", selected["Localisation"])
            st.text_input("CV", selected["CV"])
        with col2:
            st.selectbox("Changer le statut", STATUSES, index=STATUSES.index(selected["Statut"]))
            st.text_area(
                "Note RH",
                "Profil pertinent. Verifier la disponibilite et approfondir les competences metier en entretien.",
                height=130,
            )
            st.button("Enregistrer le suivi", type="primary")


def jobs_view(jobs: pd.DataFrame) -> None:
    header(
        "Gestion des offres",
        "Creer, publier et suivre les offres auxquelles les candidats postulent.",
    )

    with st.expander("Nouvelle offre", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Titre de l'offre", placeholder="Ex: Ingenieur IA")
            st.selectbox("Departement", ["Tech", "Data", "Produit", "Design", "RH", "Finance"])
            st.text_input("Localisation", placeholder="Paris, Lyon, Remote...")
        with col2:
            st.selectbox("Type de contrat", ["CDI", "CDD", "Stage", "Alternance", "Freelance"])
            st.text_area("Description", placeholder="Missions, profil recherche, competences attendues...")
            st.button("Publier l'offre", type="primary")

    st.markdown('<div class="section-title">Offres existantes</div>', unsafe_allow_html=True)
    st.dataframe(jobs, use_container_width=True, hide_index=True)


def analytics_view(candidates: pd.DataFrame, jobs: pd.DataFrame) -> None:
    header(
        "Analytique / Rapports",
        "Mesurer le volume, la qualite du matching et la progression du recrutement.",
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Scores par offre postulee</div>', unsafe_allow_html=True)
        st.bar_chart(candidates.groupby("Offre postulee")["Score"].mean().sort_values(ascending=False))
    with col2:
        st.markdown('<div class="section-title">Candidatures par offre</div>', unsafe_allow_html=True)
        st.bar_chart(jobs.set_index("Titre")["Candidatures"].sort_values(ascending=False))

    report = {
        "Taux de profils >= 80": f"{(candidates['Score'].ge(80).mean() * 100):.0f}%",
        "Meilleur canal": "Depot CV plateforme",
        "Poste le plus demande": jobs.sort_values("Candidatures", ascending=False).iloc[0]["Titre"],
        "Delai moyen estime": "6 jours",
    }
    st.json(report)
    st.download_button(
        "Telecharger le rapport CSV",
        data=candidates.to_csv(index=False).encode("utf-8"),
        file_name="rapport_candidatures.csv",
        mime="text/csv",
    )


def rh_account_view() -> None:
    header(
        "Creation compte",
        "Ajouter un recruteur ou administrateur autorise a gerer les offres et candidatures.",
    )

    with st.form("rh-account-form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Prenom")
            last_name = st.text_input("Nom")
            email = st.text_input("Email professionnel")
        with col2:
            role = st.selectbox("Role", ["RH", "Administrateur"])
            password = st.text_input("Mot de passe", type="password")
            active = st.toggle("Compte actif", value=True)

        submitted = st.form_submit_button("Creer le compte", type="primary")

    if submitted:
        if not first_name or not last_name or not email or not password:
            st.error("Tous les champs obligatoires doivent etre renseignes.")
        else:
            st.success(f"Compte {role} prepare pour {first_name} {last_name}.")
            st.caption(f"Activation: {'oui' if active else 'non'}")


def main() -> None:
    inject_style()
    candidates = load_candidates()
    jobs = load_jobs()
    page = sidebar()

    if page == "Dashboard RH":
        dashboard(candidates, jobs)
    elif page == "Gestion des candidats":
        candidates_view(candidates, jobs)
    elif page == "Gestion des offres":
        jobs_view(jobs)
    elif page == "Analytique / Rapports":
        analytics_view(candidates, jobs)
    elif page == "Creation compte RH":
        rh_account_view()


if __name__ == "__main__":
    main()
