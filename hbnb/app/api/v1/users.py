#!/usr/bin/python3

"""
This module handles API endpoints related to users.
It defines routes for creating and retrieving user information.
"""

from flask_restx import Namespace, Resource, fields
from flask import current_app
from flask_jwt_extended import create_access_token, jwt_required

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
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
    @jwt_required()
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
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update a user's information"""
        user_data = api.payload
        user = current_app.facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        # Utilisez la méthode update_user de votre façade
        updated_user = current_app.facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200
    
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        if current_app.facade.delete_user(user_id):
            return {'message': 'User deleted successfully'}, 200
        return {'error': 'User not found'}, 404
    
@api.route('/login')
class UserLogin(Resource):
    @api.expect(api.model('Login', {
        'email': fields.String(required=True, description='Email of the user'),
        'password': fields.String(required=True, description='Password of the user')
    }))
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Login a user and return a JWT token.
        
        Returns:
            tuple: A tuple containing the token and the HTTP status code.
        """
        data = api.payload
        email = data['email']
        password = data['password']

        user = current_app.facade.get_user_by_email(email)
        
        if user and user.check_password(password):  # Vérifiez le mot de passe avec la méthode check_password
            access_token = create_access_token(identity=user.id)  # Créez le token JWT avec l'ID de l'utilisateur
            return {'access_token': access_token}, 200
        
        return {'error': 'Invalid credentials'}, 401
    
# Nouvel endpoint pour récupérer un utilisateur par email
@api.route('/email/<string:email>')
class UserByEmail(Resource):
    
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, email):
        """
        Get user details by email.
        
        Args:
            email (str): The email of the user to retrieve.
        
        Returns:
            tuple: A tuple containing the user data and the HTTP status code.
        """
        user = current_app.facade.get_user_by_email(email)  # Assurez-vous que cette méthode existe dans votre façade
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200