
import pandas as pd
import plotly.express as px
import streamlit as st

from db import load_gold

st.title("🎮 Vue d'ensemble & qualité des données")
st.caption("Synthèse des jeux vidéo et fiabilité des données")

try:
    games = load_gold("mart_videogame_performance")
    genres = load_gold("mart_genre_performance")
    platforms = load_gold("mart_platform_performance")
    quality = load_gold("mart_data_quality")

    # --------------------------------------------------------
    # KPI globaux : une ligne par jeu
    # --------------------------------------------------------
    st.header("Vue d'ensemble")

    genre_col = "genre_name" if "genre_name" in genres.columns else "genre"
    platform_col = (
        "platform_name"
        if "platform_name" in platforms.columns
        else "plateforme"
    )

    score_col = "score_metacritic"

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Jeux analysés", f"{len(games):,}".replace(",", " "))
    c2.metric("Genres", genres[genre_col].nunique())
    c3.metric("Plateformes", platforms[platform_col].nunique())

    if score_col in games.columns:
        avg_score = games[score_col].mean()
        c4.metric(
            "Score Metacritic moyen",
            f"{avg_score:.1f}/100" if pd.notna(avg_score) else "N/A",
        )
    else:
        c4.metric("Score Metacritic moyen", "N/A")

    st.divider()

    # --------------------------------------------------------
    # Qualité des données
    # --------------------------------------------------------
    st.title("Qualité des données")
    st.caption("Détail des contrôles de qualité issus de gold.mart_data_quality.")

    df_quality = load_gold("mart_data_quality")

    if df_quality.empty:
        st.info("Aucun contrôle de qualité disponible.")
        st.stop()

    # Colonnes affichées dans la table
    columns = [
        "check_name",
        "quality_dimension",
        "table_name",
        "total_records",
        "failed_records",
        "quality_rate_pct",
        "status",
    ]

    # Vérification des colonnes disponibles
    missing_columns = [
        col for col in columns if col not in df_quality.columns
    ]

    if missing_columns:
        st.error(
            f"Colonnes manquantes dans mart_data_quality : "
            f"{', '.join(missing_columns)}"
        )
        st.stop()

    # Affichage exclusif du détail des contrôles
    st.dataframe(
        df_quality[columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "check_name": st.column_config.TextColumn(
                "Contrôle"
            ),
            "quality_dimension": st.column_config.TextColumn(
                "Dimension"
            ),
            "table_name": st.column_config.TextColumn(
                "Table"
            ),
            "total_records": st.column_config.NumberColumn(
                "Enregistrements",
                format="%d",
            ),
            "failed_records": st.column_config.NumberColumn(
                "Échecs",
                format="%d",
            ),
            "quality_rate_pct": st.column_config.NumberColumn(
                "Taux de conformité",
                format="%.2f %%"
            ),
            "status": st.column_config.TextColumn(
                "Statut"
            ),
        },
    )

except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")