
"""
Schéma Pydantic dédié aux jeux vidéo.

Définit la structure des réponses de l'API
pour les données issues de mart_videogame_performance.
"""

from datetime import date

from pydantic import BaseModel, ConfigDict


class VideogameResponse(BaseModel):
    """
    Représente un jeu vidéo dans les réponses de l'API.

    Attributs:
        videogame_id: Identifiant unique du jeu.
        url: URL du jeu.
        titre: Titre du jeu vidéo.
        date_sortie: Date de sortie du jeu.
        editor_name: Nom de l'éditeur.
        genre_name: Genre du jeu.
        score_metacritic: Score attribué par Metacritic.
        score_utilisateurs: Score attribué par les utilisateurs.
    """

    model_config = ConfigDict(from_attributes=True)

    videogame_id: int
    url: str
    titre: str
    date_sortie: date | None = None
    editor_name: str | None = None
    genre_name: str | None = None
    score_metacritic: int | None = None
    score_utilisateurs: float | None = None
