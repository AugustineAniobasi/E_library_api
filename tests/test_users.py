import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_get_user():
    # Ensure the user exists first
    test_create_user()
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

def test_deactivate_user():
    test_create_user()
    response = client.post("/users/1/deactivate")
    assert response.status_code == 200
    response = client.get("/users/1")
    assert response.json()["is_active"] is False

