#!/usr/bin/python3
from . import BaseModel

import uuid

class Amenity(BaseModel):

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
