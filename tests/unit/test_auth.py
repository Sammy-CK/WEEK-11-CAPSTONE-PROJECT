from fastapi.testclient import TestClient

from services.triage.app import app


def test_triage_requires_auth():
    client = TestClient(app)
    r = client.post("/triage", json={"message": "fever", "county": "Nairobi"})
    assert r.status_code == 401
