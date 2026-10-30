
"""
Routeur API dédié aux éditeurs de jeux vidéo.

Expose les indicateurs analytiques des éditeurs
à partir de la table Gold mart_editor_performance.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from api.database import fetch_gold_table


router = APIRouter(
    prefix="/api/v1/editors",
    tags=["Editors"]
)


@router.get("/")
def get_editors(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    search: str | None = None,
):
    """
    Récupère les statistiques des éditeurs de jeux vidéo.

    Args:
        limit (int): Nombre maximum d'éditeurs à retourner.
                     Valeur comprise entre 1 et 1000.
        offset (int): Nombre de lignes à ignorer avant
                      de commencer la récupération.
        search (str | None): Terme de recherche appliqué
                             au nom de l'éditeur.

    Returns:
        list[dict]: Liste des éditeurs et de leurs indicateurs
                    analytiques au format JSON.

    Raises:
        HTTPException: Erreur 500 si la récupération des
                       données échoue.
    """
    try:
        data = fetch_gold_table(
            "mart_editor_performance",
            limit=limit,
            offset=offset,
            search_column="editor_name",
            search=search,
        )

        return jsonable_encoder(data)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des éditeurs."
        )
