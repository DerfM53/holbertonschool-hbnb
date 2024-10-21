#!/usr/bin/python3
from . import BaseModel

import uuid

class Amenity(BaseModel):

    amenities = []
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description

    def to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        return {
            'id': self.id,  # Assuming BaseEntity provides an 'id' attribute
            'name': self.name,
            'description': self.description
        }
