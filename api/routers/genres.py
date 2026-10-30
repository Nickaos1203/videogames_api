
"""
Routeur API dédié aux genres de jeux vidéo.

Expose les indicateurs analytiques des genres
à partir de la table Gold mart_genre_performance.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from api.database import fetch_gold_table


router = APIRouter(
    prefix="/api/v1/genres",
    tags=["Genres"]
)


@router.get("/")
def get_genres(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Récupère les statistiques des genres de jeux vidéo.

    Args:
        limit (int): Nombre maximum de genres à retourner.
                     Valeur comprise entre 1 et 1000.
        offset (int): Nombre de lignes à ignorer avant
                      de commencer la récupération.

    Returns:
        list[dict]: Liste des genres et de leurs indicateurs
                    analytiques au format JSON.

    Raises:
        HTTPException: Erreur 500 si la récupération des
                       données échoue.
    """
    try:
        data = fetch_gold_table(
            "mart_genre_performance",
            limit=limit,
            offset=offset,
        )

        return jsonable_encoder(data)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des genres."
        )
