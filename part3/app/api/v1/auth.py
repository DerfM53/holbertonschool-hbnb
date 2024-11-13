from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        print(user.email)

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user["id"]}'}, 200

def verify_password(password):
    from app import bcrypt
    """ check password """
    return bcrypt.check_password_hash('password', password)


def verify_password(password):
    from app import bcrypt
    """ check password """
    return bcrypt.check_password_hash('password', password)



user_model = api.model('User', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name')
})

@api.route('/admin/users')
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

@api.route('/admin/users/<user_id>')
class AdminUserModification(Resource):
    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id):
        """Modify a user's details (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        update_data = api.payload
        try:
            updated_user = facade.update_user(user_id, update_data)
            return {'message': 'User updated successfully', 'user': updated_user.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/admin/users/<user_id>')
class AdminUserModification(Resource):


    @jwt_required()
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        if facade.delete_user(user_id):
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404

@api.route('/admin/users/<user_id>')
class AdminUserModification(Resource):
    @jwt_required()
    def get(self, user_id):
        """Get user details (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if user:
            return user.to_dict(), 200
        else:
            return {'error': 'User not found'}, 404

@api.route('/admin/users')
class AdminUserManagement(Resource):
    @jwt_required()
    def get(self):
        """va list tout les users en admin"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200


