# models/product.py
#
# This module defines the Product data class.
# It represents a product in the inventory system, encapsulating various attributes
# such as ID, name, category, brand, price, stock levels, image path, expiration date, etc.
#
# Usage: Instantiated to hold product data retrieved from the database or to pass product
# information between UI components, manager classes, and dialogs for creating/updating products.
#
# Helper modules: Uses dataclasses for concise class definition and typing for type hints.

from dataclasses import dataclass, field # field is used for default_factory if needed.
from typing import Optional # For attributes that can be None.
from datetime import date, datetime # For handling date and datetime objects.

@dataclass
class Product:
    """
    Data class representing a product in the inventory.

    Attributes:
        id (int): Unique identifier for the product.
        name (str): Name of the product.
        category_id (int): Foreign key referencing the category this product belongs to.
        category_name (Optional[str]): Name of the category (often joined from categories table).
        brand (Optional[str]): Brand of the product.
        price (float): Price of the product.
        stock (int): Current stock quantity of the product.
        image_path (Optional[str]): Filesystem path or URL to the product's image.
        expiration_date (Optional[date]): Expiration date of the product, if applicable.
        last_restocked (Optional[datetime]): Timestamp of when the product was last restocked.
        min_stock_level (int): Minimum stock quantity before a low stock warning is triggered.
                               Defaults to 5.
        status (str): Current status of the product (e.g., "In Stock", "Low Stock", "No Stock").
                      Defaults to "In Stock".
    """
    # Core product identifiers and details
    id: int
    name: str
    category_id: int # Foreign key to Category.id
    
    # Descriptive attributes, some may be optional or derived
    category_name: Optional[str] = None # Usually populated via a JOIN query
    brand: Optional[str] = None
    price: float
    stock: int
    image_path: Optional[str] = None # Relative path to image file
    
    # Date-related attributes
    expiration_date: Optional[date] = None
    # Ensure last_restocked can handle datetime objects or string representations if coming from DB
    last_restocked: Optional[datetime] = None 
    
    # Stock management attributes
    min_stock_level: int = 5 # Default minimum stock level
    status: str = "In Stock" # Default status

    def __post_init__(self):
        """Post-initialization processing.
        Used here to ensure correct types for price and stock, and to derive status if needed.
        """
        # Ensure price is float and stock is int, as dataclass might not enforce this from all sources.
        if self.price is not None:
            try:
                self.price = float(self.price)
            except (ValueError, TypeError):
                # Handle or log error if price conversion fails, or set a default.
                print(f"Warning: Product '{self.name}' has invalid price '{self.price}'. Setting to 0.0.")
                self.price = 0.0
        if self.stock is not None:
            try:
                self.stock = int(self.stock)
            except (ValueError, TypeError):
                print(f"Warning: Product '{self.name}' has invalid stock '{self.stock}'. Setting to 0.")
                self.stock = 0
        
        # Automatically determine status based on stock levels if not explicitly set or needs update.
        # This logic can be expanded or made more sophisticated.
        if self.stock <= 0:
            self.status = "No Stock"
        elif self.stock <= self.min_stock_level:
            self.status = "Low Stock"
        else:
            # If stock is above min_stock_level, and status was not something else (e.g. Discontinued)
            # it should be In Stock. This also handles cases where status might be None initially.
            if self.status not in ["Discontinued", "Archived"]: # Example of other statuses
                 self.status = "In Stock"

    def __str__(self):
        """Return a string representation of the product, typically its name."""
        return f"{self.name} (Brand: {self.brand or 'N/A'}, Stock: {self.stock})"

    def to_dict(self):
        """Convert the Product object to a dictionary.
        Handles date/datetime objects by converting them to ISO format strings.
        Useful for serialization (e.g., to JSON) or for database operations.
        """
        return {
            "id": self.id,
            "name": self.name,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "brand": self.brand,
            "price": self.price,
            "stock": self.stock,
            "image_path": self.image_path,
            "expiration_date": self.expiration_date.isoformat() if self.expiration_date else None,
            "last_restocked": self.last_restocked.isoformat() if self.last_restocked else None,
            "min_stock_level": self.min_stock_level,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Product instance from a dictionary.
        Handles conversion of ISO format date/datetime strings back to objects.
        Provides basic validation for essential fields.

        Args:
            data (dict): A dictionary containing product data.
        
        Returns:
            Product: A new Product object, or None if essential data is missing or invalid.
        """
        # Basic validation for essential fields
        required_fields = ['id', 'name', 'category_id', 'price', 'stock']
        if not all(field in data for field in required_fields):
            print(f"Error: Missing required fields in product data: {data}")
            return None

        # Convert date strings to date/datetime objects if they exist and are strings
        exp_date_str = data.get('expiration_date')
        if isinstance(exp_date_str, str):
            try:
                data['expiration_date'] = date.fromisoformat(exp_date_str)
            except ValueError:
                print(f"Warning: Invalid expiration_date format for product {data.get('name')}: {exp_date_str}. Setting to None.")
                data['expiration_date'] = None
        
        restock_date_str = data.get('last_restocked')
        if isinstance(restock_date_str, str):
            try:
                # datetime.fromisoformat might need adjustment if timezone info is present or missing
                # For naive datetimes (no timezone), direct fromisoformat is fine.
                # If timestamps include 'Z' or +HH:MM, more robust parsing might be needed or use dateutil.parser.
                data['last_restocked'] = datetime.fromisoformat(restock_date_str.replace('Z', '+00:00') if 'Z' in restock_date_str else restock_date_str)
            except ValueError:
                print(f"Warning: Invalid last_restocked format for product {data.get('name')}: {restock_date_str}. Setting to None.")
                data['last_restocked'] = None

        # Create and return the Product instance using dictionary unpacking for arguments.
        # This assumes dictionary keys match Product attribute names.
        # Add default values for optional fields not present in the dictionary.
        return cls(
            id=data['id'],
            name=data['name'],
            category_id=data['category_id'],
            category_name=data.get('category_name'), # Optional
            brand=data.get('brand'),                 # Optional
            price=float(data['price']), # Ensure float
            stock=int(data['stock']),   # Ensure int
            image_path=data.get('image_path'),       # Optional
            expiration_date=data.get('expiration_date'), # Already processed
            last_restocked=data.get('last_restocked'),   # Already processed
            min_stock_level=data.get('min_stock_level', 5), # Default if not present
            status=data.get('status', "In Stock")         # Default if not present
        )