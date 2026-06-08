
from fastapi.testclient import TestClient

from app.main import app


client = TestClient()

def test_health():
    response = client.get("/")

    assert response.status_code == 200


