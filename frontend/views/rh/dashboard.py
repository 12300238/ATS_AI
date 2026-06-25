import streamlit as st

from views.rh.common import (
    STATUSES,
    load_candidates,
    load_jobs,
    inject_style,
    header,
    metric_card,
    status_badge,
)


def show():
    inject_style()
    candidates = load_candidates()
    jobs = load_jobs()

    header("Dashboard RH", "Vue d'ensemble des candidatures, scores IA et offres actives.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Candidatures", len(candidates), "+5 cette semaine")
    with col2:
        metric_card("Score moyen", f"{candidates['Score'].mean():.0f}%", "Matching IA")
    with col3:
        metric_card("Offres ouvertes", len(jobs[jobs["Statut"] == "Ouverte"]), "A pourvoir")
    with col4:
        metric_card("Entretiens", len(candidates[candidates["Statut"] == "Entretien"]), "En cours")

    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="section-title">Pipeline de candidatures</div>', unsafe_allow_html=True)
        status_counts = candidates["Statut"].value_counts().reindex(STATUSES, fill_value=0)
        st.bar_chart(status_counts)

    with right:
        st.markdown('<div class="section-title">Top profils</div>', unsafe_allow_html=True)
        for _, row in candidates.sort_values("Score", ascending=False).head(3).iterrows():
            st.markdown(
                f"""
                <div class="candidate-card">
                    <h3>{row['Nom']} - {row['Score']}%</h3>
                    <p>{row['Offre postulee']} · {row['Experience']} · {status_badge(row['Statut'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-title">Candidatures</div>', unsafe_allow_html=True)
    activity = candidates[
        ["Date", "Candidature ID", "Nom", "Offre ID", "Offre postulee", "Statut", "Score"]
    ].sort_values("Date", ascending=False)
    st.dataframe(activity, use_container_width=True, hide_index=True)
