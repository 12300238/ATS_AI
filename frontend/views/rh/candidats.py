import streamlit as st

from views.rh.common import STATUSES, load_candidates, load_jobs, inject_style, header


def show():
    inject_style()
    candidates = load_candidates()
    jobs = load_jobs()

    header("Gestion des candidats", "Filtrer, prioriser et suivre les candidatures recues par offre.")

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
            ["Candidature ID", "Nom", "Offre ID", "Offre postulee", "Poste", "Score", "Statut", "Date", "CV"]
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
