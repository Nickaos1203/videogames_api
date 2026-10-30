
import streamlit as st

st.set_page_config(
    page_title="Video Games Analytics",
    page_icon="🎮",
    layout="wide",
)

overview_page = st.Page(
    "pages/overview_quality.py",
    title="Vue d'ensemble & qualité",
    icon=":material/space_dashboard:",
    default=True,
)

editor_page = st.Page(
    "pages/editor_analysis.py",
    title="Analyse des éditeurs",
    icon=":material/business:",
)

platform_page = st.Page(
    "pages/platform_genre.py",
    title="Plateformes et genres",
    icon=":material/sports_esports:",
)

navigation = st.navigation(
    {
        "Pilotage": [overview_page],
        "Analyses": [editor_page, platform_page],
    },
    position="sidebar",
)

navigation.run()
