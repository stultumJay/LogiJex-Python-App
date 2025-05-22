from core.database_manager import DatabaseManager


class InventoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def get_low_stock_items(self):
        return self.db_manager.get_low_stock_items()

    def get_expiring_items(self, days_threshold=7):
        return self.db_manager.get_expiring_items(days_threshold)

    def get_inventory_history(self):
        return self.db_manager.get_inventory_history()