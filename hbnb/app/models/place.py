#!/usr/bin/python3

"""
This module defines the Place model.
"""

from . import BaseModel
from .user import User
from flask import current_app

class Place(BaseModel):
    """
    Represents a place in the application.
    """
    def __init__(self, title, description, owner_id, price=0.0, latitude=0.0, longitude=0.0):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): The title of the place.
            description (str): The description of the place.
            owner_id (str): The ID of the owner (user) of the place.
            price (float, optional): The price per night. Defaults to 0.0.
            latitude (float, optional): The latitude coordinate. Defaults to 0.0.
            longitude (float, optional): The longitude coordinate. Defaults to 0.0.
        """
        super().__init__()
        self._title = None
        self.title = title
        self.description = description
        self._price = None
        self.price = price
        self._latitude = None
        self.latitude = latitude
        self._longitude = None
        self.longitude = longitude
        self._owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """
        Get the title of the place.
        
        Returns:
            str: The title of the place.
        """

        return self._title
    
    @title.setter
    def title(self, value):
        """
        Set the title of the place.
        
        Args:
            value (str): The new title for the place.
        
        Raises:
            ValueError: If the title is empty or exceeds 100 characters.
        """
        if not value or len(value) > 100:
            raise ValueError("Your title must be non-empty and not exceed 100 characters")
        self._title = value.strip()

    @property
    def owner(self):
        """Retourne l'objet User correspondant à l'ID du propriétaire."""
        return current_app.facade.get_user(self.owner_id)  # Utilise la façade pour récupérer le propriétaire

    @property
    def price(self):
        """
        Get the price of the place.
        
        Returns:
            float: The price per night.
        """
        return self._price
    
    @price.setter
    def price(self, value):
        """
        Set the price of the place.
        
        Args:
            value (float): The new price for the place.
        
        Raises:
            ValueError: If the price is not a positive number.
        """
        if not isinstance(value, (int, float)) or value < 0.0:
            raise ValueError("Your price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        """
        Get the latitude of the place.
        
        Returns:
            float: The latitude coordinate.
        """
        return self._latitude
    
    @latitude.setter
    def latitude(self, value):
        """
        Set the latitude of the place.
        
        Args:
            value (float): The new latitude for the place.
        
        Raises:
            ValueError: If the latitude is not between -90 and 90.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Please enter a valid latitude")
        if value < -90.0 or value > 90.0:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        """
        Get the longitude of the place.
        
        Returns:
            float: The longitude coordinate.
        """
        return self._longitude
    
    @longitude.setter
    def longitude(self, value):
        """
        Set the longitude of the place.
        
        Args:
            value (float): The new longitude for the place.
        
        Raises:
            ValueError: If the longitude is not between -180 and 180.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Please enter a valid longitude")
        if value < -180.0 or value > 180.0:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    @property
    def owner_id(self):
        """
        Get the owner ID of the place.
        
        Returns:
            str: The ID of the owner.
        """
        return self._owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        """
        Set the owner ID of the place.
        
        Args:
            value (str): The new owner ID for the place.
        """
        self._owner_id = value

    def to_dict(self):
        """
        Convert the Place instance to a dictionary.
        
        Returns:
            dict: A dictionary representation of the Place.
        """
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "price": self.price,
        "latitude": self.latitude,
        "longitude": self.longitude,
        "owner_id": self.owner_id,
        "amenities": [{"id": amenity.id, "name": amenity.name} for amenity in self.amenities],
        "reviews": [{"text": review.text, "rating": review.rating} for review in self.reviews],
        'created_at': self.created_at.isoformat(),
        'updated_at': self.updated_at.isoformat()
    }

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def __str__(self):
        owner = self.owner  # Récupérer l'objet User
        if owner:
            return f"Place: {self.title} (Owner: {owner.first_name} {owner.last_name})"
        return f"Place: {self.title} (Owner not found)"
    