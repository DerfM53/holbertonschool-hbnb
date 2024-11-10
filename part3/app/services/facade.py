from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#============================================
#handling user facade

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        return user


    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()


    def update_user(self, user_id, user_data):
        """updated a user."""
        user = self.user_repo.get(user_id)
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        self.user_repo.update(user_id, user_data)
        return user



#===============================================
#handling amenities facade
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all    ()

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
        self.amenity_repo.update( amenity_id, amenity_data)
        amenity_updated = self.amenity_repo.get(amenity_id)
        return amenity_updated

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

#===================================================
#handling place facade

    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')

        place = Place(**place_data, owner_id=owner_id)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

# fuctions to update places

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return None  # Ou tu peux lever une exception si tu préfères

        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']
        if 'owner_id' in place_data:
            place.owner_id = place_data['owner_id']

        self.place_repo.update(place_id, place_data)

        return place

    def get_places_by_user(self, user_id):
        return [place for place in self.place_repo.get_all() if place.owner_id == user_id]

    def get_place_by_attributes(self, title, latitude, longitude):
        places = self.place_repo.get_all()
        for place in places:
            if place.title == title and place.latitude == latitude and place.longitude == longitude:
                return place
        return None

 #======================================================
#handling reviews facade

    def create_review(self, review_data):
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        user = self.get_user(user_id)
        place = self.get_place(place_id)

        review = Review(**review_data, place_id=place_id, user_id=user_id)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):

        place = self.place_repo.get(place_id)
        if not place:
            return None
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]


    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        self.review_repo.update(review_id, review_data)
        review_updated = self.review_repo.get(review_id)
        return review_updated

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
