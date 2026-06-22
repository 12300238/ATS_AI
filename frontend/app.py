import streamlit as st

from pages.dashboard import show_dashboard
from pages.profile import show_profile
from pages.jobs import show_jobs
from pages.assistant import show_assistant

st.set_page_config(
    page_title="ATS Intelligent",
    page_icon="📄",
    layout="wide"
)

with open("styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.sidebar.title("ATS IA")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Mon Profil",
        "Offres",
        "Assistant IA"
    ]
)

if page == "Dashboard":
    show_dashboard()

elif page == "Mon Profil":
    show_profile()

elif page == "Offres":
    show_jobs()

elif page == "Assistant IA":
    show_assistant()