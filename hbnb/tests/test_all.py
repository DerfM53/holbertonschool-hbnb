from flask.testing import FlaskClient
import pytest
from flask import Flask, current_app
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

def test_create_user(client: FlaskClient):
    response = client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword"  # Ajoutez le mot de passe ici
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_login_and_get_user(client: FlaskClient):
    # Créer d'abord un utilisateur
    create_response = client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com",
        "password": "securepassword"
    })

    assert create_response.status_code == 201  # Vérifie que l'utilisateur a été créé avec succès

    user_in_repo = current_app.facade.user_repo.find_by_email("bob.johnson@example.com")
    assert user_in_repo is not None  # Assure-toi que l'utilisateur a bien été ajouté

    # Se connecter pour obtenir un token JWT
    login_response = client.post('/api/v1/users/login', json={
        "email": "bob.johnson@example.com",
        "password": "securepassword"
    })
    
    assert login_response.status_code == 200
    access_token = login_response.get_json()['access_token']
    
    # Utiliser le token pour obtenir les détails de l'utilisateur
    response = client.get('/api/v1/users/email/bob.johnson@example.com', headers={
        'Authorization': f'Bearer {access_token}'
    })
    
    assert response.status_code == 200
    assert response.get_json()['first_name'] == "Bob"

def test_get_user(client: FlaskClient):
    # Créer d'abord un utilisateur
    create_response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "password": "securepassword"  # Ajoutez le mot de passe ici
    })
    
    user_id = create_response.get_json()['id']
    
    # Se connecter pour obtenir un token JWT
    login_response = client.post('/api/v1/users/login', json={
        "email": "alice.smith@example.com",
        "password": "securepassword"
    })

    access_token = login_response.get_json()['access_token']

    # Utiliser le token pour obtenir les détails de l'utilisateur
    response = client.get(f'/api/v1/users/{user_id}', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert response.status_code == 200
    assert response.get_json()['first_name'] == 'Alice'

def test_delete_user(client: FlaskClient):
    # Créer d'abord un utilisateur
    create_response = client.post('/api/v1/users/', json={
        "first_name": "David",
        "last_name": "Smith",
        "email": "david.smith@example.com",
        "password": "securepassword"  # Ajoutez le mot de passe ici
    })
    
    user_id = create_response.get_json()['id']
    
    # Se connecter pour obtenir un token JWT
    login_response = client.post('/api/v1/users/login', json={
        "email": 'david.smith@example.com',
        'password': 'securepassword'
    })

    access_token = login_response.get_json()['access_token']

    # Supprimer l'utilisateur avec le token JWT
    delete_response = client.delete(f'/api/v1/users/{user_id}', headers={
        'Authorization': f'Bearer {access_token}'
    })

    assert delete_response.status_code == 200

def test_create_place(client: FlaskClient):
    # Créer d'abord un utilisateur
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "password": "securepassword"  # Ajoutez le mot de passe ici
    })
    
    user_id = user_response.get_json()['id']

    # Se connecter pour obtenir un token JWT
    login_response = client.post('/api/v1/users/login', json={
        "email": "jane.doe@example.com",
        "password": "securepassword"
    })

    access_token = login_response.get_json()['access_token']

    response = client.post('/api/v1/places/', headers={
        'Authorization': f'Bearer {access_token}'}, json={
        "title": "Cozy Apartment",
        "description": "A nice place to stay",
        "price": 100,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id
    })

    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_create_amenity(client: FlaskClient):
   response = client.post('/api/v1/amenities/', json={
       'name': 'Wi-Fi'
   })
   assert response.status_code == 201
   assert 'Amenity created successfully' in response.get_json()['message']

def test_update_user(client: FlaskClient):
   create_response = client.post('/api/v1/users/', json={
       'first_name': 'Charlie',
       'last_name': 'Brown',
       'email': 'charlie.brown@example.com',
       'password': 'securepassword'  # Ajoutez le mot de passe ici
   })
   user_id = create_response.get_json()['id']

   response = client.put(f'/api/v1/users/{user_id}', json={
       'first_name': 'Charles',
       'last_name': 'Brown',
       'email': 'charles.brown@example.com',
       'password': 'securepassword'  # Ajoutez le mot de passe ici
   })
   assert response.status_code == 200
   assert response.get_json()['first_name'] == 'Charles'

def test_create_place_with_invalid_data(client: FlaskClient):
    # Créer d'abord un utilisateur
    user_response = client.post('/api/v1/users/', json={
        'first_name': 'Invalid',
        'last_name': 'User',
        'email': 'invalid.user@example.com',
        'password': 'securepassword'
    })
    
    # Se connecter pour obtenir un token JWT
    login_response = client.post('/api/v1/users/login', json={
        "email": "invalid.user@example.com",
        "password": "securepassword"
    })
    
    access_token = login_response.get_json()['access_token']

    # Essayer de créer un lieu avec un titre vide (données invalides)
    response = client.post('/api/v1/places/', headers={'Authorization': f'Bearer {access_token}'}, json={
        'title': '',  # Titre vide pour simuler une erreur
        'description': 'A nice place to stay',
        'price': 100,
        'latitude': 37.7749,
        'longitude': -122.4194,
        'owner_id': user_response.get_json()['id']  # Utiliser l'ID de l'utilisateur créé
    })

    assert response.status_code == 400  # Vérifiez que le code d'état est 400 pour une mauvaise demande
    assert ('Your title must be non-empty and not exceed 100 characters' in 
            response.get_json()['error'])

