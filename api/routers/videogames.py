
"""
Routeur API dédié aux jeux vidéo.

Expose les données analytiques des jeux vidéo issues
de la table gold mart_videogame_performance.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from api.database import fetch_gold_table


router = APIRouter(
    prefix="/api/v1/games",
    tags=["Games"]
)


@router.get("/")
def get_games(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: str | None = None,
):
    """
    Récupère la liste des jeux vidéo avec pagination et recherche.

    Les données sont extraites de la table Gold
    mart_videogame_performance.

    Args:
        limit (int): Nombre maximum de jeux à retourner. Valeur comprise entre 1 et 1000.
        offset (int): Nombre de lignes à ignorer avant de commencer la récupération.
        search (str | None): Terme de recherche appliqué au titre du jeu vidéo.

    Returns:
        list[dict]: Liste des jeux vidéo au format JSON.

    Raises:
        HTTPException: Erreur 500 si la récupération des
                        données échoue.
    """
    try:
        data = fetch_gold_table(
            "mart_videogame_performance",
            limit=limit,
            offset=offset,
            search_column="titre",
            search=search,
        )

        return jsonable_encoder(data)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des jeux."
        )
