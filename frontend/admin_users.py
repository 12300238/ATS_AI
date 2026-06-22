import streamlit as st

# mock data
ROLES_DISPONIBLES = ["Utilisateur", "RH", "Admin"]


def donnees_initiales():
    return [
        {"id": 1, "prenom": "Alice", "nom": "Durand", "email": "alice.durand@exemple.fr", "roles": ["Utilisateur"]},
        {"id": 2, "prenom": "Bruno", "nom": "Martin", "email": "bruno.martin@exemple.fr", "roles": ["Utilisateur"]},
        {"id": 3, "prenom": "Chloé", "nom": "Bernard", "email": "chloe.bernard@exemple.fr", "roles": ["RH"]},
        {"id": 4, "prenom": "David", "nom": "Petit", "email": "david.petit@exemple.fr", "roles": ["Utilisateur"]},
        {"id": 5, "prenom": "Emma", "nom": "Robert", "email": "emma.robert@exemple.fr", "roles": ["Admin"]},
        {"id": 6, "prenom": "Farid", "nom": "Moreau", "email": "farid.moreau@exemple.fr", "roles": ["Utilisateur"]},
        {"id": 7, "prenom": "Gaëlle", "nom": "Lefebvre", "email": "gaelle.lefebvre@exemple.fr", "roles": ["Utilisateur"]},
        {"id": 8, "prenom": "Hugo", "nom": "Garcia", "email": "hugo.garcia@exemple.fr", "roles": ["Utilisateur"]},
    ]


#partie métier
def init_state():
    if "users" not in st.session_state:
        st.session_state.users = donnees_initiales()
    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = None
    if "afficher_formulaire_creation" not in st.session_state:
        st.session_state.afficher_formulaire_creation = False
    if "message_creation" not in st.session_state:
        st.session_state.message_creation = None


def filtrer_utilisateurs(users, recherche):
    """Filtre par nom, prénom ou id (pour le mock)"""
    recherche = recherche.strip().lower()
    if not recherche:
        return users
    resultats = []
    for u in users:
        cibles = [u["prenom"].lower(), u["nom"].lower(), str(u["id"])]
        if any(recherche in c for c in cibles):
            resultats.append(u)
    return resultats


def donner_role_rh(user_id):
    for u in st.session_state.users:
        if u["id"] == user_id and "RH" not in u["roles"]:
            u["roles"].append("RH")
            break


def retirer_role_rh(user_id):
    for u in st.session_state.users:
        if u["id"] == user_id and "RH" in u["roles"]:
            u["roles"].remove("RH")
            break


def donner_role_admin(user_id):
    for u in st.session_state.users:
        if u["id"] == user_id and "Admin" not in u["roles"]:
            u["roles"].append("Admin")
            break


def retirer_role_admin(user_id):
    for u in st.session_state.users:
        if u["id"] == user_id and "Admin" in u["roles"]:
            u["roles"].remove("Admin")
            break


def supprimer_utilisateur(user_id):
    st.session_state.users = [u for u in st.session_state.users if u["id"] != user_id]
    if st.session_state.get("confirm_delete") == user_id:
        st.session_state.confirm_delete = None


def demander_confirmation(user_id):
    st.session_state.confirm_delete = user_id


def annuler_confirmation():
    st.session_state.confirm_delete = None


def basculer_formulaire_creation():
    st.session_state.afficher_formulaire_creation = not st.session_state.afficher_formulaire_creation
    st.session_state.message_creation = None


def prochain_id():
    ids = [u["id"] for u in st.session_state.users]
    return max(ids) + 1 if ids else 1


def creer_compte(prenom, nom, email, mdp, role):
    """Valide les champs puis crée le compte. Retourne (succès, message)."""
    prenom = prenom.strip()
    nom = nom.strip()
    email = email.strip()

    if not prenom or not nom or not email or not mdp:
        return False, "Tous les champs sont obligatoires."

    if "@" not in email or "." not in email.split("@")[-1]:
        return False, "L'adresse email n'est pas valide."

    if any(u["email"].lower() == email.lower() for u in st.session_state.users):
        return False, "Un compte avec cet email existe déjà."

    if len(mdp) < 6:
        return False, "Le mot de passe doit contenir au moins 6 caractères."

    nouveau_compte = {
        "id": prochain_id(),
        "prenom": prenom,
        "nom": nom,
        "email": email,
        "mdp": mdp,
        "roles": [role],
    }
    st.session_state.users.append(nouveau_compte)
    st.session_state.afficher_formulaire_creation = False
    return True, f"Compte créé pour {prenom} {nom} (ID {nouveau_compte['id']})."

