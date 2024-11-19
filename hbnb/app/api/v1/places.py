#!/usr/bin/python3

"""
This module handles API endpoints related to places.
It defines routes for creating, retrieving, and updating places.
"""

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import current_app

api = Namespace('places', description='Place operations')

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

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

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner details'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    """
    Resource for handling operations on the collection of places.
    """
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """
        Register a new place.
        """
        current_user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur authentifié
        place_data = api.payload
        place_data['owner_id'] = current_user_id  # Assigner l'ID de l'utilisateur comme propriétaire
        
        try:
            new_place = current_app.facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places.
        
        Returns:
            tuple: A tuple containing a list of places and the HTTP status code.
        """
        all_places = current_app.facade.get_all_places()
        if not all_places:
            return {'message': 'No amenities found'}, 404
        return [
            {
                "id": place.id,
                "title": place.title
            }
            for place in all_places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    """
    Resource for handling operations on individual places.
    """
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID.
        
        Args:
            place_id (str): The ID of the place to retrieve.
        
        Returns:
            tuple: A tuple containing the place data and the HTTP status code.
        """
        place = current_app.facade.get_place(place_id)
        if not place:
            return {'error': 'No place found'}, 404
        place_data = place.to_dict()
        place_data['reviews'] = [review.to_dict() for review in current_app.facade.get_reviews_by_place(place_id)]
        return place_data, 200

    @jwt_required()
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Update a place's information.
        """
        current_user_id = get_jwt_identity()
        current_user = current_app.facade.get_user(current_user_id)
        place = current_app.facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404
        
        if place.owner_id != current_user_id and not current_user.is_admin:  # Vérifier si l'utilisateur est le propriétaire
            return {'error': 'You do not have permission to update this place'}, 403
        
        place_data = api.payload
        updated_place = current_app.facade.update_place(place_id, place_data)
        return {
            'id': updated_place.id,
            'title': updated_place.title
        }, 200