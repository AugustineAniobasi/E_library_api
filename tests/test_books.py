import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books/", json={
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "is_available": True
    })
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby"

def test_mark_book_unavailable():
    test_create_book()
    response = client.post("/books/1/mark_unavailable")
    assert response.status_code == 200
    response = client.get("/books/1")
    assert response.json()["is_available"] is False

