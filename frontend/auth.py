"""
Authentification et gestion de session.

L'ensemble des comptes vit dans st.session_state.comptes : la page admin
les modifie (rôle, création, suppression) et la connexion s'appuie dessus.

On ne stocke PAS l'objet compte connecté directement (ce serait une référence
partagée avec la liste, source de bugs). On stocke seulement son identifiant
et on résout le compte à jour à chaque exécution.
"""

import streamlit as st

from services import comptes_initiaux


def init_auth():
    """À appeler au tout début de l'app."""
    st.session_state.setdefault("comptes", comptes_initiaux())
    st.session_state.setdefault("id_connecte", None)
    st.session_state.setdefault("erreur_login", None)


def compte_par_id(user_id):
    for compte in st.session_state.comptes:
        if compte["id"] == user_id:
            return compte
    return None


def authentifier(email, mdp):
    """Retourne le compte si les identifiants sont valides, sinon None."""
    email = email.strip().lower()
    for compte in st.session_state.comptes:
        if compte["email"].lower() == email and compte["mdp"] == mdp:
            return compte
    return None


def utilisateur_courant():
    """Compte connecté, résolu à jour depuis la liste (ou None)."""
    uid = st.session_state.get("id_connecte")
    return compte_par_id(uid) if uid is not None else None


def est_connecte():
    return utilisateur_courant() is not None


def deconnexion():
    st.session_state.id_connecte = None
    st.session_state.erreur_login = None


def page_connexion():
    """Affiche le formulaire de connexion (écran d'accueil non connecté)."""
    st.title("🔐 Connexion")
    st.caption("Connectez-vous pour accéder à votre espace.")

    _, centre, _ = st.columns([1, 2, 1])

    with centre:
        with st.form("formulaire_connexion"):
            email = st.text_input("Email", placeholder="vous@exemple.fr")
            mdp = st.text_input("Mot de passe", type="password")
            valider = st.form_submit_button("Se connecter", type="primary", use_container_width=True)

            if valider:
                compte = authentifier(email, mdp)
                if compte:
                    st.session_state.id_connecte = compte["id"]
                    st.session_state.erreur_login = None
                    st.rerun()
                else:
                    st.session_state.erreur_login = "Email ou mot de passe incorrect."

        if st.session_state.erreur_login:
            st.error(st.session_state.erreur_login)

        with st.expander("Comptes de démonstration"):
            st.markdown(
                "- **Candidat** — `user@ats.fr` / `user123`\n"
                "- **RH** — `rh@ats.fr` / `rh123`\n"
                "- **Admin** — `admin@ats.fr` / `admin123`"
            )
