
"""
Schéma Pydantic dédié à la qualité des données.

Définit la structure des réponses de l'API
pour les données issues de mart_data_quality.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class QualityResponse(BaseModel):
    """
    Représente un contrôle de qualité des données.

    Attributs:
        check_name: Nom du contrôle effectué.
        quality_dimension: Dimension de qualité évaluée.
        table_name: Nom de la table concernée.
        total_records: Nombre total d'enregistrements contrôlés.
        failed_records: Nombre d'enregistrements non conformes.
        quality_rate_pct: Taux de conformité en pourcentage.
        status: Statut du contrôle de qualité.
    """

    model_config = ConfigDict(from_attributes=True)

    check_name: str
    quality_dimension: str
    table_name: str
    total_records: int
    failed_records: int
    quality_rate_pct: Decimal | None = None
    status: str
