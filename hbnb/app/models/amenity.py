#!/usr/bin/python3
from . import BaseModel

import uuid

class Amenity(BaseModel):

    amenities = []
    def __init__(self, name):
        super().__init__()
        self.name = name
        Amenity.amenities.append(self)

    @classmethod

    def get_aminities(cls):
        return cls.amenities
