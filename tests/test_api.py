from fastapi.testclient import TestClient
from core.api import app

client = TestClient(app)

def test_analyze_py_endpoint():
    resp = client.post("/analyze", json={"lang": "py", "code": "def f():\n  pass"})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("success") is True
