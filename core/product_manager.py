from core.database_manager import DatabaseManager


class ProductManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProductManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
        return cls._instance

    def get_products(self, category_id=None, search_term=None, min_stock=None, max_stock=None):
        return self.db_manager.get_products(category_id, search_term, min_stock, max_stock)

    def get_product_by_id(self, product_id):
        return self.db_manager.get_product_by_id(product_id)

    def add_product(self, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        return self.db_manager.add_product(name, category_id, brand, price, stock, image_path, expiration_date,
                                           min_stock_level)

    def update_product(self, product_id, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        return self.db_manager.update_product(product_id, name, category_id, brand, price, stock, image_path, expiration_date,
                                              min_stock_level)

    def delete_product(self, product_id):
        return self.db_manager.delete_product(product_id)

    def get_categories(self):
        return self.db_manager.get_categories()

    def add_category(self, name):
        return self.db_manager.add_category(name)

    def update_category(self, category_id, name):
        return self.db_manager.update_category(category_id, name)

    def delete_category(self, category_id):
        return self.db_manager.delete_category(category_id)