from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_recommendations_success():
    payload = {"userId": "user123", "actions": ["gmail", "calendar", "drive"]}
    headers = {"X-API-Version": "v1"}
    response = client.post("/recommendations", json=payload, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 3
    assert data["modelVersion"] == "dummy"
    assert "requestId" in data


def test_get_recommendations_invalid_version():
    payload = {"userId": "user123", "actions": ["gmail", "calendar", "drive"]}
    headers = {"X-API-Version": "v2"}
    response = client.post("/recommendations", json=payload, headers=headers)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid API version"


def test_get_recommendations_validation_error():
    payload = {"userId": "user123", "actions": ["one"]}  # min 3 items required
    headers = {"X-API-Version": "v1"}
    response = client.post("/recommendations", json=payload, headers=headers)

    assert response.status_code == 422
