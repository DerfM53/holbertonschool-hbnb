#!/usr/bin/python3

"""
This module defines the review model.
"""
from sqlalchemy.orm import validates
from app.extensions import db
from typing import TYPE_CHECKING
from . import BaseModel
import uuid

if TYPE_CHECKING:
    from models.user import User  # Import différé uniquement pour l'annotation de type

    from models.place import Place


class Review(BaseModel):
    """
    class review to creat review objects
    """
    __tablename__ = "reviews"
        #self.place_id = place_id
        #self.user_id = user_id

    text = db.Column(db.String(180), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    def review_to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


    @validates("rating")
    def check_rating(self, key, rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise TypeError ("rating must be a number betwen 1 and 5")
        return rating
