import pytest
from flask import Flask
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_create_place(client):
    # Créer d'abord un utilisateur
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })
    user_id = user_response.get_json()['id']

    response = client.post('/api/v1/places/', json={
        "title": "Cozy Apartment",
        "description": "A nice place to stay",
        "price": 100,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_create_review(client):
    # Créer un utilisateur et une place d'abord
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    user_id = user_response.get_json()['id']

    place_response = client.post('/api/v1/places/', json={
        "title": "Lovely House",
        "description": "Perfect for families",
        "price": 150,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user_id
    })
    place_id = place_response.get_json()['id']

    response = client.post('/api/v1/reviews/', json={
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_create_amenity(client):
    response = client.post('/api/v1/amenities/', json={
        "name": "Wi-Fi"
    })
    assert response.status_code == 201
    assert "Amenity created successfully" in response.get_json()['message']

def test_get_user(client):
    # Créer d'abord un utilisateur
    create_response = client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com"
    })
    user_id = create_response.get_json()['id']

    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    assert response.get_json()['first_name'] == "Bob"
    assert response.get_json()['last_name'] == "Johnson"

# Ajoutez d'autres tests selon vos besoins...