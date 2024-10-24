#!/usr/bin/python3

from . import BaseModel
import uuid

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update(self, data):
        if 'name' in data:
            self.name = data['name']