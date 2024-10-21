#!/usr/bin/python3
from . import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity

class Place(BaseModel):

    def __init__(self, title ,owner_id , description=None, latitude=0.0, price=0.0, longitude=0.0):
        super().__init__()
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.price = set_price(price)
        self.latitude = set_latitude(latitude)
        self.longitude = set_longitude(longitude)
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)


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

