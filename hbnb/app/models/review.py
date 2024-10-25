#!/bin/usr/python3

"""
This module defines the Review model.
"""

from . import BaseModel

class Review(BaseModel):
    """
    Represents a review in the application.
    """
    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): The text content of the review.
            rating (int): The rating given in the review.
            place_id (str): The ID of the place being reviewed.
            user_id (str): The ID of the user who wrote the review.
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        """
        Convert the Review instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Review.
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
       