from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self, user_repo, place_repo, amenity_repo, review_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.amenity_repo = amenity_repo
        self.review_repo = review_repo

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
    
    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)

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

    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found")
        if not 1 <= review_data['rating'] <= 5:
            raise ValueError("Rating must be between 1 and 5")
    
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
    
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
    
        if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")
    
        review.update(review_data)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return True