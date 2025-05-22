class Category:
    def __init__(self, category_id, name):
        self.id = category_id
        self.name = name

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"