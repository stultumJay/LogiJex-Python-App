from core.database_manager import DatabaseManager
from PyQt6.QtCore import QDate

class SalesManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SalesManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def record_sale(self, product_id, quantity, total_price, seller_id):
        return self.db_manager.record_sale(product_id, quantity, total_price, seller_id)

    def undo_sale(self, sale_id):
        return self.db_manager.undo_sale(sale_id)

    def get_sales_reports(self, start_date, end_date):
        return self.db_manager.get_sales_reports(start_date, end_date)

    def get_all_sales(self):
        """Get all sales records without date filtering"""
        # Using a large date range to effectively get all sales
        end_date = QDate.currentDate()
        start_date = QDate(2000, 1, 1)  # Far past date to include all records
        return self.db_manager.get_sales_reports(start_date, end_date)