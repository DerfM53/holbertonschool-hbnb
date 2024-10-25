#!/usr/bin/python3

"""
This module defines the Amenity model.
"""

from . import BaseModel
import uuid

class Amenity(BaseModel):
    """
    Represents an amenity in the application.
    """
    def __init__(self, name):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): The name of the amenity.
        """
        super().__init__()
        self.id = str(uuid.uuid4())
        self.name = name

    def to_dict(self):
        """
        Convert the Amenity instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Amenity.
        """
        return {
            "id": self.id,
            "name": self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        """
        Update the Amenity instance with new data.
        
        Args:
            data (dict): A dictionary containing the attributes to update.
        """
        if 'name' in data:
            self.name = data['name']