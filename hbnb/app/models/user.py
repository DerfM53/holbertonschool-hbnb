#!/usr/bin/python3

"""
This module defines the User model.
"""

from flask_bcrypt import generate_password_hash, check_password_hash
from . import BaseModel
import re
import uuid

class User(BaseModel):
    """
    Represents a user in the application.
    """
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


    def __init__(self, first_name, last_name, email, password='password', is_admin=False):
        """
        Initialize a new User instance.
        
        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to 'password'.
            is_admin (bool, optional): Whether the user is an admin. Defaults to False.
        """
        super().__init__()
        self.id = str(uuid.uuid4())
        self._first_name = None
        self.first_name = first_name
        self._last_name = None
        self.last_name = last_name
        self._email = None
        self.email = email
        self._is_admin = is_admin
        self._password_hash = None
        self.set_password(password)

    def set_password(self, password):
        self._password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self._password_hash, password)

    def to_dict(self):
        """
        Convert the User instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the User.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def first_name(self):
        """
        Get the first name of the user.
        
        Returns:
            str: The user's first name.
        """
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        """
        Set the first name of the user.
        
        Args:
            value (str): The new first name for the user.
        
        Raises:
            TypeError: If the first name is not a string or is empty.
            ValueError: If the first name exceeds 50 characters.
        """
        if not isinstance(value, str) or value.strip() == "":
            raise TypeError("Please enter your first name!")
        if len(value) > 50:
            raise ValueError("Max 50 characters for your first_name!")
        self._first_name = value.strip()

    @property
    def last_name(self):
        """
        Get the last name of the user.
        
        Returns:
            str: The user's last name.
        """
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        """
        Set the last name of the user.
        
        Args:
            value (str): The new last name for the user.
        
        Raises:
            ValueError: If the last name is not a string, is empty, or exceeds 50 characters.
        """
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Please enter your last name!")
        if len(value) > 50:
            raise ValueError("Max 50 characters for your last name!")
        self._last_name = value.strip()

    @property
    def email(self):
        """
        Get the email of the user.
        
        Returns:
            str: The user's email address.
        """
        return self._email
    
    @email.setter
    def email(self, value):
        """
        Set the email of the user.
        
        Args:
            value (str): The new email for the user.
        
        Raises:
            ValueError: If the email is invalid, empty, or too long.
        """
        if value is None:
            raise ValueError("Email address cannot be None.")
        value = value.strip()
        if not value:
            raise ValueError("Email address cannot be empty.")
        if not self.EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format.")
        if len(value) > 254:
            raise ValueError("Email address is too long (max 254 characters).")
        self._email = value.lower()

    @property
    def is_admin(self):
        """
        Get the admin status of the user.
        
        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):

        if not isinstance(value, bool):
            """
        Set the admin status of the user.
        
        Args:
            value (bool): The new admin status for the user.
        
        Raises:
            ValueError: If the value is not a boolean.
        """
            raise ValueError("is_admin must be a boolean.")
        self._is_admin = value

    def __str__(self):
        """
        Return a string representation of the User.
        
        Returns:
            str: A string describing the user.
        """
        return f"User: {self.first_name} {self.last_name}, Email: {self.email}, Admin: {self.is_admin}"
