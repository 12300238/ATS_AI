import streamlit as st
from services import get_applications


def show_dashboard():

    st.title("🏠 Tableau de bord")

    st.write("Bienvenue sur votre espace candidat.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Score ATS", "84 %")
    col2.metric("Candidatures", "12")
    col3.metric("Entretiens", "2")

    st.divider()

    st.subheader("📋 Dernières candidatures")

    applications = get_applications()

    for app in applications:

        with st.container(border=True):

            st.write(
                f"**{app['poste']}** - {app['entreprise']}"
            )

            st.write(
                f"Statut : {app['statut']}"
            )

    st.divider()

    st.subheader("🤖 Conseils IA")

    st.success(
        "Ajoutez davantage de mots-clés techniques."
    )

    st.info(
        "Complétez votre profil LinkedIn."
    )

    st.warning(
        "Ajoutez un projet personnel récent."
    )