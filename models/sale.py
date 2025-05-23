# models/sale.py
#
# This module defines the Sale data class.
# It represents a sales transaction in the inventory system, linking a product
# to a seller (user) and recording details like quantity, total price, and sale time.
#
# Usage: Instantiated to hold sales data retrieved from the database or to pass sales
# transaction information to UI components or manager classes for recording or display.
#
# Helper modules: Uses dataclasses for concise class definition and typing for type hints.
# Uses datetime for timestamping the sale.

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class Sale:
    """
    Data class representing a sales transaction.

    Attributes:
        id (int): Unique identifier for the sale transaction.
        product_id (int): Foreign key referencing the product that was sold.
        quantity (int): The number of units of the product sold.
        total_price (float): The total price for this sale transaction (quantity * product_price_at_sale_time).
        seller_id (int): Foreign key referencing the user (seller) who made the sale.
        sale_time (datetime): Timestamp of when the sale occurred. Defaults to the current time if not provided.
        product_name (Optional[str]): Name of the product sold (often joined from products table for display).
        seller_username (Optional[str]): Username of the seller (often joined from users table for display).
    """
    id: int
    product_id: int  # Foreign key to Product.id
    quantity: int
    total_price: float
    seller_id: int   # Foreign key to User.id
    
    # Timestamp for the sale, defaults to current time if not specified during creation.
    # The default_factory ensures a new datetime is generated for each new instance if not provided.
    sale_time: datetime = field(default_factory=datetime.now)
    
    # Optional fields, typically populated from database JOINs for display purposes.
    product_name: Optional[str] = None
    seller_username: Optional[str] = None

    def __post_init__(self):
        """Post-initialization processing.
        Ensures quantity is an int and total_price is a float.
        """
        # Ensure correct types for critical numeric fields.
        if self.quantity is not None:
            try:
                self.quantity = int(self.quantity)
            except (ValueError, TypeError):
                print(f"Warning: Sale ID {self.id} has invalid quantity '{self.quantity}'. Setting to 0.")
                self.quantity = 0
        
        if self.total_price is not None:
            try:
                self.total_price = float(self.total_price)
            except (ValueError, TypeError):
                print(f"Warning: Sale ID {self.id} has invalid total_price '{self.total_price}'. Setting to 0.0.")
                self.total_price = 0.0

        # Ensure sale_time is a datetime object if it comes as a string (e.g., from DB query result)
        if isinstance(self.sale_time, str):
            try:
                # Attempt to parse from ISO format; adjust if DB format differs.
                self.sale_time = datetime.fromisoformat(self.sale_time.replace('Z', '+00:00') if 'Z' in self.sale_time else self.sale_time)
            except ValueError:
                print(f"Warning: Sale ID {self.id} has invalid sale_time format '{self.sale_time}'. Using current time.")
                self.sale_time = datetime.now() # Fallback to current time

    def __str__(self):
        """Return a string representation of the sale."""
        product_info = self.product_name or f"Product ID {self.product_id}"
        seller_info = self.seller_username or f"Seller ID {self.seller_id}"
        return (f"Sale ID: {self.id}, Product: {product_info}, Qty: {self.quantity}, "
                f"Total: {self.total_price:.2f}, By: {seller_info} at {self.sale_time.strftime('%Y-%m-%d %H:%M')}")

    def to_dict(self):
        """Convert the Sale object to a dictionary.
        Useful for serialization or database operations. Converts datetime to ISO string.
        """
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "seller_id": self.seller_id,
            "sale_time": self.sale_time.isoformat() if self.sale_time else None,
            # Optional fields are included if they have values.
            "product_name": self.product_name,
            "seller_username": self.seller_username,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create a Sale instance from a dictionary.
        Handles conversion of ISO format datetime string for 'sale_time'.
        Provides basic validation for essential fields.

        Args:
            data (dict): A dictionary containing sale data.
        
        Returns:
            Sale: A new Sale object, or None if essential data is missing or invalid.
        """
        required_fields = ['id', 'product_id', 'quantity', 'total_price', 'seller_id']
        if not all(field in data for field in required_fields):
            print(f"Error: Missing required fields in sale data: {data}")
            return None

        # Convert sale_time from string if necessary
        sale_time_data = data.get('sale_time')
        parsed_sale_time = datetime.now() # Default to now if parsing fails or not provided
        if isinstance(sale_time_data, str):
            try:
                parsed_sale_time = datetime.fromisoformat(sale_time_data.replace('Z', '+00:00') if 'Z' in sale_time_data else sale_time_data)
            except ValueError:
                print(f"Warning: Invalid sale_time format for Sale ID {data.get('id')}: {sale_time_data}. Defaulting.")
        elif isinstance(sale_time_data, datetime):
            parsed_sale_time = sale_time_data
        
        # Create and return the Sale instance.
        return cls(
            id=data['id'],
            product_id=data['product_id'],
            quantity=int(data['quantity']), # Ensure int
            total_price=float(data['total_price']), # Ensure float
            seller_id=data['seller_id'],
            sale_time=parsed_sale_time,
            product_name=data.get('product_name'), # Optional
            seller_username=data.get('seller_username') # Optional
        )

    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total_price})>"