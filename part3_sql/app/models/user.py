#!/usr/bin/python3

"""
This module defines the User model.
"""
from sqlalchemy.orm import validates, relationship
from app.extensions import db
from . import BaseModel
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.place import Place
    from models.review import Review



    """
    class user to creat user object
    """



class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship('Place', back_populates='owner' )
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    def mask_password(self):
        return '*' * len(self.password)


    @validates("password")
    def validate_password(self, key, pw):
        # virify charachtérs
        regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

        if not pw:
            raise TypeError("Must enter a password")

        if not isinstance(pw, str):
            raise TypeError("Password must be a valid string")

        match =re.fullmatch(regex, pw)
        if not match:
            raise TypeError("Password is not valid. It must be at least "
                     "8 characters long and contain both letters and numbers")
        return pw

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


    """
    functions to handle data type input
    """
    @validates("email")
    def check_email(self, key, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return email
        else:
            raise TypeError("not valid email")

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise TypeError("Invalid input name")

        if not isinstance(first_name, str):
            raise TypeError(f"{first_name} is not a validate name")

        if not (3 <= len(first_name) <= 64):
            raise ValueError(f"{first_name} is too long or too short")
        return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise TypeError("Invalid input name")

        if not isinstance(last_name, str):
            raise TypeError(f"{last_name} is not a validate name")

        if not (3 <= len(last_name) <= 64):
            raise ValueError(f"{last_name} is too long or too short")
        return last_name

#check the pass word lenth and charachters requirement

    def validate_password(self, pw):
        regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

        if not pw:
            raise TypeError("Must enter a password")

        if not isinstance(pw, str):
            raise TypeError("Password must be a valid string")

        match =re.fullmatch(regex, pw)
        print("Regex match result:", bool(match))
        if match:
            return pw
        else:
            raise ValueError("Password is not valid. It must be at least "
                     "8 characters long and contain both letters and numbers")

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
        'password': self.mask_password()
    }
