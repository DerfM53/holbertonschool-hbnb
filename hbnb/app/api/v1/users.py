#!/usr/bin/python3

"""
This module handles API endpoints related to users.
It defines routes for creating and retrieving user information.
"""

from flask_restx import Namespace, Resource, fields
from flask import current_app

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
        """
        Register a new user.
        
        Returns:
            tuple: A tuple containing the created user data and the HTTP status code.
        """
        try:
            new_user = current_app.facade.create_user(api.payload)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "An unexpected error occurred"}, 500

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for handling operations on individual users.
    """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.
        
        Args:
            user_id (str): The ID of the user to retrieve.
        
        Returns:
            tuple: A tuple containing the user data and the HTTP status code.
        """
        user = current_app.facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200