#!/usr/bin/python3

"""
This module handles API endpoints related to reviews.
It defines routes for creating, retrieving, updating, and deleting reviews.
"""
import traceback
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services import facade

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
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        #get user identy connected
        current_user = get_jwt_identity()
        review_data = api.payload
        #associate user_id ro the reviw_id
        review_data['user_id'] = current_user['id']
        current_place = facade.get_place(review_data['place_id'])
        if current_place is None:
            return {'message': 'place not found'}, 400
        print(f"Place owner_id: {current_place.owner_id}")
        if review_data['user_id'] != current_place.owner_id:
            try:
                review = facade.get_review_by_user(review_data['user_id'], review_data['place_id'])
                if review:
                    return {'message': 'You have already reviewed this place.'}, 400
                facade.create_review(review_data)
                return {'message': 'review added'},201
            except TypeError as e:
                traceback.print_exc()
                return ({"error": str(e)}), 400
        else:
            return {'message': 'You cannot review your own place.'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        if not all_reviews:
            return {'message': 'No review found'},404
        return [
            {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
            }
            for review in all_reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """
    Resource for handling operations on the collection of reviews.
    """

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')

    def get(self, review_id):
        """Get review details by ID"""

        review = facade.get_review(review_id)
        if not review:
            return {'message: Review not found'}
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
            }, 200


    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review_data = api.payload
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'review not found'}
        if review.user_id != current_user['id']:
            return {"error": "Unauthorized action."}, 403
        updated_review = facade.update_review(review_id, review_data)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
            }, 201


    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'review not found'}
        if review.user_id != current_user['id']:
            return {"error": "Unauthorized action."}, 403
        facade.delete_review(review_id)
        return {'message': 'review deleted , seccufuly!'},200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """
    Resource for handling operations on reviews for a specific place.
    """


    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews:
            return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ], 200
        else:
            return {'message': 'Place not found'}, 404

