
"""
Tests automatisés des endpoints de l'API.

Vérifie le fonctionnement des routes, la validation des
paramètres, la structure des réponses et la gestion des erreurs.

Les accès à PostgreSQL sont simulés afin de rendre les tests
indépendants de la base de données réelle (mocks).
"""

from fastapi.testclient import TestClient

from api.main import app
from api import main
from api.routers import (
    videogames,
    platforms,
    genres,
    editors,
    quality,
)


client = TestClient(app)


# ============================================================
# TESTS DES ENDPOINTS GÉNÉRAUX
# ============================================================

def test_root():
    """
    Vérifie que l'endpoint d'accueil retourne un message
    de bienvenue et le lien vers la documentation Swagger.
    """
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Bienvenue sur Video Games Analytics API"
    )
    assert response.json()["documentation"] == "/docs"


def test_health_success(monkeypatch):
    """
    Vérifie que le endpoint health retourne un statut sain
    lorsque la connexion à PostgreSQL fonctionne.
    """
    monkeypatch.setattr(main, "check_database", lambda: True)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "api_status": "healthy",
        "database_status": "connected",
    }


def test_health_failure(monkeypatch):
    """
    Vérifie que le endpoint health retourne une erreur HTTP 503
    lorsque la connexion à PostgreSQL échoue.
    """
    def mock_database_error():
        raise Exception("Erreur de connexion PostgreSQL")

    monkeypatch.setattr(
        main,
        "check_database",
        mock_database_error
    )

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Connexion à la base de données indisponible."
    )


# ============================================================
# TESTS DE L'ENDPOINT GAMES
# ============================================================

def test_get_games(monkeypatch):
    """
    Vérifie la récupération des jeux vidéo et la conformité
    de la réponse avec le schéma VideogameResponse.
    """
    mock_data = [
        {
            "videogame_id": 1,
            "url": "https://example.com/game/1",
            "titre": "Test Game",
            "date_sortie": "2024-01-01",
            "editor_name": "Test Editor",
            "genre_name": "Action",
            "score_metacritic": 85,
            "score_utilisateurs": 8.5,
        }
    ]

    def mock_fetch(*args, **kwargs):
        return mock_data

    monkeypatch.setattr(
        videogames,
        "fetch_gold_table",
        mock_fetch
    )

    response = client.get("/api/v1/games/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Test Game"
    assert response.json()[0]["score_utilisateurs"] == 8.5


def test_get_games_search(monkeypatch):
    """
    Vérifie que le paramètre search est transmis à la fonction
    de récupération des jeux vidéo.
    """
    captured = {}

    def mock_fetch(*args, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(
        videogames,
        "fetch_gold_table",
        mock_fetch
    )

    response = client.get(
        "/api/v1/games/",
        params={"search": "Zelda"}
    )

    assert response.status_code == 200
    assert captured["search"] == "Zelda"
    assert captured["search_column"] == "titre"


# ============================================================
# TESTS DE L'ENDPOINT PLATFORMS
# ============================================================

def test_get_platforms(monkeypatch):
    """
    Vérifie la récupération des statistiques par plateforme
    et la conformité de la réponse avec PlatformResponse.
    """
    mock_data = [
        {
            "platform_id": 1,
            "platform_name": "PC",
            "nombre_jeux": 250,
            "score_metacritic_moyen": 82.45,
            "score_utilisateurs_moyen": 8.12,
        }
    ]

    monkeypatch.setattr(
        platforms,
        "fetch_gold_table",
        lambda *args, **kwargs: mock_data
    )

    response = client.get("/api/v1/platforms/")

    assert response.status_code == 200
    assert response.json()[0]["platform_name"] == "PC"
    assert response.json()[0]["nombre_jeux"] == 250


# ============================================================
# TESTS DE L'ENDPOINT GENRES
# ============================================================

def test_get_genres(monkeypatch):
    """
    Vérifie la récupération des statistiques par genre
    et la conformité de la réponse avec GenreResponse.
    """
    mock_data = [
        {
            "genre_id": 1,
            "genre_name": "Action",
            "nombre_jeux": 120,
            "score_metacritic_moyen": 80.5,
            "score_utilisateurs_moyen": 8.2,
        }
    ]

    monkeypatch.setattr(
        genres,
        "fetch_gold_table",
        lambda *args, **kwargs: mock_data
    )

    response = client.get("/api/v1/genres/")

    assert response.status_code == 200
    assert response.json()[0]["genre_name"] == "Action"
    assert response.json()[0]["nombre_jeux"] == 120


# ============================================================
# TESTS DE L'ENDPOINT EDITORS
# ============================================================

def test_get_editors(monkeypatch):
    """
    Vérifie la récupération des statistiques par éditeur
    et la conformité de la réponse avec EditorResponse.
    """
    mock_data = [
        {
            "editor_id": 1,
            "editor_name": "Ubisoft",
            "nombre_jeux": 50,
            "score_metacritic_moyen": 78.5,
            "score_utilisateurs_moyen": 7.9,
        }
    ]

    monkeypatch.setattr(
        editors,
        "fetch_gold_table",
        lambda *args, **kwargs: mock_data
    )

    response = client.get("/api/v1/editors/")

    assert response.status_code == 200
    assert response.json()[0]["editor_name"] == "Ubisoft"
    assert response.json()[0]["nombre_jeux"] == 50


def test_get_editors_search(monkeypatch):
    """
    Vérifie que le paramètre search est transmis à la fonction
    de récupération des éditeurs.
    """
    captured = {}

    def mock_fetch(*args, **kwargs):
        captured.update(kwargs)
        return []

    monkeypatch.setattr(
        editors,
        "fetch_gold_table",
        mock_fetch
    )

    response = client.get(
        "/api/v1/editors/",
        params={"search": "Ubisoft"}
    )

    assert response.status_code == 200
    assert captured["search"] == "Ubisoft"
    assert captured["search_column"] == "editor_name"


# ============================================================
# TESTS DE L'ENDPOINT QUALITY
# ============================================================

def test_get_quality(monkeypatch):
    """
    Vérifie la récupération des indicateurs de qualité
    et la conformité de la réponse avec QualityResponse.
    """
    mock_data = [
        {
            "check_name": "unique_videogame_id",
            "quality_dimension": "Unicité",
            "table_name": "videogame",
            "total_records": 100,
            "failed_records": 0,
            "quality_rate_pct": 100.0,
            "status": "PASS",
        }
    ]

    monkeypatch.setattr(
        quality,
        "fetch_gold_table",
        lambda *args, **kwargs: mock_data
    )

    response = client.get("/api/v1/quality/")

    assert response.status_code == 200
    assert response.json()[0]["check_name"] == (
        "unique_videogame_id"
    )
    assert response.json()[0]["status"] == "PASS"


# ============================================================
# TESTS DE VALIDATION DES PARAMÈTRES
# ============================================================

def test_get_games_invalid_limit():
    """
    Vérifie que l'API refuse un paramètre limit supérieur
    à la valeur maximale autorisée.
    """
    response = client.get(
        "/api/v1/games/",
        params={"limit": 2000}
    )

    assert response.status_code == 422


def test_get_games_invalid_offset():
    """
    Vérifie que l'API refuse une valeur négative
    pour le paramètre offset.
    """
    response = client.get(
        "/api/v1/games/",
        params={"offset": -1}
    )

    assert response.status_code == 422