def test_update_amenity(client: FlaskClient):
   # Créer d'abord un nouvel équipement
   response = client.post('/api/v1/amenities/', json={
       'name': 'Wi-Fi'
   })
   amenity_id = response.get_json()['data']['id']

   # Essayer de mettre à jour l'équipement avec des données valides
   update_response = client.put(f'/api/v1/amenities/{amenity_id}', json={
       'name': 'High-Speed Wi-Fi'
   })
   assert update_response.status_code == 200
   assert update_response.get_json()['name'] == 'High-Speed Wi-Fi'

   # Essayer de mettre à jour l'équipement avec des données invalides (nom vide)
   invalid_update_response = client.put(f'/api/v1/amenities/{amenity_id}', json={
       'name': ''
   })
   assert invalid_update_response.status_code == 400
   assert ('Your name must be non-empty' in 
           invalid_update_response.get_json()['error'])

def test_get_all_amenities(client: FlaskClient):
   # Essayer de récupérer la liste des équipements sans en avoir créé...
   response = client.get('/api/v1/amenities/')
   assert response.status_code == 404  # Vérifiez que le code d'état est 404 car aucun équipement n'existe.
   assert response.get_json()['message'] == 'No amenities found'

   # Créer quelques équipements.
   client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
   client.post('/api/v1/amenities/', json={'name': 'Pool'})

   # Récupérer à nouveau la liste des équipements.
   response = client.get('/api/v1/amenities/')
   assert response.status_code == 200  # Vérifiez que le code d'état est 200.
   
   amenities = response.get_json()
   
   assert len(amenities) == 2  # Assurez-vous qu'il y a deux équipements.
   
   assert amenities[0]['name'] == 'Wi-Fi'
   assert amenities[1]['name'] == 'Pool'

def test_delete_amenity(client: FlaskClient):
   # Créer d'abord un nouvel équipement.
   response = client.post('/api/v1/amenities/', json={'name': 'Wi-Fi'})
   
   amenity_id = response.get_json()['data']['id']

   # Supprimer l'équipement.
   delete_response = client.delete(f'/api/v1/amenities/{amenity_id}')
   
   assert delete_response.status_code == 200
   assert delete_response.get_json()['message'] == 'Amenity deleted successfully'

   # Vérifier que l'équipement n'existe plus.
   get_response = client.get(f'/api/v1/amenities/{amenity_id}')
   
   assert get_response.status_code == 404 
   assert get_response.get_json()['error'] == 'No amenity found'

def test_create_review(client: FlaskClient):
    # Créer d'abord un utilisateur.
    user_response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "password": "securepassword"
    })
    
    # Se connecter pour obtenir un token JWT.
    login_response = client.post('/api/v1/users/login', json={
        "email": "alice.smith@example.com",
        "password": "securepassword"
    })
    
    access_token = login_response.get_json()['access_token']

    # Créer d'abord une place.
    place_response = client.post('/api/v1/places/', headers={'Authorization': f'Bearer {access_token}'}, json={
        "title": "Lovely House",
        "description": "Perfect for families",
        "price": 150,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": user_response.get_json()['id'] 
    })

    place_id = place_response.get_json()['id']  # Assurez-vous que cela fonctionne maintenant

    # Créer un deuxième utilisateur.
    second_user_response = client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Johnson",
        "email": "bob.johnson@example.com",
        "password": "securepassword"
    })

    # Se connecter en tant que deuxième utilisateur pour obtenir un token JWT.
    second_login_response = client.post('/api/v1/users/login', json={
        "email": "bob.johnson@example.com",
        "password": "securepassword"
    })

    second_access_token = second_login_response.get_json()['access_token']

    # Essayer de créer une revue avec des données valides en utilisant le deuxième utilisateur.
    response = client.post('/api/v1/reviews/', headers={'Authorization': f'Bearer {second_access_token}'}, 
                        json={"text": "Great place to stay!",
                              "rating": 5,
                              "place_id": place_id})  # Utiliser le deuxième utilisateur

    assert response.status_code == 201 
    assert "id" in response.get_json()

    # Essayer de créer une revue avec des données invalides (texte vide).
    invalid_response = client.post('/api/v1/reviews/', headers={'Authorization': f'Bearer {second_access_token}'}, 
                                json={"text": "",
                                      "rating": 5,
                                      "place_id": place_id})

    assert invalid_response.status_code == 400 
    assert "Text cannot be empty" in invalid_response.get_json()['error']