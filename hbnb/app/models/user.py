#!/usr/bin/python3

from . import BaseModel
import re

class User(BaseModel):
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


    def __init__(self, first_name, last_name, email, password='password', is_admin=False):
        super().__init__()
        self._first_name = None
        self.first_name = first_name
        self._last_name = None
        self.last_name = last_name
        self._email = None
        self.email = email
        self._is_admin = is_admin
        self.password = password

    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        if value is None or value.strip() == "":
            raise ValueError("Please enter your first name!")
        if len(value) > 50:
            raise ValueError("Max 50 characters for your first_name!")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if value is None or value.strip() == "":
            raise ValueError("Please enter your last name!")
        if len(value) > 50:
            raise ValueError("Max 50 characters for your last name!")
        self._last_name = value.strip()

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
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
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_admin must be a boolean.")
        self._is_admin = value

    def __str__(self):
        return f"User: {self.first_name} {self.last_name}, Email: {self.email}, Admin: {self.is_admin}"
