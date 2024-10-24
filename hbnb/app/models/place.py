#!/usr/bin/python3

from . import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, owner_id, price=0.0, latitude=0.0, longitude=0.0):
        super().__init__()
        self._title = None
        self.title = title
        self.description = description
        self._price = None
        self.price = price
        self._latitude = None
        self.latitude = latitude
        self._longitude = None
        self.longitude = longitude
        self._owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Your title must be non-empty and not exceed 100 characters")
        self._title = value.strip()

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0.0:
            raise ValueError("Your price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Please enter a valid latitude")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Please enter a valid longitude")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    @property
    def owner_id(self):
        return self._owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        self._owner_id = value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "amenities": self.amenities,
            "reviews": self.reviews,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def __str__(self):
        return f"Place: {self.title} (Owner: {self.owner.first_name} {self.owner.last_name})"

    