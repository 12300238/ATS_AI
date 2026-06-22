import streamlit as st

from auth import init_auth, est_connecte, page_connexion, deconnexion, utilisateur_courant

from views.dashboard import show_dashboard
from views.profile import show_profile
from views.jobs import show_jobs
from views.assistant import show_assistant
from views.rh import show_rh
from views.admin import show_admin


st.set_page_config(page_title="ATS Intelligent", page_icon="📄", layout="wide")

# CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialisation de l'authentification / session
init_auth()


# ---------------------------------------------------------------------------
# 1) Non connecté -> on affiche uniquement la page de connexion et on s'arrête
# ---------------------------------------------------------------------------
if not est_connecte():
    page_connexion()
    st.stop()


# ---------------------------------------------------------------------------
# 2) Connecté -> barre latérale commune (identité + déconnexion)
# ---------------------------------------------------------------------------
user = utilisateur_courant()

st.sidebar.title("ATS IA")
st.sidebar.write(f"👋 {user['prenom']} {user['nom']}")
st.sidebar.caption(f"Rôle : **{user['role']}**")
st.sidebar.button("🚪 Se déconnecter", on_click=deconnexion, use_container_width=True)
st.sidebar.divider()


# ---------------------------------------------------------------------------
# 3) Routage selon le rôle du compte
# ---------------------------------------------------------------------------
role = user["role"]

if role == "Admin":
    # Espace administration : gestion des comptes
    show_admin()

elif role == "RH":
    # Espace RH : suivi des candidats et candidatures
    show_rh()

else:
    # Espace candidat (rôle "Utilisateur") : navigation classique
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Mon Profil", "Offres", "Assistant IA"],
    )

    if page == "Dashboard":
        show_dashboard()
    elif page == "Mon Profil":
        show_profile()
    elif page == "Offres":
        show_jobs()
    elif page == "Assistant IA":
        show_assistant()
