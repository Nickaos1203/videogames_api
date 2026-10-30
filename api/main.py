
from fastapi import FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from api.database import fetch_gold_table, check_database

app = FastAPI(
    title="Video Games Analytics API",
    description="API REST pour exposer des données de jeux vidéo.",
    version="1.0.0",
)


@app.get("/", tags=["Accueil"])
def root():
    return {
        "message": "Bienvenue sur Video Games Analytics API",
        "documentation": "/docs",
    }


@app.get("/health", tags=["Monitoring"])
def health():
    try:
        check_database()
        return {
            "api_status": "healthy",
            "database_status": "connected",
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Connexion à la base de données indisponible.",
        )


@app.get("/api/v1/games", tags=["Games"])
def get_games(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: str | None = None,
):
    try:
        data = fetch_gold_table(
            "mart_videogame_performance",
            limit,
            offset,
            search_column="titre",
            search=search,
        )
        return jsonable_encoder(data)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des jeux.",
        )


@app.get("/api/v1/genres", tags=["Genres"])
def get_genres(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    try:
        data = fetch_gold_table("mart_genre_performance", limit, offset)
        return jsonable_encoder(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur de récupération des genres.")


@app.get("/api/v1/platforms", tags=["Platforms"])
def get_platforms(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    try:
        data = fetch_gold_table("mart_platform_performance", limit, offset)
        return jsonable_encoder(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur de récupération des plateformes.")


@app.get("/api/v1/editors", tags=["Editors"])
def get_editors(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: str | None = None,
):
    try:
        data = fetch_gold_table(
            "mart_editor_performance",
            limit,
            offset,
            search_column="editor_name",
            search=search,
        )
        return jsonable_encoder(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur de récupération des éditeurs.")


@app.get("/api/v1/quality", tags=["Data Quality"])
def get_quality(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    try:
        data = fetch_gold_table("mart_data_quality", limit, offset)
        return jsonable_encoder(data)
    except Exception:
        raise HTTPException(status_code=500, detail="Erreur de récupération de la qualité.")
