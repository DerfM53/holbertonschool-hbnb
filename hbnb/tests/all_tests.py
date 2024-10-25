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

    def test_create_place_with_amenities(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
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

    def test_create_amenities(self):
        response = self.client.post('/api/v1/amenities/', json={"name": "wifi"})
        self.assertEqual(response.status_code, 201)
        self.assertIn('amenity added', response.get_json()['message'])

    def test_create_reviews(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 7,  # Note: This should ideally be between 1 and 5 for a valid test
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating must be a number betwen 1 and 5', response.get_json()['error'])

    def test_update_user(self):
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Lamine",
            "last_name": "Doe",
            "email": "lamine@example.com"
        })
        self.assertEqual(create_response.status_code, 201)
        user_id = create_response.get_json().get('id')


        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Jane Updated",
            "last_name": "Doe Updated",
            "email": "jane.doe_updated@example.com"
        })
        self.assertEqual(update_response.status_code, 200)
        updated_user = update_response.get_json()
        self.assertEqual(updated_user['first_name'], "Jane Updated")
        self.assertEqual(updated_user['last_name'], "Doe Updated")
        self.assertEqual(updated_user['email'], "jane.doe_updated@example.com")

    def test_delete_review(self):
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Another great stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(create_response.status_code, 201)
        review_id = create_response.get_json().get('id')


        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('review deleted , seccufuly!', delete_response.get_json()['message'])

    def test_update_review(self):
        # Création d'une review pour pouvoir la mettre à jour
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice stay!",
            "rating": 4,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(create_response.status_code, 201)
        review_id = create_response.get_json().get('id')

        # Mise à jour de la review
        update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('Review updated successfully', update_response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
