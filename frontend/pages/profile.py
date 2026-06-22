import streamlit as st
from services import get_user


def show_profile():

    user = get_user()

    st.title("👤 Mon Profil")

    nom = st.text_input(
        "Nom",
        value=user["nom"]
    )

    prenom = st.text_input(
        "Prénom",
        value=user["prenom"]
    )

    email = st.text_input(
        "Email",
        value=user["email"]
    )

    telephone = st.text_input(
        "Téléphone",
        value=user["telephone"]
    )

    linkedin = st.text_input(
        "LinkedIn",
        value=user["linkedin"]
    )

    github = st.text_input(
        "GitHub",
        value=user["github"]
    )

    st.button("💾 Sauvegarder")

    st.divider()

    st.subheader("📄 CV")

    cv = st.file_uploader(
        "Importer un CV",
        type=["pdf", "docx"]
    )

    if cv:
        st.success("CV importé.")

    st.divider()

    st.subheader("🧠 Compétences détectées")

    cols = st.columns(5)

    skills = [
        "Python",
        "Flask",
        "MongoDB",
        "Docker",
        "Git"
    ]

    for i, skill in enumerate(skills):

        cols[i % 5].success(skill)

    st.divider()

    st.subheader("🎯 Score ATS")

    st.progress(84)

    st.write("84 %")