#!/usr/bin/python3

"""
This module handles API endpoints related to users.
It defines routes for creating and retrieving user information.
"""


from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import jsonify
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    """
    Resource for handling operations on the collection of users.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            facade.create_user(user_data)
            return {"message": "User created successfully"}, 201
        except TypeError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Invalid input data"}, 500

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get all users"""

        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404
        return [user.user_to_dict() for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for handling operations on individual users.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.user_to_dict(), 201


    @api.expect(user_model, validate=True)
    @api.response(200, 'update is done')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        user_data = api.payload
        user_exists = facade.get_user(user_id)

        if not user_exists:
            return {'error': 'User not found'}, 404

        updated_user = facade.update_user(user_id, user_data)

        return {
        'id': updated_user.id,
        'first_name': updated_user.first_name,
        'last_name': updated_user.last_name,
        'email': updated_user.email,
        'created_at': updated_user.created_at.isoformat(),
        'updated_at': updated_user.updated_at.isoformat()
        }, 200