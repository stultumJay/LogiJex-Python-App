class Sale:
    def __init__(self, sale_id, product_id, quantity, total_price, seller_id, sale_time):
        self.id = sale_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price
        self.seller_id = seller_id
        self.sale_time = sale_time

    def __repr__(self):
        return f"<Sale(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, total={self.total_price})>"