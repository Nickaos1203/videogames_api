
"""
Schéma Pydantic dédié aux plateformes de jeux vidéo.

Définit la structure des réponses de l'API
pour les données issues de mart_platform_performance.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PlatformResponse(BaseModel):
    """
    Représente une plateforme de jeux vidéo.

    Attributs:
        platform_id: Identifiant unique de la plateforme.
        platform_name: Nom de la plateforme.
        nombre_jeux: Nombre de jeux associés à la plateforme.
        score_metacritic_moyen: Score Metacritic moyen.
        score_utilisateurs_moyen: Score moyen des utilisateurs.
    """

    model_config = ConfigDict(from_attributes=True)

    platform_id: int
    platform_name: str
    nombre_jeux: int
    score_metacritic_moyen: Decimal | None = None
    score_utilisateurs_moyen: Decimal | None = None
