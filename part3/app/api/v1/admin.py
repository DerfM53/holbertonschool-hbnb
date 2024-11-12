from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('admin', description='Admin operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='Admin privileges')
})

@api.route('/users')
class AdminUserCreate(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        """Get all users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404
        return [user.user_to_dict() for user in users], 200

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {'id': new_user.id,
                "message": "User created successfully"}, 201


@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')

        if email:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

            updated_user = facade.update_user(user_id, data)
            return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'created_at': updated_user.created_at.isoformat(),
            'updated_at': updated_user.updated_at.isoformat()
            }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id,
                "message": "amenity created successfully"}, 201


    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        amenities = facade.get_all_amenities()
        if not amenities:
            return {'message': 'No ameneties found'}, 404
        return [amenity.amenity_to_dict() for amenity in amenities], 200


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def get(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'No amenety found'}, 404
        return amenity.amenity_to_dict(), 200


    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json
        id = amenity_data.get('id')
        existing_amenity = facade.get_amenity(id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            "created_at": updated_amenity.created_at.isoformat(),
            "updated_at": updated_amenity.updated_at.isoformat()
        }, 201


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {"error": 'place not found'}
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        place_data = request.json
        updated_place = facade.update_place(place_id, place_data)
        return {
            'id': updated_place.id,
                    'description': updated_place.description,
        'price': updated_place.price,
        'latitude': updated_place.latitude,
        'longitude': updated_place.longitude,
        'owner_id': updated_place.owner_id,
        'created_at': updated_place.created_at.isoformat(),
        'updated_at': updated_place.updated_at.isoformat()
        }, 200

    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        place = facade.get_place(place_id)
        if not place:
            return {"error": 'place not found'}
        if not is_admin and place.owner_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        facade.delete_place(place_id)
        return {"message": "place deleted"}, 200


@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @jwt_required
    def put(self, review_id):
        current_user = get_jwt_identity()

        # Set is_admin default to False if not exists
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')


        review = facade.get_review(review_id)
        if not review:
            return {"error": "review not found"}, 400
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        review_data = request.json
        updated_review = facade.update_review(review_id, review_data)
        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
            }, 201

    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        user_id = current_user.get('id')

        review = facade.get_review(review_id)
        if not review:
            return {"error": "review not found"}, 400
        if not is_admin and review.user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'review deleted , seccufuly!'},200

