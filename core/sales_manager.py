# sales_manager.py
#
# This module provides the SalesManager class, a singleton for sales-related operations and reports.
# It is used to record sales, undo sales, and generate sales reports for the inventory system.
#
# Usage: Instantiated as a singleton (SalesManager()), used by sales UI and reporting widgets.
#
# Helper modules: Uses DatabaseManager for DB access.

from core.database_manager import DatabaseManager
from PyQt6.QtCore import QDate

class SalesManager:
    """
    Singleton class for sales management and reporting.
    Provides methods to record/undo sales and generate sales reports.
    Used by sales UI and reporting widgets.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SalesManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def record_sale(self, product_id, quantity, total_price, seller_id):
        """
        Record a sale transaction and update product stock.
        Used by sales UI when a sale is made.
        """
        return self.db_manager.record_sale(product_id, quantity, total_price, seller_id)

    def undo_sale(self, sale_id):
        """
        Undo a sale transaction and restore product stock.
        Used by sales UI for sale reversal/correction.
        """
        return self.db_manager.undo_sale(sale_id)

    def get_sales_reports(self, start_date, end_date):
        """
        Return a list of sales between the given dates.
        Used for sales reporting and analytics.
        """
        return self.db_manager.get_sales_reports(start_date, end_date)

    def get_all_sales(self):
        """
        Return all sales records (no date filtering).
        Used for full sales export or analytics.
        """
        # Using a large date range to effectively get all sales
        end_date = QDate.currentDate()
        start_date = QDate(2000, 1, 1)  # Far past date to include all records
        return self.db_manager.get_sales_reports(start_date, end_date)