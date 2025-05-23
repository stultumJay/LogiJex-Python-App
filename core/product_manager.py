# product_manager.py
#
# This module provides the ProductManager class, a singleton for product and category CRUD operations.
# It is used by UI and business logic to manage products and categories in the inventory system.
#
# Usage: Instantiated as a singleton (ProductManager()), used by product/category management UIs.
#
# Helper modules: Uses DatabaseManager for DB access.

from core.database_manager import DatabaseManager


class ProductManager:
    """
    Singleton class for product and category management.
    Provides CRUD operations for products and categories.
    Used by product/category management UIs.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def get_products(self, category_id=None, search_term=None, min_stock=None, max_stock=None):
        """
        Return a list of products, optionally filtered by category, search term, or stock range.
        Used for product listing and search.
        """
        return self.db_manager.get_products(category_id, search_term, min_stock, max_stock)

    def get_product_by_id(self, product_id):
        """
        Return details for a single product by its ID.
        Used for product detail views and editing.
        """
        return self.db_manager.get_product_by_id(product_id)

    def add_product(self, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        """
        Add a new product to the database.
        Used by product creation UI.
        """
        return self.db_manager.add_product(name, category_id, brand, price, stock, image_path, expiration_date,
                                           min_stock_level)

    def update_product(self, product_id, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        """
        Update an existing product in the database.
        Used by product editing UI.
        """
        return self.db_manager.update_product(product_id, name, category_id, brand, price, stock, image_path, expiration_date,
                                              min_stock_level)

    def delete_product(self, product_id):
        """
        Delete a product by its ID.
        Used by product management UI.
        """
        return self.db_manager.delete_product(product_id)

    def get_categories(self):
        """
        Return a list of all product categories.
        Used for category dropdowns and management.
        """
        return self.db_manager.get_categories()

    def add_category(self, name):
        """
        Add a new category to the database.
        Used by category creation UI.
        """
        return self.db_manager.add_category(name)

    def update_category(self, category_id, name):
        """
        Update a category's name by its ID.
        Used by category editing UI.
        """
        return self.db_manager.update_category(category_id, name)

    def delete_category(self, category_id):
        """
        Delete a category by its ID.
        Used by category management UI.
        """
        return self.db_manager.delete_category(category_id)