#!/usr/bin/python3

"""
This module handles API endpoints related to reviews.
It defines routes for creating, retrieving, updating, and deleting reviews.
"""

from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    """
    Resource for handling operations on the collection of reviews.
    """
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review."""
        data = api.payload
        print(f"Payload received for review creation: {data}")  # Log pour débogage
        current_user_id = get_jwt_identity()  # Récupérer l'ID de l'utilisateur authentifié

        # Récupérer l'ID de l'utilisateur authentifié
        print(f"Current user ID: {current_user_id}")  # Log pour débogage
        # Ajout d'un log pour déboguer les données reçues
        print(f"Data received for review creation: {data}")  # Log pour débogage
        
        # Validation pour le texte de la revue
        if not data.get('text'):
            return {'error': 'Text cannot be empty'}, 400
        
        # Vérifier si l'utilisateur essaie de laisser un avis sur un lieu qu'il possède
        place = current_app.facade.get_place(data['place_id'])
        print(f"Place retrieved: {place}")  # Log pour débogage
        if place and place.owner_id == current_user_id:
            return {'error': "You cannot review your own place"}, 403
        
        try:
            data['user_id'] = current_user_id  # Assigner l'ID de l'utilisateur comme auteur de la revue
            review = current_app.facade.create_review(data)
            response_data = review.to_dict()
            print(f"Review created: {response_data}")  # Log pour débogage
            return response_data, 201
        except ValueError as e:
            print(f"Error creating review: {str(e)}")  # Log pour débogage
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.
        
        Returns:
            tuple: A tuple containing a list of reviews and the HTTP status code.
        """
        reviews = current_app.facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource for handling operations on individual reviews.
    """
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.
        
        Args:
            review_id (str): The ID of the review to retrieve.
        
        Returns:
            tuple: A tuple containing the review data and the HTTP status code.
        """
        review = current_app.facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """
        Update a review's information.
        
        Args:
            review_id (str): The ID of the review to update.
        
        Returns:
            tuple: A tuple containing a success message and the HTTP status code.
        """
        data = api.payload
        try:
            current_app.facade.update_review(review_id, data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id (str): The ID of the review to delete.
        
        Returns:
            tuple: A tuple containing a success message and the HTTP status code.
        """
        if current_app.facade.delete_review(review_id):
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource for handling operations on reviews for a specific place.
    """
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.
        
        Args:
            place_id (str): The ID of the place to get reviews for.
        
        Returns:
            tuple: A tuple containing a list of reviews and the HTTP status code.
        """
        reviews = current_app.facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'message': 'Place not found'}, 404
        return [review.to_dict() for review in reviews], 200
