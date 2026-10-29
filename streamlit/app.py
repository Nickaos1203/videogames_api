
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="Video Games Analytics",
    page_icon="🎮",
    layout="wide",
)

st.title("🎮 Video Games Analytics")
st.caption("Analyse des jeux vidéo extraits de Metacritic")

@st.cache_data(ttl=60)
def load_data(query):
    connection = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )
    try:
        return pd.read_sql_query(query, connection)
    finally:
        connection.close()


try:
    genres = load_data("""
        SELECT *
        FROM gold.mart_genre_performance
    """)

    platforms = load_data("""
        SELECT *
        FROM gold.mart_platform_performance
    """)

    if genres.empty or platforms.empty:
        st.warning("Les tables Gold ne contiennent pas encore de données.")
        st.stop()

    # Indicateurs globaux calculés à partir des agrégats
    total_games = genres["nombre_jeux"].sum()
    genre_count = genres["genre"].nunique()
    platform_count = platforms["plateforme"].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Jeux analysés", f"{total_games:,}".replace(",", " "))
    c2.metric("Genres", genre_count)
    c3.metric("Plateformes", platform_count)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Score Metacritic moyen par genre")
        genre_scores = genres.dropna(
            subset=["score_metacritic_moyen"]
        ).sort_values("score_metacritic_moyen", ascending=False)

        fig_genre = px.bar(
            genre_scores,
            x="score_metacritic_moyen",
            y="genre",
            orientation="h",
            labels={
                "score_metacritic_moyen": "Score moyen",
                "genre": "Genre",
            },
        )
        fig_genre.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_genre, use_container_width=True)

    with right:
        st.subheader("Nombre de jeux par plateforme")
        platform_counts = platforms.sort_values(
            "nombre_jeux", ascending=False
        )

        fig_platform = px.bar(
            platform_counts,
            x="plateforme",
            y="nombre_jeux",
            labels={
                "plateforme": "Plateforme",
                "nombre_jeux": "Nombre de jeux",
            },
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    st.subheader("Détail des genres")
    st.dataframe(genres, use_container_width=True, hide_index=True)

    st.subheader("Détail des plateformes")
    st.dataframe(platforms, use_container_width=True, hide_index=True)

except Exception as error:
    st.error(f"Impossible de charger les données PostgreSQL : {error}")
