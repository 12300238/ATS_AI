import streamlit as st
from services import get_jobs


def show_jobs():

    st.title("💼 Offres d'emploi")

    search = st.text_input(
        "Rechercher une offre"
    )

    jobs = get_jobs()

    for job in jobs:

        with st.container(border=True):

            st.subheader(job["title"])

            st.write(
                f"🏢 {job['company']}"
            )

            st.write(
                f"📍 {job['location']}"
            )

            st.write(
                f"🎯 Match ATS : {job['match']} %"
            )

            st.progress(job["match"])

            col1, col2 = st.columns(2)

            with col1:
                st.button(
                    "Voir",
                    key=f"view_{job['title']}"
                )

            with col2:
                st.button(
                    "Postuler",
                    key=f"apply_{job['title']}"
                )
