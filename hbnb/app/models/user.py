#!/usr/bin/python3
from . import BaseModel
import re

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.place import Place
    from models.review import Review


class User(BaseModel):

    users = []

    role_user = 'user'
    role_admin = 'admin'
    role_owner = 'owner'

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = validate_len(first_name)
        self.last_name = validate_len(last_name)
        self.email = check_email(email)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []
        User.users.append(self)



    def add_places(self, place):
        """
        add places to user
    """
        if isinstance(place, Place):
            self.places.append(place)

    def add_reviews(self, review):
        """
            add reviews to user's place
         """
        if isinstance(review, Review):
            self.reviews.append(review)

    @classmethod
    def get_all_users(cls):
        """Retourne la liste de tous les utilisateurs sous forme de dictionnaire."""
        return cls.users


def user_to_dict(self):
    user_dict = super().to_dict()
    user_dict.update({'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
        'is_admin': self.is_admin,
        'places': [place.id for place in self.places],
        'reviews': [review.id for review in self.reviews],
    })
    return user_dict



def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
         return email
    else:
        raise TypeError("not valid email")

def validate_len(names):
    if not names:
        raise TypeError("Invalid input data")

    if not isinstance(names, str):
        raise TypeError("{names} is not a validate name")

    if not (3 <= len(names) <= 64):
        raise ValueError(f"{names} is too long or too short")
    return names

def valideate_passw(pw):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not pw:
        raise TypeError("must enter pass word")
    if isinstance(pw, str):
        raise TypeError("enter a valid pass word")
    if re.fullmatch(regex, pw):
         return pw
    else:
        raise TypeError("not valid pass word")

