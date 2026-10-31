
"""
Point d'entrée principal de Video Games Analytics API.

Initialise l'application FastAPI, configure les routes
et expose les endpoints de monitoring.
"""

from fastapi import FastAPI, HTTPException

from api.database import check_database
from api.routers import (
    videogames,
    platforms,
    genres,
    editors,
    quality,
)


# Initialisation de l'application FastAPI
app = FastAPI(
    title="Video Games Analytics API",
    description="API REST permettant d'exposer les données analytiques de jeux vidéo ",
    version="1.0.0",
)


# Enregistrement des routeurs
app.include_router(videogames.router)
app.include_router(platforms.router)
app.include_router(genres.router)
app.include_router(editors.router)
app.include_router(quality.router)


@app.get("/", tags=["Accueil"])
def root():
    """
    Retourne les informations générales de l'API.

    Returns:
        dict: Message de bienvenue et lien vers la documentation.
    """
    return {
        "message": "Bienvenue sur Video Games Analytics API",
        "documentation": "/docs",
    }


@app.get("/health", tags=["Monitoring"])
def health():
    """
    Vérifie l'état de fonctionnement de l'API et de PostgreSQL.

    Returns:
        dict: Statut de l'API et de la connexion à la base.

    Raises:
        HTTPException: Erreur 503 si PostgreSQL est inaccessible.
    """
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
