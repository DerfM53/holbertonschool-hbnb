import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_json()['message'])

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid input data', response.get_json()['error'])


    def test_creat_place_with_aminities(self):
        # it will creat a imptyt list of reviews even if you dont pass it
        response = self.client.post('/api/v1/places/', json={
        "title": "Cozy Apartment",
        "description": "A nice place to stay",
        "price":100,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
        },
        "amenities": [
        {
        "id": "4fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Wi-Fi"
        },
        {
        "id": "5fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Air Conditioning"
        }
        ]
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('place created successufully', response.get_json()['message'])

    def test_creat_aminities(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "wifi"})

        self.assertEqual(response.status_code, 201)
        self.assertIn('amenity added', response.get_json()['message'])

    def test_creat_reviews(self):
        response = self.client.post('/api/v1/reviews/', json={
        "text": "Great place to stay!",
        "rating": 7,
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating must be a number betwen 1 and 5', response.get_json()['error'])

    def test_update_user(self):
        # Création d'un utilisateur
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "lamine",
            "last_name": "Doe",
            "email": "lamine@example.com"
        })
        self.assertEqual(create_response.status_code, 201)
        user_id = create_response.get_json().get('id')
        self.assertIsNotNone(user_id)

        # Mise à jour de l'utilisateur
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Jane Updated",
            "last_name": "Doe Updated",
            "email": "jane.doe_updated@example.com"
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('update is done', update_response.get_json()['message'])



