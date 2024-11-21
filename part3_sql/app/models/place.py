#!/usr/bin/python3

"""
This module defines the Place model.
"""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates, relationship
from app.extensions import db
from . import BaseModel
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.review import Review
    from models.amenity import Amenity

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
     )

class Place(BaseModel):
    """
    Represents a place class to creat place objects.
    """
    __tablename__ = 'places'

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'),nullable=False)

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    reviews = db.relationship('Review', back_populates='place', cascade="all, delete-orphan", lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places', lazy=True)
        #self.reviews = reviews if reviews is not None else []
        #self.amenities = amenities if amenities is not None else []
    owner = db.relationship('User', back_populates='places', lazy=True)

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
            for review in (self.reviews or [])
            ],
            'amenities': [
            amenity.amenity_to_dict() if hasattr(amenity, 'amenity_to_dict') else amenity
            for amenity  in (self.amenities or [])],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    """  functions to handle types data """

    @validates("price")
    def set_price(self, key, price):
        if isinstance(price, (int, float)) and price > 0:
            return price
        else:
            raise TypeError("price must be a number and superior to zero")

    @validates("latitude")
    def set_latitude(self, key, valid):
        if isinstance(valid, (int, float)):
            if -90 <= valid  <= 90:
                return valid
        else:
            raise ValueError (" must be a number betwen -90 and 90")

    @validates("longitude")
    def set_longitude(self, key, valid):
        if isinstance(valid, (int, float)):
            if -180 <= valid  <= 180:
                return valid
        else:
            raise ValueError (" must be a number betwen -90 and 90")
