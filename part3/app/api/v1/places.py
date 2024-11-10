#!/usr/bin/python3
"""
This module handles API endpoints related to places.
It defines routes for creating, retrieving, and updating places.
"""


from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import current_app
from app.services import facade


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})



@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')

    def post(self):
        """Register a new place"""
        place_data = api.payload
        existing_place = facade.get_place_by_attributes(
            title=place_data['title'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude']
        )
        if existing_place:
            return {'error': 'place already exists'}, 400

        # Creat new place, associating owner_id to current user
        facade.create_place(place_data)

        return {'message': 'place created successufully'}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if not places:
            return {'message': 'No place found'}, 400

        return [ place.place_to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource for handling operations on the collection of places.
    """

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}

        return place.place_to_dict()


    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        place_exists = facade.get_place(place_id)

        if not place_exists:
            return {'error': 'place not found'}, 404

        updated_place = facade.update_place(place_id, place_data)

        return {
        'title': updated_place.title,
        'description': updated_place.description,
        'latitude': updated_place.latitude,
        'longitude': updated_place.longitude,
        'owner_id': updated_place.owner_id,
        'created_at': updated_place.created_at.isoformat(),
        'updated_at': updated_place.updated_at.isoformat()
    }, 200

@api.route('/user/<user_id>/places')
class UserPlacesResource(Resource):


    @api.response(200, 'Places retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """get all places of a user by user_id"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        places = facade.get_places_by_user(user_id)
        if not places:
            return {'message': 'No places found for this user'}, 200

        return [{'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': facade.get_user(place.owner_id)}
                for place in places], 200
