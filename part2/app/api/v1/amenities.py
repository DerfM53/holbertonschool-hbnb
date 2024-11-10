#!/usr/bin/python3

"""
This module handles API endpoints related to amenities.
It defines routes for creating, retrieving, and updating amenities.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services import facade
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})



@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):
        """Register a new amenity"""

        amenity_data = api.payload
        existing_amenity = facade.get_amenity(amenity_data['name'])
        if existing_amenity:
            return {'error': 'amenity already exists'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {'message': 'amenity added'}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """ get all the aminities created """

        all_amenities = facade.get_all_amenities()
        if not all_amenities:
            return {'message': 'No ameneties found'}, 404
        return [amenity.amenity_to_dict() for amenity in all_amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
        Resource for handling operations on individual amenities.
    """

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'No amenity found'}, 404
        return amenity.amenity_to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')

    def put(self, amenity_id):
        """Update an amenity's information"""

        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name,
            "created_at": amenity.created_at.isoformat(),
            "updated_at": amenity.updated_at.isoformat()
        }, 201
