#!/usr/bin/python3

"""
This module handles API endpoints related to amenities.
It defines routes for creating, retrieving, and updating amenities.
"""


from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import current_app

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Resource for handling operations on the collection of amenities.
    """
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.
        
        Returns:
            tuple: A tuple containing a dictionary with the created amenity data and the HTTP status code.
        """
        try:
            new_amenity = current_app.facade.create_amenity(api.payload)
            return {"message": "Amenity created successfully", "data": new_amenity.to_dict()}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "An unexpected error occurred"}, 500
        
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.
        
        Returns:
            tuple: A tuple containing a list of amenities and the HTTP status code.
        """
        all_amenities = current_app.facade.get_all_amenities()
        if not all_amenities:
            return {'message': 'No amenities found'}, 404
        return [
            {
                "id": amenity.id,
                "name": amenity.name
            }
            for amenity in all_amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource for handling operations on individual amenities.
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.
        
        Args:
            amenity_id (str): The ID of the amenity to retrieve.
        
        Returns:
            tuple: A tuple containing the amenity data and the HTTP status code.
        """
        amenity = current_app.facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'No amenity found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        amenity = current_app.facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        # Validation pour le champ name
        if 'name' in amenity_data and (not amenity_data['name'] or len(amenity_data['name']) > 100):
            return {'error': "Your name must be non-empty and not exceed 100 characters"}, 400

        updated_amenity = current_app.facade.update_amenity(amenity_id, amenity_data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity"""
        if current_app.facade.delete_amenity(amenity_id):
            return {'message': 'Amenity deleted successfully'}, 200
        return {'error': 'Amenity not found'}, 404