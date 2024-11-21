#!/usr/bin/python3

"""
This module defines the Amenity model.
"""
from sqlalchemy.orm import validates
from app.extensions import db
from . import BaseModel

import uuid

class Amenity(BaseModel):
    """
    Represents an amenity class, to creat amenity object.
    """

    #amenities = []
    __tablename__ = "amenities"
    name = db.Column(db.String(50), nullable=False)
    places = db.relationship('Place', secondary='place_amenity', back_populates='amenities')

    def amenity_to_dict(self):
        """Return a dictionary representation of the Amenity instance."""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
