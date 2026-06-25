import streamlit as st

from views.rh.common import inject_style, header


def show():
    inject_style()
    header("Creation compte", "Créer un compte recruteur ou administrateur.")

    with st.form("rh-account-form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Prenom")
            last_name = st.text_input("Nom")
            email = st.text_input("Email")
        with col2:
            role = st.selectbox("Role", ["RH", "Administrateur"])
            password = st.text_input("Mot de passe", type="password")
            # Champ ajouté : l'original utilisait 'active' sans jamais le définir.
            active = st.checkbox("Activer le compte", value=True)

        submitted = st.form_submit_button("Creer le compte", type="primary")

    if submitted:
        if not first_name or not last_name or not email or not password:
            st.error("Tous les champs obligatoires doivent etre renseignes.")
        else:
            st.success(f"Compte {role} prepare pour {first_name} {last_name}.")
            st.caption(f"Activation: {'oui' if active else 'non'}")
