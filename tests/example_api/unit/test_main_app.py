from fastapi.testclient import TestClient
from example_api.excepts import OkStatus
from example_api.main import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