# Interface
def main():
    st.set_page_config(page_title="Administration des comptes", page_icon="👤", layout="wide")
    init_state()

    st.title("Administration des comptes")
    st.caption("Lister, rechercher et attribuer des rôles aux utilisateurs.")

    # Bouton d'ouverture/fermeture du formulaire de création
    st.button(
        "➕ Créer un compte" if not st.session_state.afficher_formulaire_creation else "✖️ Fermer le formulaire",
        on_click=basculer_formulaire_creation,
    )

    # Message de retour (succès / erreur) suite à une création
    if st.session_state.message_creation:
        type_message, texte = st.session_state.message_creation
        getattr(st, type_message)(texte)
        st.session_state.message_creation = None

    # Formulaire de création de compte
    if st.session_state.afficher_formulaire_creation:
        with st.form("formulaire_creation_compte", clear_on_submit=True):
            st.subheader("Nouveau compte")
            c1, c2 = st.columns(2)
            prenom = c1.text_input("Prénom")
            nom = c2.text_input("Nom")
            email = st.text_input("Email")
            mdp = st.text_input("Mot de passe", type="password")
            role = st.selectbox("Rôle", ROLES_DISPONIBLES)

            valider = st.form_submit_button("Créer le compte", type="primary")

            if valider:
                succes, texte = creer_compte(prenom, nom, email, mdp, role)
                st.session_state.message_creation = ("success" if succes else "error", texte)
                st.rerun()

    st.divider()

    # Barre de recherche
    recherche = st.text_input(
        "🔍 Rechercher",
        placeholder="Nom, prénom ou ID…",
    )

    users_filtres = filtrer_utilisateurs(st.session_state.users, recherche)

    st.write(f"**{len(users_filtres)}** compte(s) affiché(s) sur **{len(st.session_state.users)}**.")
    st.divider()

    # En-têtes de colonnes
    cols = st.columns([0.6, 2, 2.5, 2.2, 1.2, 1.2, 1.2])
    for col, titre in zip(cols, ["ID", "Nom complet", "Email", "Rôles", "Action RH", "Action Admin", "Supprimer"]):
        col.markdown(f"**{titre}**")

    st.divider()

    if not users_filtres:
        st.info("Aucun compte ne correspond à la recherche.")
        return

    # Lignes
    for u in users_filtres:
        c_id, c_nom, c_email, c_roles, c_action_rh, c_action_admin, c_action_suppr = st.columns(
            [0.6, 2, 2.5, 2.2, 1.2, 1.2, 1.2]
        )

        c_id.write(u["id"])
        c_nom.write(f"{u['prenom']} {u['nom']}")
        c_email.write(u["email"])

        # Affichage des rôles sous forme de badges
        badges = " ".join(f"`{r}`" for r in u["roles"])
        c_roles.markdown(badges)

        # Bouton contextuel : donner ou retirer le rôle RH
        if "RH" in u["roles"]:
            c_action_rh.button(
                "Retirer RH",
                key=f"retirer_rh_{u['id']}",
                on_click=retirer_role_rh,
                args=(u["id"],),
                use_container_width=True,
            )
        else:
            c_action_rh.button(
                "Donner RH",
                key=f"donner_rh_{u['id']}",
                type="primary",
                on_click=donner_role_rh,
                args=(u["id"],),
                use_container_width=True,
            )

        # Bouton contextuel : donner ou retirer le rôle Admin
        if "Admin" in u["roles"]:
            c_action_admin.button(
                "Retirer Admin",
                key=f"retirer_admin_{u['id']}",
                on_click=retirer_role_admin,
                args=(u["id"],),
                use_container_width=True,
            )
        else:
            c_action_admin.button(
                "Donner Admin",
                key=f"donner_admin_{u['id']}",
                type="primary",
                on_click=donner_role_admin,
                args=(u["id"],),
                use_container_width=True,
            )

        # Bouton de suppression (avec confirmation)
        c_action_suppr.button(
            "Supprimer",
            key=f"supprimer_{u['id']}",
            on_click=demander_confirmation,
            args=(u["id"],),
            use_container_width=True,
        )

        # Bandeau de confirmation affiché sous la ligne concernée
        if st.session_state.confirm_delete == u["id"]:
            c_warn, c_confirm, c_annuler = st.columns([5.5, 1.2, 1.2])
            c_warn.warning(
                f"Confirmer la suppression de **{u['prenom']} {u['nom']}** (ID {u['id']}) ? Cette action est irréversible."
            )
            c_confirm.button(
                "Confirmer",
                key=f"confirmer_suppr_{u['id']}",
                type="primary",
                on_click=supprimer_utilisateur,
                args=(u["id"],),
                use_container_width=True,
            )
            c_annuler.button(
                "Annuler",
                key=f"annuler_suppr_{u['id']}",
                on_click=annuler_confirmation,
                use_container_width=True,
            )

        st.divider()


if __name__ == "__main__":
    main()
