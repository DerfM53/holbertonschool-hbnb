import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')  # Assure-toi que cette méthode existe et prend un argument
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {'message': 'amenity added'})

    def test_create_existing_amenity(self):
        # Crée d'abord l'amenity
        self.client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Swimming Pool'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {'error': 'amenity already exists'})

    def test_get_all_amenities(self):
        self.client.post('/api/v1/amenities/', json={'name': 'Gym'})
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIn({'name': 'Gym'}, response.get_json())

    def test_get_amenity_by_id(self):
        create_response = self.client.post('/api/v1/amenities/', json={'name': 'Spa'})
        amenity_id = create_response.get_json()['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Spa')

    def test_get_non_existing_amenity(self):
        response = self.client.get('/api/v1/amenities/999')  # Un ID qui n'existe pas
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'No amenity found'})

    def test_update_amenity(self):
        create_response = self.client.post('/api/v1/amenities/', json={'name': 'Sauna'})
        amenity_id = create_response.get_json()['id']
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={'name': 'Updated Sauna'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Updated Sauna')

    def test_update_non_existing_amenity(self):
        response = self.client.put('/api/v1/amenities/999', json={'name': 'Non-existing'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {'error': 'Amenity not found'})

if __name__ == '__main__':
    unittest.main()

