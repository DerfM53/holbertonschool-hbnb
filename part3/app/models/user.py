#!/usr/bin/python3

"""
This module defines the User model.
"""

from . import BaseModel
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.place import Place
    from models.review import Review


class User(BaseModel):
    """
    class user to creat user object
    """

    places = []

    role_user = 'user'
    role_admin = 'admin'
    role_owner = 'owner'

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = validate_len(first_name)
        self.last_name = validate_len(last_name)
        self.email = check_email(email)
        self.is_admin = is_admin
        validate = valideate_passw(password)
        print("Validating password:", validate)
        self.password = self.hash_password(validate)

    def hash_password(self, password):
        from app import bcrypt
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        return self.password

    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    def user_to_dict(self):
        return {
        'id': self.id,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'email': self.email,
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat(),
        'password': self.password
    }

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

"""
functions to handle data type input
"""

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
         return email
    else:
        raise TypeError("not valid email")

def validate_len(names):
    if not names:
        raise TypeError("Invalid input name")

    if not isinstance(names, str):
        raise TypeError("{names} is not a validate name")

    if not (3 <= len(names) <= 64):
        raise ValueError(f"{names} is too long or too short")
    return names

#check the pass word lenth and charachters requirement
def valideate_passw(pw):

    if not pw:
        raise TypeError("Must enter a password")

    if not isinstance(pw, str):
        raise TypeError("Password must be a valid string")

    regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
    if re.fullmatch(regex, pw):
        return pw
    else:
        raise TypeError("Password is not valid. It must be at least"
                         "8 characters long and contain both letters and numbers")

def verify_password(self, password):
    from app import bcrypt
    """Verifies if the provided password matches the hashed password."""
    return bcrypt.check_password_hash(self.password, password)
