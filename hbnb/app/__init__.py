from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.persistence.repository import InMemoryRepository
from app.services.facade import HBnBFacade

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    user_repo = InMemoryRepository()
    place_repo = InMemoryRepository()
    amenity_repo = InMemoryRepository()
    app.facade = HBnBFacade(user_repo, place_repo, amenity_repo)

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    return app