"""
Tests du scaffold : ne nécessitent pas de connexion Mongo réelle pour
le test de /, et tolèrent l'absence de Mongo pour /health/db (qui doit
alors répondre 503 proprement, sans planter).
"""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_health_db_does_not_crash(client):
    """
    Sans Mongo configuré, on attend un 503 propre (pas une exception
    non gérée). Si MONGO_URI pointe vers un vrai cluster joignable,
    on accepte aussi le 200.
    """
    response = client.get("/health/db")
    assert response.status_code in (200, 503)
    assert "mongo_connected" in response.get_json()
