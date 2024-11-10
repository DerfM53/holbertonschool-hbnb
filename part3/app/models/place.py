#!/usr/bin/python3

"""
This module defines the Place model.
"""


from . import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity

class Place(BaseModel):
    """
    Represents a place class to creat place objects.
    """

    def __init__(self, title ,owner_id , description=None, latitude=0.0, price=0.0, longitude=0.0, amenities=None, reviews= None):
        super().__init__()
        self.owner_id = owner_id
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


    def place_to_dict(self):
        """Return a dictionary representation of the Place instance."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'reviews': [
            review.review_to_dict() if hasattr(review, 'review_to_dict') else review
            for review in self.reviews
            ],
            'amenities': [
            amenity.amenity_to_dict() if hasattr(amenity, 'amenity_to_dict') else amenity
            for amenity  in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    """  functions to handle types data """


def set_price(price):
    if isinstance(price, (int, float)) and price > 0:
        return price
    else:
        raise TypeError("price must be a number and superior to zero")

def set_latitude(valid):
    if isinstance(valid, (int, float)):
        if -90 <= valid  <= 90:
            return valid
    else:
        raise ValueError (" must be a number betwen -90 and 90")

def set_longitude(valid):
    if isinstance(valid, (int, float)):
        if -180 <= valid  <= 180:
            return valid
    else:
        raise ValueError (" must be a number betwen -90 and 90")
