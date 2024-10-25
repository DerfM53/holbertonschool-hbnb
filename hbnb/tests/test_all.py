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

def test_update_user(client):
    create_response = client.post('/api/v1/users/', json={
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie.brown@example.com"
    })
    user_id = create_response.get_json()['id']

    response = client.put(f'/api/v1/users/{user_id}', json={
        "first_name": "Charles",
        "last_name": "Brown",
        "email": "charles.brown@example.com"
    })
    assert response.status_code == 200
    assert response.get_json()['first_name'] == "Charles"

def test_delete_user(client):
    # Créer d'abord un utilisateur
    create_response = client.post('/api/v1/users/', json={
        "first_name": "David",
        "last_name": "Smith",
        "email": "david.smith@example.com"
    })
    user_id = create_response.get_json()['id']

    # Supprimer l'utilisateur
    delete_response = client.delete(f'/api/v1/users/{user_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json()['message'] == 'User deleted successfully'

    # Vérifier que l'utilisateur n'existe plus
    get_response = client.get(f'/api/v1/users/{user_id}')
    assert get_response.status_code == 404

def test_create_place_with_invalid_data(client):
    # Créer d'abord un utilisateur
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Invalid",
        "last_name": "User",
        "email": "invalid.user@example.com"
    })
    user_id = user_response.get_json()['id']

    # Essayer de créer un lieu avec un titre vide (données invalides)
    response = client.post('/api/v1/places/', json={
        "title": "",  # Titre vide pour simuler une erreur
        "description": "A nice place to stay",
        "price": 100,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id
    })
    
    assert response.status_code == 400  # Vérifiez que le code d'état est 400 pour une mauvaise demande
    assert "Your title must be non-empty and not exceed 100 characters" in response.get_json()['error']

def test_update_amenity(client):
    # Créer d'abord un nouvel équipement
    response = client.post('/api/v1/amenities/', json={
        "name": "Wi-Fi"
    })
    amenity_id = response.get_json()['data']['id']

    # Essayer de mettre à jour l'équipement avec des données valides
    update_response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        "name": "High-Speed Wi-Fi"
    })
    assert update_response.status_code == 200
    assert update_response.get_json()['name'] == "High-Speed Wi-Fi"

    # Essayer de mettre à jour l'équipement avec des données invalides (nom vide)
    invalid_update_response = client.put(f'/api/v1/amenities/{amenity_id}', json={
        "name": ""
    })
    assert invalid_update_response.status_code == 400
    assert "Your name must be non-empty" in invalid_update_response.get_json()['error']

def test_get_all_amenities(client):
    # Essayer de récupérer la liste des équipements sans en avoir créé
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 404  # Vérifiez que le code d'état est 404 car aucun équipement n'existe
    assert response.get_json()['message'] == 'No amenities found'

    # Créer quelques équipements
    client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    client.post('/api/v1/amenities/', json={"name": "Pool"})

    # Récupérer à nouveau la liste des équipements
    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200  # Vérifiez que le code d'état est 200
    amenities = response.get_json()
    assert len(amenities) == 2  # Assurez-vous qu'il y a deux équipements
    assert amenities[0]['name'] == "Wi-Fi"
    assert amenities[1]['name'] == "Pool"

def test_delete_amenity(client):
    # Créer d'abord un nouvel équipement
    response = client.post('/api/v1/amenities/', json={
        "name": "Wi-Fi"
    })
    amenity_id = response.get_json()['data']['id']

    # Supprimer l'équipement
    delete_response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json()['message'] == 'Amenity deleted successfully'

    # Vérifier que l'équipement n'existe plus
    get_response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert get_response.status_code == 404
    assert get_response.get_json()['error'] == 'No amenity found'

def test_create_review(client):
    # Créer d'abord un utilisateur
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    user_id = user_response.get_json()['id']

    # Créer d'abord un lieu
    place_response = client.post('/api/v1/places/', json={
        "title": "Lovely House",
        "description": "Perfect for families",
        "price": 150,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user_id
    })
    place_id = place_response.get_json()['id']

    # Essayer de créer une revue avec des données valides
    response = client.post('/api/v1/reviews/', json={
        "text": "Great place to stay!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

    # Essayer de créer une revue avec des données invalides (texte vide)
    invalid_response = client.post('/api/v1/reviews/', json={
        "text": "",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    })
    assert invalid_response.status_code == 400
    assert "Text cannot be empty" in invalid_response.get_json()['error']

# Ajoutez d'autres tests selon vos besoins...