# models/__init__.py
#
# This __init__.py file serves to mark the 'models' directory as a Python package.
# It also provides a convenient way to import all the data model classes
# (Category, Product, Sale, User) from this package directly.
# This allows other parts of the application to import models like:
#   from models import User, Product
# instead of:
#   from models.user import User
#   from models.product import Product
#
# Usage: This file is automatically processed when the 'models' package or its modules are imported.

# Import data model classes to make them available at the package level.
from .category import Category
from .product import Product
from .sale import Sale
from .user import User

# Optional: Define __all__ to specify what is exported when 'from models import *' is used.
# This is good practice for packages.
__all__ = [
    "Category",
    "Product",
    "Sale",
    "User"
]
