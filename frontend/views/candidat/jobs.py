import streamlit as st
from services import get_jobs


def show():
    st.title("💼 Offres d'emploi")

    st.text_input("Rechercher une offre")

    for job in get_jobs():
        with st.container(border=True):
            st.subheader(job["title"])
            st.write(f"🏢 {job['company']}")
            st.write(f"📍 {job['location']}")
            st.write(f"🎯 Match ATS : {job['match']} %")
            st.progress(job["match"])

            col1, col2 = st.columns(2)
            col1.button("Voir", key=f"view_{job['title']}")
            col2.button("Postuler", key=f"apply_{job['title']}")
