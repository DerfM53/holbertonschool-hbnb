from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self, user_repo, place_repo, amenity_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.amenity_repo = amenity_repo

    def create_user(self, user_data):
        new_user = User(**user_data)
        self.user_repo.add(new_user)
        return new_user
    
    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user is None:
            print(f"User with ID {user_id} not found")  # Ajoutez ce log pour le débogage
        return user
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def create_amenity(self, amenity_data):
        if 'name' not in amenity_data:
            raise ValueError("Amenity name is required")
        new_amenity = Amenity(name=amenity_data['name'])
        if not hasattr(new_amenity, 'id') or new_amenity.id is None:
            raise ValueError("Amenity object does not have a valid ID")
        self.amenity_repo.add(new_amenity)
        return new_amenity
        
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"User with ID {owner_id} not found")
        new_place = Place(**place_data, owner_id=owner_id)
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)       