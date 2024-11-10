#!/usr/bin/python3

"""
This module defines the review model.
"""

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

    def __init__(self, text, place_id, user_id, rating=0,):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id

        self.text = text
        self.rating = check_rating(rating)


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



def check_rating(rating):
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        raise TypeError ("rating must be a number betwen 1 and 5")
    return rating
