from fastapi.testclient import TestClient
from app.main import app
from datetime import date

client = TestClient(app)

def setup_test_data():
    # Create a user and a book
    client.post("/users/", json={
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "is_active": True
    })
    client.post("/books/", json={
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "is_available": True
    })

def test_borrow_book():
    setup_test_data()
    response = client.post("/borrows/borrow", json={"user_id": 1, "book_id": 1})
    assert response.status_code == 200
    assert response.json()["borrow_date"] == str(date.today())

def test_return_book():
    setup_test_data()
    client.post("/borrows/borrow", json={"user_id": 1, "book_id": 1})
    response = client.post("/borrows/return", json={"record_id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Book returned successfully"

