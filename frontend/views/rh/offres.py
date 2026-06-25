import streamlit as st

from views.rh.common import load_jobs, inject_style, header


def show():
    inject_style()
    jobs = load_jobs()

    header("Gestion des offres", "Creer, publier et suivre les offres auxquelles les candidats postulent.")

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
