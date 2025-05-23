# models/user.py
#
# This module defines the User data class.
# It represents a user in the inventory system, holding information such as ID,
# username, role (e.g., admin, manager, retailer), email, and active status.
# The password_hash is included for completeness but should be handled securely and
# typically not exposed directly or stored in User objects that are passed around openly.
#
# Usage: Instantiated to hold user data retrieved from the database (excluding raw password hash
# in most contexts), or to pass user information for authentication, authorization (role checks),
# and user management UIs.
#
# Helper modules: Uses dataclasses for concise class definition and typing for type hints.

from dataclasses import dataclass, field
from typing import Optional # For attributes that can be None.

@dataclass
class User:
    """
    Data class representing a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Username for login.
        role (str): Role of the user (e.g., 'admin', 'manager', 'retailer').
                    This dictates permissions within the application.
        email (Optional[str]): User's email address, used for notifications or MFA.
        is_active (bool): Flag indicating if the user account is active. Defaults to True.
        password_hash (Optional[str]): The hashed password. This should generally NOT be
                                     populated in User objects used in the UI or general logic
                                     after authentication. It's primarily for internal DB interaction
                                     or direct authentication checks if necessary.
                                     Defaults to None for User objects.
    """
    id: int
    username: str
    role: str # E.g., "admin", "manager", "retailer"
    
    email: Optional[str] = None
    is_active: bool = True # User is active by default
    
    # Password hash should generally not be stored in User objects passed around after auth.
    # It's included here if a full User representation from DB is needed by a secure backend part.
    # For most client-side or general logic, this would be None or excluded.
    password_hash: Optional[str] = None 

    def __post_init__(self):
        """Post-initialization processing.
        Ensures boolean conversion for is_active if it comes as int (e.g. 0 or 1 from DB).
        """
        # Ensure is_active is a boolean.
        if isinstance(self.is_active, int):
            self.is_active = bool(self.is_active)
        
        # Basic validation for role if needed, though usually handled by DB constraints.
        # Example: if self.role not in ["admin", "manager", "retailer"]:
        #    raise ValueError(f"Invalid role: {self.role}")

    def __str__(self):
        """Return a string representation of the user, typically username and role."""
        return f"{self.username} ({self.role}) - Active: {self.is_active}"

    def to_dict(self, include_hash=False):
        """Convert the User object to a dictionary.
        
        Args:
            include_hash (bool): If True, includes the password_hash in the dictionary.
                                 Defaults to False for security.
        Returns:
            dict: A dictionary representation of the User.
        """
        data = {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "email": self.email,
            "is_active": self.is_active,
        }
        if include_hash and self.password_hash is not None:
            # Only include password_hash if explicitly requested and present.
            data["password_hash"] = self.password_hash
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """Create a User instance from a dictionary.
        Provides basic validation for essential fields.

        Args:
            data (dict): A dictionary containing user data.
        
        Returns:
            User: A new User object, or None if essential data is missing or invalid.
        """
        required_fields = ['id', 'username', 'role'] # Email might be optional depending on system design.
        if not all(field in data and data[field] is not None for field in required_fields):
            print(f"Error: Missing or None required fields in user data: {data}")
            return None

        # Create and return the User instance.
        # is_active defaults to True in dataclass if not provided in dict.
        # password_hash defaults to None in dataclass if not provided.
        return cls(
            id=data['id'],
            username=data['username'],
            role=data['role'],
            email=data.get('email'), # Optional, .get() returns None if not found
            is_active=bool(data.get('is_active', True)), # Ensure boolean, default to True
            password_hash=data.get('password_hash') # Optional
        )