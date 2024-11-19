#!/usr/bin/python3
"""
This module defines the base model for all other models in the application.
"""

import uuid
from datetime import datetime, timezone
from app.extensions import db

class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()




