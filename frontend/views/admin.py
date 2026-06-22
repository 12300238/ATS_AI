import streamlit as st
from services import ROLES


# ---------------------------------------------------------------------------
# Partie métier (agit sur st.session_state.comptes, partagé avec l'auth)
# ---------------------------------------------------------------------------
def filtrer_comptes(comptes, recherche):
    """Filtre par nom, prénom ou id."""
    recherche = recherche.strip().lower()
    if not recherche:
        return comptes
    resultats = []
    for c in comptes:
        cibles = [c["prenom"].lower(), c["nom"].lower(), str(c["id"])]
        if any(recherche in cible for cible in cibles):
            resultats.append(c)
    return resultats


def changer_role(user_id, widget_key):
    nouveau_role = st.session_state[widget_key]
    compte = next((c for c in st.session_state.comptes if c["id"] == user_id), None)
    if compte is None:
        return

    # Garde-fou : un admin ne peut pas se retirer à lui-même le rôle Admin
    # (sinon il perd l'accès à cette page sans pouvoir revenir en arrière).
    if user_id == st.session_state.get("id_connecte") and nouveau_role != "Admin":
        st.session_state[widget_key] = compte["role"]  # on annule la sélection
        st.session_state.message_role = (
            "warning",
            "Vous ne pouvez pas retirer votre propre rôle Admin.",
        )
        return

    ancien = compte["role"]
    compte["role"] = nouveau_role
    if ancien != nouveau_role:
        st.session_state.message_role = (
            "success",
            f"Rôle de {compte['prenom']} {compte['nom']} : {ancien} → {nouveau_role}.",
        )


def supprimer_compte(user_id):
    st.session_state.comptes = [c for c in st.session_state.comptes if c["id"] != user_id]
    if st.session_state.get("confirm_delete") == user_id:
        st.session_state.confirm_delete = None


def demander_confirmation(user_id):
    st.session_state.confirm_delete = user_id


def annuler_confirmation():
    st.session_state.confirm_delete = None


def basculer_formulaire_creation():
    st.session_state.afficher_formulaire_creation = not st.session_state.get(
        "afficher_formulaire_creation", False
    )
    st.session_state.message_creation = None


def prochain_id():
    ids = [c["id"] for c in st.session_state.comptes]
    return max(ids) + 1 if ids else 1


def creer_compte(prenom, nom, email, mdp, role):
    """Valide les champs puis crée le compte. Retourne (succès, message)."""
    prenom, nom, email = prenom.strip(), nom.strip(), email.strip()

    if not prenom or not nom or not email or not mdp:
        return False, "Tous les champs sont obligatoires."
    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "L'adresse email n'est pas valide."
    if any(c["email"].lower() == email.lower() for c in st.session_state.comptes):
        return False, "Un compte avec cet email existe déjà."
    if len(mdp) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."

    nouveau = {
        "id": prochain_id(),
        "prenom": prenom,
        "nom": nom,
        "email": email,
        # ⚠️ Mock uniquement : à hasher côté serveur dans un vrai backend.
        "mdp": mdp,
        "role": role,
    }
    st.session_state.comptes.append(nouveau)
    st.session_state.afficher_formulaire_creation = False
    return True, f"Compte créé pour {prenom} {nom} (ID {nouveau['id']})."


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------
def show_admin():
    # États propres à la page admin
    st.session_state.setdefault("confirm_delete", None)
    st.session_state.setdefault("afficher_formulaire_creation", False)
    st.session_state.setdefault("message_creation", None)
    st.session_state.setdefault("message_role", None)

    # Feedback du dernier changement de rôle (toast bien visible)
    if st.session_state.message_role:
        type_msg, texte = st.session_state.message_role
        icone = "✅" if type_msg == "success" else "⚠️"
        st.toast(texte, icon=icone)
        st.session_state.message_role = None

    mon_id = st.session_state.get("id_connecte")

    st.title("🛠️ Administration des comptes")
    st.caption("Lister, rechercher, créer, attribuer un rôle et supprimer des comptes.")

    # Bouton d'ouverture/fermeture du formulaire de création
    st.button(
        "➕ Créer un compte"
        if not st.session_state.afficher_formulaire_creation
        else "✖️ Fermer le formulaire",
        on_click=basculer_formulaire_creation,
    )

    # Message de retour suite à une création
    if st.session_state.message_creation:
        type_message, texte = st.session_state.message_creation
        getattr(st, type_message)(texte)
        st.session_state.message_creation = None

    # Formulaire de création
    if st.session_state.afficher_formulaire_creation:
        with st.form("formulaire_creation_compte", clear_on_submit=True):
            st.subheader("Nouveau compte")
            c1, c2 = st.columns(2)
            prenom = c1.text_input("Prénom")
            nom = c2.text_input("Nom")
            email = st.text_input("Email")
            mdp = st.text_input("Mot de passe", type="password")
            role = st.selectbox("Rôle", ROLES)

            if st.form_submit_button("Créer le compte", type="primary"):
                succes, texte = creer_compte(prenom, nom, email, mdp, role)
                st.session_state.message_creation = ("success" if succes else "error", texte)
                st.rerun()

    st.divider()

    # Recherche
    recherche = st.text_input("🔍 Rechercher", placeholder="Nom, prénom ou ID…")
    comptes_filtres = filtrer_comptes(st.session_state.comptes, recherche)

    st.write(
        f"**{len(comptes_filtres)}** compte(s) affiché(s) sur **{len(st.session_state.comptes)}**."
    )
    st.divider()

    # En-têtes
    cols = st.columns([0.6, 2, 3, 2, 1.4])
    for col, titre in zip(cols, ["ID", "Nom complet", "Email", "Rôle", "Suppression"]):
        col.markdown(f"**{titre}**")
    st.divider()

    if not comptes_filtres:
        st.info("Aucun compte ne correspond à la recherche.")
        return

    # Lignes
    for c in comptes_filtres:
        c_id, c_nom, c_email, c_role, c_suppr = st.columns([0.6, 2, 3, 2, 1.4])

        c_id.write(c["id"])
        c_nom.write(f"{c['prenom']} {c['nom']}")
        c_email.write(c["email"])

        # Menu déroulant pour changer le rôle
        role_key = f"role_{c['id']}"
        c_role.selectbox(
            "Rôle",
            ROLES,
            index=ROLES.index(c["role"]),
            key=role_key,
            label_visibility="collapsed",
            on_change=changer_role,
            args=(c["id"], role_key),
        )

        # Suppression : on s'interdit de supprimer son propre compte
        if c["id"] == mon_id:
            c_suppr.caption("Vous")
        else:
            c_suppr.button(
                "🗑️ Supprimer",
                key=f"supprimer_{c['id']}",
                on_click=demander_confirmation,
                args=(c["id"],),
                use_container_width=True,
            )

        # Bandeau de confirmation
        if st.session_state.confirm_delete == c["id"]:
            c_warn, c_ok, c_no = st.columns([5.5, 1.2, 1.2])
            c_warn.warning(
                f"Supprimer **{c['prenom']} {c['nom']}** (ID {c['id']}) ? Action irréversible."
            )
            c_ok.button(
                "Confirmer",
                key=f"confirmer_{c['id']}",
                type="primary",
                on_click=supprimer_compte,
                args=(c["id"],),
                use_container_width=True,
            )
            c_no.button(
                "Annuler",
                key=f"annuler_{c['id']}",
                on_click=annuler_confirmation,
                use_container_width=True,
            )

        st.divider()
