#!/usr/bin/python3
from typing import TYPE_CHECKING
from . import BaseModel
import uuid

if TYPE_CHECKING:
    from models.user import User  # Import différé uniquement pour l'annotation de type

    from models.place import Place


class Review(BaseModel):

    def __init__(self, text, place_id, user_id, rating=0,):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id

        self.text = text
        self.rating = rating


    def to_dict(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text,
            'rating': self.rating
        }

def check_User(author):
    if not isinstance(author, User):
        raise TypeError("author must be a valid user instance")
    return (author)


def check_owner(self, owner):
    if not isinstance(owner, User):
        raise TypeError("Owner must be a valid user instance")



