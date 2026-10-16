import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_liveness(client):
    assert client.get("/health/live").status_code == 200

def test_readiness_failure_and_recovery(client):
    assert client.get("/health/ready").status_code == 200
    assert client.post("/simulate-failure").status_code == 202
    assert client.get("/health/ready").status_code == 503
    assert client.post("/recover").status_code == 200
    assert client.get("/health/ready").status_code == 200

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"demo_http_requests_total" in response.data
