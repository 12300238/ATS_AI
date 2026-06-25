import streamlit as st

from views.rh.common import load_candidates, load_jobs, inject_style, header


def show():
    inject_style()
    candidates = load_candidates()
    jobs = load_jobs()

    header("Analytique / Rapports", "Mesurer le volume, la qualite du matching et la progression du recrutement.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Scores par offre postulee</div>', unsafe_allow_html=True)
        st.bar_chart(candidates.groupby("Offre postulee")["Score"].mean().sort_values(ascending=False))
    with col2:
        st.markdown('<div class="section-title">Candidatures par offre</div>', unsafe_allow_html=True)
        st.bar_chart(jobs.set_index("Titre")["Candidatures"].sort_values(ascending=False))

    report = {
        "Taux de profils >= 80": f"{(candidates['Score'].ge(80).mean() * 100):.0f}%",
        "Meilleur canal": "Depot CV plateforme",
        "Poste le plus demande": jobs.sort_values("Candidatures", ascending=False).iloc[0]["Titre"],
        "Delai moyen estime": "6 jours",
    }
    st.json(report)
    st.download_button(
        "Telecharger le rapport CSV",
        data=candidates.to_csv(index=False).encode("utf-8"),
        file_name="rapport_candidatures.csv",
        mime="text/csv",
    )
