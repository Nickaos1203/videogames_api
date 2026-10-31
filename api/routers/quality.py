
"""
Routeur API dédié à la qualité des données.

Expose les indicateurs de qualité calculés par dbt
à partir de la table Gold mart_data_quality.
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder

from api.database import fetch_gold_table
from api.schemas.quality import QualityResponse


router = APIRouter(
    prefix="/api/v1/quality",
    tags=["Data Quality"]
)


@router.get("/", response_model=list[QualityResponse])
def get_quality(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Récupère les indicateurs de qualité des données.

    Args:
        limit (int): Nombre maximum de contrôles à retourner.
                     Valeur comprise entre 1 et 1000.
        offset (int): Nombre de lignes à ignorer avant
                      de commencer la récupération.

    Returns:
        list[dict]: Liste des contrôles de qualité et de leurs
                    indicateurs au format JSON.

    Raises:
        HTTPException: Erreur 500 si la récupération des
                       données échoue.
    """
    try:
        data = fetch_gold_table(
            "mart_data_quality",
            limit=limit,
            offset=offset,
        )

        return jsonable_encoder(data)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des données de qualité."
        )
