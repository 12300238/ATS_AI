import streamlit as st
from services import get_applications, get_jobs


def show_rh():
    st.title("🧑‍💼 Espace RH")
    st.caption("Suivi des candidats, des candidatures et des offres.")

    applications = get_applications()
    jobs = get_jobs()
    # Les candidats sont les comptes ayant le rôle "Utilisateur"
    candidats = [c for c in st.session_state.comptes if c["role"] == "Utilisateur"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Candidats", len(candidats))
    col2.metric("Candidatures", len(applications))
    col3.metric("Offres ouvertes", len(jobs))

    st.divider()

    tab_candidatures, tab_candidats, tab_offres = st.tabs(
        ["📨 Candidatures", "👥 Candidats", "💼 Offres"]
    )

    # --- Candidatures ---------------------------------------------------
    with tab_candidatures:
        st.subheader("Candidatures en cours")
        statut_couleur = {"En cours": "🟡", "Entretien": "🟢", "Refusé": "🔴"}
        for app in applications:
            with st.container(border=True):
                st.write(f"**{app['poste']}** — {app['entreprise']}")
                st.write(f"Candidat : {app.get('candidat', '—')}")
                st.write(
                    f"Statut : {statut_couleur.get(app['statut'], '⚪')} {app['statut']}"
                )

    # --- Candidats ------------------------------------------------------
    with tab_candidats:
        st.subheader("Liste des candidats")
        recherche = st.text_input("🔍 Rechercher un candidat", placeholder="Nom, prénom ou email…")
        r = recherche.strip().lower()
        for c in candidats:
            if r and r not in c["prenom"].lower() and r not in c["nom"].lower() and r not in c["email"].lower():
                continue
            with st.container(border=True):
                st.write(f"**{c['prenom']} {c['nom']}**")
                st.write(f"✉️ {c['email']}")

    # --- Offres ---------------------------------------------------------
    with tab_offres:
        st.subheader("Offres publiées")
        for job in jobs:
            with st.container(border=True):
                st.write(f"**{job['title']}** — {job['company']}")
                st.write(f"📍 {job['location']}")
