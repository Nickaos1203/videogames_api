
"""
Schéma Pydantic dédié aux éditeurs de jeux vidéo.

Définit la structure des réponses de l'API
pour les données issues de mart_editor_performance.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class EditorResponse(BaseModel):
    """
    Représente un éditeur de jeux vidéo.

    Attributs:
        editor_id: Identifiant unique de l'éditeur.
        editor_name: Nom de l'éditeur.
        nombre_jeux: Nombre de jeux associés à l'éditeur.
        score_metacritic_moyen: Score Metacritic moyen.
        score_utilisateurs_moyen: Score moyen des utilisateurs.
    """

    model_config = ConfigDict(from_attributes=True)

    editor_id: int
    editor_name: str
    nombre_jeux: int
    score_metacritic_moyen: Decimal | None = None
    score_utilisateurs_moyen: Decimal | None = None
