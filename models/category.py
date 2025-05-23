# models/category.py
#
# This module defines the Category data class.
# It represents a product category within the inventory system, typically including
# an ID and a name.
#
# Usage: Instantiated to hold category data retrieved from the database or to pass
# category information to UI components or manager classes.
#
# Helper modules: Uses dataclasses for concise class definition.

from dataclasses import dataclass

@dataclass
class Category:
    """
    Data class representing a product category.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category (e.g., "Electronics", "Books").
    """
    id: int
    name: str

    def __str__(self):
        """Return a string representation of the category, typically its name."""
        return self.name

    def to_dict(self):
        """Convert the category object to a dictionary.
        Useful for serialization or when a dictionary representation is needed.
        """
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data_dict):
        """Create a Category object from a dictionary.
        Useful for deserialization or creating an object from dictionary data.

        Args:
            data_dict (dict): A dictionary containing category data with keys 'id' and 'name'.
        
        Returns:
            Category: A new Category object, or None if essential data is missing.
        """
        if not data_dict or 'id' not in data_dict or 'name' not in data_dict:
            # Basic validation: ensure essential keys are present.
            return None 
        return cls(id=data_dict['id'], name=data_dict['name'])

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"