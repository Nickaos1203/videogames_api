
import plotly.express as px
import streamlit as st

from db import load_gold

st.title("🏢 Analyse des éditeurs")

try:
    df = load_gold("mart_editor_performance")

    if df.empty:
        st.warning("Aucune donnée disponible.")
        st.stop()

    name = "editor_name"
    count = "nombre_jeux"
    score = "score_metacritic_moyen"

    top_n = st.slider(
        "Nombre d'éditeurs à afficher",
        min_value=5,
        max_value=max(5, min(50, len(df))),
        value=min(10, max(5, len(df))),
    )

    top = df.sort_values(count, ascending=False).head(top_n)

    st.subheader("Nombre de jeux par éditeur")

    fig_count = px.bar(
        top.sort_values(count),
        x=count,
        y=name,
        orientation="h",
        labels={count: "Nombre de jeux", name: "Éditeur"},
    )
    st.plotly_chart(fig_count, use_container_width=True)

    if score in df.columns:
        st.subheader("Score Metacritic moyen par éditeur")

        scored = df.dropna(subset=[score]).sort_values(
            score, ascending=False
        ).head(top_n)

        fig_score = px.bar(
            scored.sort_values(score),
            x=score,
            y=name,
            orientation="h",
            labels={score: "Score moyen", name: "Éditeur"},
        )
        st.plotly_chart(fig_score, use_container_width=True)

    st.subheader("Détail des éditeurs")
    st.dataframe(df, use_container_width=True, hide_index=True)

except Exception as error:
    st.error(f"Erreur lors du chargement des éditeurs : {error}")
