import streamlit as st

# mock data
ROLES_DISPONIBLES = ["Utilisateur", "RH", "Manager", "Admin"]


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


def filtrer_utilisateurs(users, recherche):
    """Filtre par nom, prénom ou id (recherche insensible à la casse)."""
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

# Interface
def main():
    st.set_page_config(page_title="Administration des comptes", page_icon="👤", layout="wide")
    init_state()

    st.title("👤 Administration des comptes")
    st.caption("Lister, rechercher et attribuer le rôle RH aux utilisateurs.")

    # Barre de recherche
    recherche = st.text_input(
        "🔍 Rechercher",
        placeholder="Nom, prénom ou ID…",
    )

    users_filtres = filtrer_utilisateurs(st.session_state.users, recherche)

    st.write(f"**{len(users_filtres)}** compte(s) affiché(s) sur **{len(st.session_state.users)}**.")
    st.divider()

    # En-têtes de colonnes
    cols = st.columns([0.6, 2, 2.5, 3, 1.4, 1.4])
    for col, titre in zip(cols, ["ID", "Nom complet", "Email", "Rôles", "Action RH", "Action Admin"]):
        col.markdown(f"**{titre}**")

    st.divider()

    if not users_filtres:
        st.info("Aucun compte ne correspond à la recherche.")
        return

    # Lignes
    for u in users_filtres:
        c_id, c_nom, c_email, c_roles, c_action_rh, c_action_admin = st.columns([0.6, 2, 2.5, 3, 1.4, 1.4])

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


if __name__ == "__main__":
    main()
