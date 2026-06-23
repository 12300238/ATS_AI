import streamlit as st

from auth import init_auth, est_connecte, page_connexion, deconnexion, utilisateur_courant

# Espace candidat
from views.candidat import dashboard as cand_dashboard
from views.candidat import profile as cand_profile
from views.candidat import jobs as cand_jobs
from views.candidat import assistant as cand_assistant

# Espace RH
from views.rh import dashboard as rh_dashboard
from views.rh import candidats as rh_candidats
from views.rh import offres as rh_offres
from views.rh import analytique as rh_analytique
from views.rh import compte as rh_compte
from views.rh.common import api_get

# Espace admin
from views.admin import comptes as admin_comptes


st.set_page_config(page_title="ATS Intelligent", page_icon="📄", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

init_auth()


# ---------------------------------------------------------------------------
# 1) Non connecté -> page de connexion uniquement
# ---------------------------------------------------------------------------
if not est_connecte():
    page_connexion()
    st.stop()


# ---------------------------------------------------------------------------
# 2) Navigation par rôle : un dictionnaire {libellé: fonction d'affichage}
#    par espace. Facile à étendre : ajouter une page = une ligne ici.
# ---------------------------------------------------------------------------
ESPACES = {
    "Utilisateur": {
        "🏠 Tableau de bord": cand_dashboard.show,
        "👤 Mon Profil": cand_profile.show,
        "💼 Offres": cand_jobs.show,
        "🤖 Assistant IA": cand_assistant.show,
    },
    "RH": {
        "📊 Dashboard RH": rh_dashboard.show,
        "👥 Gestion des candidats": rh_candidats.show,
        "📁 Gestion des offres": rh_offres.show,
        "📈 Analytique / Rapports": rh_analytique.show,
        "➕ Création de compte": rh_compte.show,
    },
    "Admin": {
        "🛠️ Gestion des comptes": admin_comptes.show,
    },
}


# ---------------------------------------------------------------------------
# 3) Barre latérale commune (identité + déconnexion + navigation de l'espace)
# ---------------------------------------------------------------------------
user = utilisateur_courant()
role = user["role"]
pages = ESPACES.get(role, {})

st.sidebar.title("ATS IA")
st.sidebar.write(f"👋 {user['prenom']} {user['nom']}")
st.sidebar.caption(f"Rôle : **{role}**")
st.sidebar.button("🚪 Se déconnecter", on_click=deconnexion, use_container_width=True)
st.sidebar.divider()

if not pages:
    st.error(f"Aucune page n'est définie pour le rôle « {role} ».")
    st.stop()

choix = st.sidebar.radio("Navigation", list(pages.keys()))

# Indicateur backend, utile surtout pour l'espace RH
if role == "RH":
    st.sidebar.divider()
    if api_get("/"):
        st.sidebar.success("API backend connectée")
    else:
        st.sidebar.caption("API backend non connectée")

# ---------------------------------------------------------------------------
# 4) Affichage de la page choisie
# ---------------------------------------------------------------------------
pages[choix]()
