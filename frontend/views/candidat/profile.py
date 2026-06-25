import streamlit as st
from services import get_user
from auth import utilisateur_courant


def show():
    user = get_user()

    # Pré-remplissage avec l'identité du compte connecté si disponible
    compte = utilisateur_courant()
    if compte:
        user = {**user, "nom": compte["nom"], "prenom": compte["prenom"], "email": compte["email"]}

    st.title("👤 Mon Profil")

    st.text_input("Nom", value=user["nom"])
    st.text_input("Prénom", value=user["prenom"])
    st.text_input("Email", value=user["email"])
    st.text_input("Téléphone", value=user["telephone"])
    st.text_input("LinkedIn", value=user["linkedin"])
    st.text_input("GitHub", value=user["github"])

    st.button("💾 Sauvegarder")

    st.divider()
    st.subheader("📄 CV")
    cv = st.file_uploader("Importer un CV", type=["pdf", "docx"])
    if cv:
        st.success("CV importé.")

    st.divider()
    st.subheader("🧠 Compétences détectées")
    cols = st.columns(5)
    for i, skill in enumerate(["Python", "Flask", "MongoDB", "Docker", "Git"]):
        cols[i % 5].success(skill)

    st.divider()
    st.subheader("🎯 Score ATS")
    st.progress(84)
    st.write("84 %")
