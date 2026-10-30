
import plotly.express as px
import streamlit as st

from db import load_gold

st.title("🎮 Analyse des plateformes et des genres")

try:
    genres = load_gold("mart_genre_performance")
    platforms = load_gold("mart_platform_performance")

    genre_name = (
        "genre_name" if "genre_name" in genres.columns else "genre"
    )
    platform_name = (
        "platform_name"
        if "platform_name" in platforms.columns
        else "plateforme"
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Score Metacritic moyen par genre")

        genre_score = genres.dropna(
            subset=["score_metacritic_moyen"]
        ).sort_values("score_metacritic_moyen")

        fig_genre = px.bar(
            genre_score,
            x="score_metacritic_moyen",
            y=genre_name,
            orientation="h",
            labels={
                "score_metacritic_moyen": "Score moyen",
                genre_name: "Genre",
            },
        )
        st.plotly_chart(fig_genre, use_container_width=True)

    with right:
        st.subheader("Nombre de jeux par plateforme")

        platform_count = platforms.sort_values("nombre_jeux")

        fig_platform = px.bar(
            platform_count,
            x="nombre_jeux",
            y=platform_name,
            orientation="h",
            labels={
                "nombre_jeux": "Nombre de jeux",
                platform_name: "Plateforme",
            },
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    with st.expander("Détail des genres"):
        st.dataframe(genres, use_container_width=True, hide_index=True)

    with st.expander("Détail des plateformes"):
        st.dataframe(
            platforms, use_container_width=True, hide_index=True
        )

except Exception as error:
    st.error(f"Erreur lors du chargement des données : {error}")
