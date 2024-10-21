#!/usr/bin/python3
from typing import TYPE_CHECKING
from . import BaseModel
import uuid

if TYPE_CHECKING:
    from models.user import User  # Import différé uniquement pour l'annotation de type

    from models.place import Place


class Review(BaseModel):

    def __init__(self, text, place, user, rating=0,):
        super().__init__()
        self.place = place
        self.user = user

        self.text = text
        self.rating = rating

def check_User(self, author):
    if not isinstance(author, User):
        raise TypeError("author must be a valid user instance")
    return (author)


def check_owner(self, owner):
    if not isinstance(owner, User):
        raise TypeError("Owner must be a valid user instance")



