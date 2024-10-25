#!/usr/bin/python3

"""
This module defines the Amenity model.
"""

from . import BaseModel

import uuid

class Amenity(BaseModel):
    """
    Represents an amenity class, to creat amenity object.
    """

    amenities = []
    def __init__(self, name):
        super().__init__()
        self.name = name

    def amenity_to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
