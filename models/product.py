class Product:
    def __init__(self, product_id, name, category_id, brand, price, stock, image_path=None, 
                 expiration_date=None, last_restocked=None, min_stock_level=5, status="In Stock"):
        self.id = product_id
        self.name = name
        self.category_id = category_id
        self.brand = brand
        self.price = price
        self.stock = stock
        self.image_path = image_path
        self.expiration_date = expiration_date
        self.last_restocked = last_restocked
        self.min_stock_level = min_stock_level
        self.status = status

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', brand='{self.brand}', stock={self.stock}, status={self.status})>"
        
    def update_status(self):
        """Update the status based on current stock level"""
        if self.stock <= 0:
            self.status = "No Stock"
        elif self.stock <= self.min_stock_level:
            self.status = "Low Stock"
        else:
            self.status = "In Stock"
        return self.status