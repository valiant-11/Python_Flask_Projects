import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from server import app, db, BusinessCard

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_get_empty_cards(client):
    response = client.get("/api/cards")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_card(client):
    new_card = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "123456789",
        "company": "TestCo",
        "job_title": "Tester"
    }
    response = client.post("/api/cards", json=new_card)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert "id" in data

def test_get_card_by_id(client):
    # First create one
    new_card = {
        "name": "Another Test",
        "email": "another@example.com",
        "phone": "555-5555",
        "company": "ABC",
        "job_title": "Dev"
    }
    post = client.post("/api/cards", json=new_card)
    card_id = post.get_json()["id"]

    # Then fetch it
    get = client.get(f"/api/cards/{card_id}")
    assert get.status_code == 200
    assert get.get_json()["email"] == "another@example.com"

def test_update_card(client):
    # Create
    response = client.post("/api/cards", json={
        "name": "To Update",
        "email": "old@mail.com",
        "phone": "111",
        "company": "OldCo",
        "job_title": "OldJob"
    })
    card_id = response.get_json()["id"]

    # Update
    update = client.put(f"/api/cards/{card_id}", json={"email": "new@mail.com"})
    assert update.status_code == 200
    assert update.get_json()["email"] == "new@mail.com"

def test_delete_card(client):
    # Create
    response = client.post("/api/cards", json={
        "name": "To Delete",
        "email": "delete@mail.com",
        "phone": "999",
        "company": "DeleteCo",
        "job_title": "DeleteJob"
    })
    card_id = response.get_json()["id"]

    # Delete
    delete = client.delete(f"/api/cards/{card_id}")
    assert delete.status_code == 200
    assert delete.get_json()["message"] == "Card deleted"

    # Confirm it's gone
    get = client.get(f"/api/cards/{card_id}")
    assert get.status_code == 404
