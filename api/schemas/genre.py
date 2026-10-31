
"""
Schéma Pydantic dédié aux genres de jeux vidéo.

Définit la structure des réponses de l'API
pour les données issues de mart_genre_performance.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class GenreResponse(BaseModel):
    """
    Représente un genre de jeux vidéo.

    Attributs:
        genre_id: Identifiant unique du genre.
        genre_name: Nom du genre.
        nombre_jeux: Nombre de jeux associés au genre.
        score_metacritic_moyen: Score Metacritic moyen.
        score_utilisateurs_moyen: Score moyen des utilisateurs.
    """

    model_config = ConfigDict(from_attributes=True)

    genre_id: int
    genre_name: str
    nombre_jeux: int
    score_metacritic_moyen: Decimal | None = None
    score_utilisateurs_moyen: Decimal | None = None
