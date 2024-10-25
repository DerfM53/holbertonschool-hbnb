#!/usr/bin/python3

"""
This module defines the base model for all other models in the application.
"""

import uuid
from datetime import datetime

class BaseModel:
    """
    Base model class with common attributes and methods for all models.
    """
    def __init__(self):
        """
        Initialize a new BaseModel instance with a unique ID and timestamps.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): A dictionary containing the attributes to update.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp