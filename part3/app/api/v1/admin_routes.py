#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('admin', description='Admin operations')

# Modele pour creer nouveau users
user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name')
})

@api.route('/users')
class AdminUserManagement(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Create a new user (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        new_user_data = api.payload
        try:
            new_user = facade.create_user(new_user_data)
            return {'message': 'User created successfully', 'user_id': str(new_user.id)}, 201
        except Exception as e:
            return {'error': str(e)}, 400
