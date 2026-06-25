"""
Messagerie commune aux trois espaces (candidat, RH, admin).

Règle d'accès :
- Tout le monde peut consulter ses conversations et y répondre.
- Seuls les rôles RH et Admin peuvent DÉMARRER une nouvelle conversation.

Les conversations vivent en mémoire (st.session_state.conversations), comme le
reste de l'app. À remplacer par des appels backend le moment venu.
"""

from datetime import datetime

import streamlit as st

from auth import utilisateur_courant, compte_par_id


# Rôles autorisés à initier une conversation
ROLES_INITIATEURS = {"RH", "Admin"}


# ---------------------------------------------------------------------------
# État & logique métier
# ---------------------------------------------------------------------------
def init_messagerie():
    if "conversations" not in st.session_state:
        # Conversation de démonstration : Sophie (RH) écrit à Thomas (candidat)
        st.session_state.conversations = [
            {
                "id": 1,
                "participants": [2, 1],  # 2 = Sophie (RH), 1 = Thomas (Utilisateur)
                "cree_par": 2,
                "messages": [
                    {"auteur": 2, "texte": "Bonjour Thomas, votre profil nous intéresse. Êtes-vous disponible cette semaine pour un entretien ?", "date": "2026-06-20 09:30"},
                ],
            }
        ]
    st.session_state.setdefault("conv_active", None)


def prochain_conv_id():
    ids = [c["id"] for c in st.session_state.conversations]
    return max(ids) + 1 if ids else 1


def conversations_de(user_id):
    return [c for c in st.session_state.conversations if user_id in c["participants"]]


def autre_participant(conv, user_id):
    """Renvoie le compte de l'autre personne de la conversation."""
    for pid in conv["participants"]:
        if pid != user_id:
            return compte_par_id(pid)
    return None


def creer_conversation(createur, destinataire_id, premier_message):
    """Crée une conversation. Réservé aux rôles initiateurs (double sécurité)."""
    if createur["role"] not in ROLES_INITIATEURS:
        return False, "Vous n'êtes pas autorisé à démarrer une conversation."
    if destinataire_id == createur["id"]:
        return False, "Vous ne pouvez pas démarrer une conversation avec vous-même."
    if not premier_message.strip():
        return False, "Le message ne peut pas être vide."

    conv = {
        "id": prochain_conv_id(),
        "participants": [createur["id"], destinataire_id],
        "cree_par": createur["id"],
        "messages": [
            {
                "auteur": createur["id"],
                "texte": premier_message.strip(),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        ],
    }
    st.session_state.conversations.append(conv)
    st.session_state.conv_active = conv["id"]
    return True, "Conversation démarrée."


def envoyer_message(conv_id, auteur_id, texte):
    if not texte.strip():
        return
    for c in st.session_state.conversations:
        if c["id"] == conv_id:
            c["messages"].append(
                {
                    "auteur": auteur_id,
                    "texte": texte.strip(),
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
            )
            break


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------
def show():
    init_messagerie()
    moi = utilisateur_courant()
    peut_initier = moi["role"] in ROLES_INITIATEURS

    st.title("💬 Messagerie")

    # --- Démarrer une conversation (RH / Admin uniquement) --------------
    if peut_initier:
        with st.expander("➕ Nouvelle conversation", expanded=False):
            autres = [c for c in st.session_state.comptes if c["id"] != moi["id"]]
            libelles = {
                f"{c['prenom']} {c['nom']} ({c['role']})": c["id"] for c in autres
            }
            with st.form("form_nouvelle_conv", clear_on_submit=True):
                choix = st.selectbox("Destinataire", list(libelles.keys()))
                message = st.text_area("Message", placeholder="Votre message…")
                if st.form_submit_button("Démarrer", type="primary"):
                    ok, info = creer_conversation(moi, libelles[choix], message)
                    st.session_state.msg_feedback = ("success" if ok else "error", info)
                    st.rerun()
    else:
        st.caption("Seuls les RH et les administrateurs peuvent démarrer une conversation.")

    if st.session_state.get("msg_feedback"):
        type_msg, texte = st.session_state.msg_feedback
        getattr(st, type_msg)(texte)
        st.session_state.msg_feedback = None

    st.divider()

    # --- Liste des conversations de l'utilisateur -----------------------
    mes_convs = conversations_de(moi["id"])
    if not mes_convs:
        st.info("Vous n'avez aucune conversation pour le moment.")
        return

    def libelle_conv(conv):
        autre = autre_participant(conv, moi["id"])
        nom = f"{autre['prenom']} {autre['nom']}" if autre else "Inconnu"
        dernier = conv["messages"][-1]["texte"] if conv["messages"] else ""
        apercu = (dernier[:35] + "…") if len(dernier) > 35 else dernier
        return f"{nom} — {apercu}" if apercu else nom

    ids_convs = [c["id"] for c in mes_convs]
    index_defaut = (
        ids_convs.index(st.session_state.conv_active)
        if st.session_state.conv_active in ids_convs
        else 0
    )
    conv_id = st.selectbox(
        "Conversations",
        ids_convs,
        index=index_defaut,
        format_func=lambda cid: libelle_conv(next(c for c in mes_convs if c["id"] == cid)),
    )
    st.session_state.conv_active = conv_id
    conv = next(c for c in mes_convs if c["id"] == conv_id)

    autre = autre_participant(conv, moi["id"])
    if autre:
        st.subheader(f"Conversation avec {autre['prenom']} {autre['nom']}")

    # --- Fil de messages -----------------------------------------------
    for m in conv["messages"]:
        de_moi = m["auteur"] == moi["id"]
        auteur = compte_par_id(m["auteur"])
        nom = f"{auteur['prenom']} {auteur['nom']}" if auteur else "Inconnu"
        with st.chat_message("user" if de_moi else "assistant"):
            st.markdown(f"**{nom}** · _{m['date']}_")
            st.write(m["texte"])

    # --- Répondre (tout le monde) --------------------------------------
    with st.form("form_reponse", clear_on_submit=True):
        reponse = st.text_input("Votre réponse")
        if st.form_submit_button("Envoyer", type="primary"):
            envoyer_message(conv_id, moi["id"], reponse)
            st.rerun()
