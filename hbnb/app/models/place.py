#!/usr/bin/python3
from . import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity

class Place(BaseModel):

    def __init__(self, title ,owner , description=None, latitude=0.0, price=0.0, longitude=0.0, amenities=None, reviews= None):
        super().__init__()
        self.owner = owner
        self.title = title
        self.description = description
        self.price = set_price(price)
        self.latitude = set_latitude(latitude)
        self.longitude = set_longitude(longitude)
        self.reviews = reviews if reviews is not None else []
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def set_owner(self, owner_id):
        from app.models.user import User  # Import dans le corps de la méthode
        return User(owner_id)

    def to_dict(self):
        """Return a dictionary representation of the Place instance."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict() if self.owner else None,
            'reviews': [review.to_dict() for review in self.reviews],
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        }

def validate_owner(owner):
    if not isinstance(owner, User):
        raise TypeError("Owner must be a valid User instance.")
    return owner

def set_price(price):
    if isinstance(price, float):
        if price >= 0:
            return price
    else:
        raise ((TypeError, ValueError)(" price must be a number and superior to zero"))

def set_latitude(valid):
    if isinstance(valid, (int, float)):
        if -90 <= valid  <= 90:
            return valid
    else:
        raise ((TypeError, ValueError)(" must be a number betwen -90 and 90"))

def set_longitude(valid):
    if isinstance(valid, (int, float)):
        if -180 <= valid  <= 180:
            return valid
    else:
        raise ((TypeError, ValueError)(" must be a number betwen -90 and 90"))


def get_by_id(user_id):
    user = User.users.get(user_id)


