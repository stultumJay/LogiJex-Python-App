# inventory_manager.py
#
# This module provides the InventoryManager class, a singleton for inventory-related queries and summaries.
# It is used to fetch low stock items, expiring items, and inventory history for dashboards and reports.
#
# Usage: Instantiated as a singleton (InventoryManager()), used by UI/dashboard widgets.
#
# Helper modules: Uses DatabaseManager for DB access.

from core.database_manager import DatabaseManager


class InventoryManager:
    """
    Singleton class for inventory summary and alert queries.
    Used for dashboard widgets and inventory status checks.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def get_low_stock_items(self):
        """
        Return a list of products with stock below their minimum stock level.
        Used for low stock alerts.
        """
        return self.db_manager.get_low_stock_items()

    def get_expiring_items(self, days_threshold=7):
        """
        Return a list of products expiring within the given number of days.
        Used for expiring soon alerts.
        """
        return self.db_manager.get_expiring_items(days_threshold)

    def get_inventory_history(self):
        """
        Return a list of inventory history records (restocks, current stock, etc).
        Used for inventory history reports.
        """
        return self.db_manager.get_inventory_history()