# database_manager.py
#
# This module provides the DatabaseManager class, a singleton responsible for all database operations in the inventory management system.
# It manages MySQL connections, schema creation, CRUD operations for users, products, categories, and sales, and utility queries.
# All database logic is centralized here for maintainability and consistency.
#
# Usage: Instantiated as a singleton (DatabaseManager()), used by other managers (UserManager, ProductManager, etc).
#
# Helper modules: Uses mysql-connector for MySQL, dotenv for environment config, hashlib for password hashing.

import hashlib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode
from PyQt6.QtCore import QDate

class DatabaseManager:
    """
    Singleton class for managing all MySQL database operations for the inventory system.
    Handles connection, schema creation, and CRUD for users, products, categories, and sales.
    """
    _instance = None

    def __new__(cls):
        # Singleton pattern: only one instance exists
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.conn = None  # MySQL connection
            try:
                cls._instance.initialize_database()
            except Exception as e:
                print(f"Database initialization error: {e}")
        return cls._instance

    def initialize_database(self):
        """
        Initialize the MySQL database connection and ensure tables/default data exist.
        Loads config from .env or defaults. Creates schema if missing.
        """
        load_dotenv()
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "akosijayster")
        db_name = os.getenv("DB_NAME", "inventory_db")
        try:
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            print("Successfully connected using mysql-connector-python")
            self._create_tables_with_connector()
            self._add_default_data_with_connector()
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
            raise Exception(f"Database connection failed: {err}")

    def _reconnect_if_needed(self):
        """
        Ensure the MySQL connection is alive, reconnect if needed.
        """
        if not self.conn:
            self.initialize_database()
            return
        try:
            self.conn.ping(reconnect=True, attempts=3, delay=0.5)
        except mysql.connector.Error as err:
            print(f"Error reconnecting to database: {err}")
            self.initialize_database()

    def _create_tables_with_connector(self):
        """
        Create all required tables in the MySQL database if they do not exist.
        """
        try:
            cursor = self.conn.cursor()
            queries = [
                # Users table
                """CREATE TABLE IF NOT EXISTS users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT chk_role CHECK (role IN ('admin', 'manager', 'retailer'))
                )""",
                # Categories table
                """CREATE TABLE IF NOT EXISTS categories (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) UNIQUE NOT NULL
                )""",
                # Products table
                """CREATE TABLE IF NOT EXISTS products (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    category_id INT,
                    brand VARCHAR(50),
                    price DECIMAL(10,2) NOT NULL,
                    stock INT NOT NULL,
                    image_path VARCHAR(255),
                    expiration_date DATE,
                    last_restocked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    min_stock_level INT DEFAULT 5,
                    status VARCHAR(20) DEFAULT 'In Stock',
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                )""",
                # Sales table
                """CREATE TABLE IF NOT EXISTS sales (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    product_id INT,
                    quantity INT NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    seller_id INT,
                    sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
                    FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE SET NULL
                )"""
            ]
            for q_text in queries:
                cursor.execute(q_text)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Failed to create tables with connector: {err}")
            raise Exception(f"Database table creation failed: {err}")

    def _add_default_data_with_connector(self):
        """
        Add default categories, users, and sample products if tables are empty.
        """
        try:
            cursor = self.conn.cursor()
            # Add default categories
            cursor.execute("SELECT COUNT(*) FROM categories")
            if cursor.fetchone()[0] == 0:
                categories = ["Meat", "Seafood", "Pantry Items", "Junk Food", "Pet Food (Wet & Dry)"]
                for cat in categories:
                    cursor.execute("INSERT INTO categories (name) VALUES (%s)", (cat,))
                    print(f"Default category '{cat}' created.")
            # Add default users
            default_users = {
                "admin": {"password": "admin", "email": "admin@example.com"},
                "manager": {"password": "password", "email": "manager@example.com"},
                "retailer": {"password": "password", "email": "retailer@example.com"}
            }
            for role, data in default_users.items():
                cursor.execute(f"SELECT COUNT(*) FROM users WHERE username = %s", (role,))
                if cursor.fetchone()[0] == 0:
                    password_hash = hashlib.sha256(data["password"].encode()).hexdigest()
                    cursor.execute(
                        "INSERT INTO users (username, password_hash, role, email, is_active) VALUES (%s, %s, %s, %s, 1)",
                        (role, password_hash, role, data["email"])
                    )
                    print(f"Default {role} user created.")
            # Add sample products
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                cursor.execute("SELECT id, name FROM categories")
                categories = {name: id for id, name in cursor.fetchall()}
                sample_products = [
                    {"name": "Chicken Breast", "category": "Meat", "brand": "FreshFarms", "price": 150.00, "stock": 15},
                    {"name": "Tuna Steak", "category": "Seafood", "brand": "OceanHarvest", "price": 120.00, "stock": 2},
                    {"name": "Potato Chips", "category": "Junk Food", "brand": "CrispyBite", "price": 50.00, "stock": 20},
                    {"name": "Dog Food Premium", "category": "Pet Food (Wet & Dry)", "brand": "PetNutri", "price": 200.00, "stock": 4}
                ]
                for product in sample_products:
                    category_id = categories.get(product["category"])
                    if category_id:
                        status = "In Stock"
                        if product["stock"] <= 0:
                            status = "No Stock"
                        elif product["stock"] <= 5:
                            status = "Low Stock"
                        cursor.execute(
                            "INSERT INTO products (name, category_id, brand, price, stock, min_stock_level, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (product["name"], category_id, product["brand"], product["price"], product["stock"], 5, status)
                        )
                        print(f"Sample product '{product['name']}' created.")
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Failed to add default data with connector: {err}")
            raise Exception(f"Failed to add default data: {err}")

    def authenticate_user(self, username, password):
        print(f"Authenticating user: {username}")
        # Try SHA-256 hash first
        password_hash_sha256 = hashlib.sha256(password.encode()).hexdigest()
        # Also try MD5 hash (for legacy passwords)
        password_hash_md5 = hashlib.md5(password.encode()).hexdigest()
        
        print(f"Generated SHA-256 hash: {password_hash_sha256}")
        print(f"Generated MD5 hash: {password_hash_md5}")
        
        # If using connector instead of QSqlDatabase
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                # Try both hash methods
                query = "SELECT id, username, role, email, is_active FROM users WHERE username = %s AND (password_hash = %s OR password_hash = %s) AND is_active = 1"
                cursor.execute(query, (username, password_hash_sha256, password_hash_md5))
                user_data = cursor.fetchone()
                print(f"MySQL connector auth result: {user_data}")
                
                if not user_data:
                    # Debug: check if the user exists but password is wrong
                    cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
                    debug_data = cursor.fetchone()
                    if debug_data:
                        print(f"User found but password mismatch. DB hash: {debug_data['password_hash']}")
                
                cursor.close()
                return user_data
            except mysql.connector.Error as err:
                print(f"Authentication query failed: {err}")
                return None
        
        # If using QSqlDatabase
        query = QSqlQuery(self.db)
        query.prepare(
            "SELECT id, username, role, email, is_active FROM users WHERE username = ? AND (password_hash = ? OR password_hash = ?) AND is_active = 1")
        query.addBindValue(username)
        query.addBindValue(password_hash_sha256)
        query.addBindValue(password_hash_md5)
        if not query.exec():
            print(f"Authentication query failed: {query.lastError().text()}")
            return None
        if query.next():
            user_data = {
                "id": query.value(0),
                "username": query.value(1),
                "role": query.value(2),
                "email": query.value(3),
                "is_active": bool(query.value(4))
            }
            return user_data
        return None

    def get_users(self):
        """
        Get all users from the database.
        Returns a list of dictionaries with user data.
        
        This method handles both QSqlDatabase and direct mysql-connector connections.
        """
        # If using direct mysql-connector
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                cursor.execute("SELECT id, username, role, email, is_active FROM users")
                users = cursor.fetchall()
                cursor.close()
                return users
            except mysql.connector.Error as err:
                print(f"Failed to get users: {err}")
                return []
        
        # If using QSqlDatabase
        query = QSqlQuery(self.db)
        if not query.exec("SELECT id, username, role, email, is_active FROM users"):
            print(f"Failed to get users: {query.lastError().text()}")
            return []
        users = []
        while query.next():
            users.append({
                "id": query.value(0),
                "username": query.value(1),
                "role": query.value(2),
                "email": query.value(3),
                "is_active": bool(query.value(4))
            })
        return users

    def add_user(self, username, password, role, email):
        """
        Add a new user to the database.
        
        Args:
            username: User's username (must be unique)
            password: User's password (will be hashed)
            role: User's role (admin, manager, or retailer)
            email: User's email address
            
        Returns:
            True if user was added successfully, False otherwise
            
        This method handles both QSqlDatabase and direct mysql-connector connections.
        """
        # Hash the password using SHA-256
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # If using direct mysql-connector
        if self.conn is not None:
            try:
                cursor = self.conn.cursor()
                query = "INSERT INTO users (username, password_hash, role, email, is_active) VALUES (%s, %s, %s, %s, 1)"
                cursor.execute(query, (username, password_hash, role, email))
                self.conn.commit()
                cursor.close()
                return True
            except mysql.connector.Error as err:
                print(f"Failed to add user: {err}")
                return False
        
        # If using QSqlDatabase
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO users (username, password_hash, role, email, is_active) VALUES (?, ?, ?, ?, 1)")
        query.addBindValue(username)
        query.addBindValue(password_hash)
        query.addBindValue(role)
        query.addBindValue(email)
        if not query.exec():
            print(f"Failed to add user: {query.lastError().text()}")
            return False
        return True

    def update_user(self, user_id, username, role, email, is_active, password=None):
        """
        Update an existing user.
        
        Args:
            user_id: ID of the user to update
            username: Updated username
            role: Updated role
            email: Updated email
            is_active: User active status
            password: New password (if changed), None otherwise
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._reconnect_if_needed()  # Make sure connection is active

            # Use mysql-connector cursor
            if hasattr(self, 'conn') and self.conn:
                cursor = self.conn.cursor(prepared=True)
                
                # First check if the username or email already exists for a DIFFERENT user
                check_query = "SELECT id FROM users WHERE (username = %s OR email = %s) AND id != %s"
                cursor.execute(check_query, (username, email, user_id))
                if cursor.fetchone():
                    return False  # Username or email already exists for another user
                    
                if password:  # If password was changed
                    import hashlib
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    update_query = """
                        UPDATE users 
                        SET username = %s, role = %s, email = %s, password_hash = %s, is_active = %s
                        WHERE id = %s
                    """
                    cursor.execute(update_query, (username, role, email, password_hash, is_active, user_id))
                else:  # Just update without changing password
                    update_query = """
                        UPDATE users 
                        SET username = %s, role = %s, email = %s, is_active = %s
                        WHERE id = %s
                    """
                    cursor.execute(update_query, (username, role, email, is_active, user_id))
                    
                self.conn.commit()
                return cursor.rowcount > 0
                
            # Use QSqlQuery
            else:
                from PyQt6.QtSql import QSqlQuery
                query = QSqlQuery(self.db)
                
                # First check if the username or email already exists for a DIFFERENT user
                query.prepare("SELECT id FROM users WHERE (username = ? OR email = ?) AND id != ?")
                query.addBindValue(username)
                query.addBindValue(email)
                query.addBindValue(user_id)
                query.exec()
                if query.next():
                    return False  # Username or email already exists for another user
                    
                if password:  # If password was changed
                    import hashlib
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    query.prepare("""
                        UPDATE users 
                        SET username = ?, role = ?, email = ?, password_hash = ?, is_active = ?
                        WHERE id = ?
                    """)
                    query.addBindValue(username)
                    query.addBindValue(role)
                    query.addBindValue(email)
                    query.addBindValue(password_hash)
                    query.addBindValue(is_active)
                    query.addBindValue(user_id)
                else:  # Just update without changing password
                    query.prepare("""
                        UPDATE users 
                        SET username = ?, role = ?, email = ?, is_active = ?
                        WHERE id = ?
                    """)
                    query.addBindValue(username)
                    query.addBindValue(role)
                    query.addBindValue(email)
                    query.addBindValue(is_active)
                    query.addBindValue(user_id)
                    
                success = query.exec()
                if not success:
                    print(f"SQL error updating user: {query.lastError().text()}")
                return success
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def delete_user(self, user_id):
        """
        Delete a user by ID
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._reconnect_if_needed()  # Make sure connection is active
            
            # Use mysql-connector cursor
            if hasattr(self, 'conn') and self.conn:
                cursor = self.conn.cursor(prepared=True)
                query = "DELETE FROM users WHERE id = %s"
                cursor.execute(query, (user_id,))
                self.conn.commit()
                return cursor.rowcount > 0
                
            # Use QSqlQuery
            else:
                from PyQt6.QtSql import QSqlQuery
                query = QSqlQuery(self.db)
                query.prepare("DELETE FROM users WHERE id = ?")
                query.addBindValue(user_id)
                success = query.exec()
                if not success:
                    print(f"SQL error deleting user: {query.lastError().text()}")
                return success
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def get_products(self, category_id=None, search_term=None, min_stock=None, max_stock=None):
        """
        Get products with optional filtering.
        Returns a list of product dictionaries with all required keys.
        """
        self._reconnect_if_needed()
        # If using direct mysql-connector
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                sql = """
                    SELECT p.id, p.name, p.brand, c.name as category, p.price, p.stock, 
                           p.min_stock_level, p.image_path, p.expiration_date, p.status,
                           p.category_id
                    FROM products p 
                    JOIN categories c ON p.category_id = c.id 
                    WHERE 1=1
                """
                params = []
                if category_id:
                    sql += " AND p.category_id = %s"
                    params.append(category_id)
                if search_term:
                    sql += " AND (p.name LIKE %s OR c.name LIKE %s OR p.brand LIKE %s)"
                    search_pattern = f"%{search_term}%"
                    params.extend([search_pattern, search_pattern, search_pattern])
                if min_stock is not None:
                    sql += " AND p.stock <= %s"
                    params.append(min_stock)
                if max_stock is not None:
                    sql += " AND p.stock >= %s"
                    params.append(max_stock)
                cursor.execute(sql, params)
                products = cursor.fetchall()
                cursor.close()
                return products
            except mysql.connector.Error as err:
                print(f"Failed to get products: {err}")
                return []
        # Fallback: QSqlDatabase
        query = QSqlQuery(self.db)
        sql = ("SELECT p.id, p.name, p.brand, c.name as category, p.price, p.stock, "
               "p.min_stock_level, p.image_path, p.expiration_date, p.status, p.category_id "
               "FROM products p JOIN categories c ON p.category_id = c.id WHERE 1=1")
        params = []
        if category_id:
            sql += " AND p.category_id = ?"
            params.append(category_id)
        if search_term:
            sql += " AND (p.name LIKE ? OR c.name LIKE ? OR p.brand LIKE ?)"
            search_pattern = f"%{search_term}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        if min_stock is not None:
            sql += " AND p.stock <= ?"
            params.append(min_stock)
        if max_stock is not None:
            sql += " AND p.stock >= ?"
            params.append(max_stock)
        query.prepare(sql)
        for param in params:
            query.addBindValue(param)
        if not query.exec():
            print(f"Failed to get products: {query.lastError().text()}")
            return []
        products = []
        while query.next():
            # Always include all keys, even if None
            products.append({
                'id': query.value(0),
                'name': query.value(1),
                'brand': query.value(2),
                'category': query.value(3),
                'price': query.value(4),
                'stock': query.value(5),
                'min_stock_level': query.value(6),
                'image_path': query.value(7),
                'expiration_date': query.value(8),
                'status': query.value(9),
                'category_id': query.value(10)
            })
        return products

    def get_product_by_id(self, product_id):
        """Get product details by ID"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT id, name, category_id, brand, price, stock, image_path, 
                      expiration_date, last_restocked, min_stock_level, status 
                FROM products WHERE id = %s
            """
            cursor.execute(query, (product_id,))
            product = cursor.fetchone()
            cursor.close()
            
            # Convert date objects to strings
            if product and 'expiration_date' in product and product['expiration_date']:
                product['expiration_date'] = product['expiration_date'].isoformat()
            if product and 'last_restocked' in product and product['last_restocked']:
                product['last_restocked'] = product['last_restocked'].isoformat()
                
            return product
        except mysql.connector.Error as err:
            print(f"Failed to get product by ID: {err}")
            return None

    def add_product(self, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        """
        Add a new product to the database.
        
        Args:
            name: Product name
            category_id: Category ID
            brand: Product brand
            price: Product price
            stock: Initial stock quantity
            image_path: Path to product image (optional)
            expiration_date: Product expiration date (optional)
            min_stock_level: Minimum stock level for low stock warning
            
        Returns:
            True if product was added successfully, False otherwise
        """
        # Always check connection before operations
        self._reconnect_if_needed()
        
        # Determine status based on stock level
        status = "In Stock"
        if stock <= 0:
            status = "No Stock"
        elif stock <= min_stock_level:
            status = "Low Stock"
        
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO products 
                (name, category_id, brand, price, stock, image_path, expiration_date, min_stock_level, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                name, category_id, brand, price, stock, 
                image_path, expiration_date, min_stock_level, status
            ))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to add product: {err}")
            return False

    def update_product(self, product_id, name, category_id, brand, price, stock, image_path=None, expiration_date=None, min_stock_level=5):
        """Update an existing product"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        # Determine status based on stock level
        status = "In Stock"
        if stock <= 0:
            status = "No Stock"
        elif stock <= min_stock_level:
            status = "Low Stock"
            
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE products 
                SET name = %s, category_id = %s, brand = %s, price = %s, stock = %s, 
                    image_path = %s, expiration_date = %s, min_stock_level = %s, status = %s,
                    last_restocked = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            cursor.execute(query, (
                name, category_id, brand, price, stock, 
                image_path, expiration_date, min_stock_level, status, product_id
            ))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to update product: {err}")
            return False

    def delete_product(self, product_id):
        """Delete a product by ID"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor()
            
            # First check if the product is used in any sales
            query = "SELECT COUNT(*) FROM sales WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            count = cursor.fetchone()[0]
            
            # If product is used in sales, set product_id to NULL to preserve sales records
            if count > 0:
                cursor.execute("UPDATE sales SET product_id = NULL WHERE product_id = %s", (product_id,))
            
            # Now delete the product
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to delete product: {err}")
            if self.conn:
                self.conn.rollback()
            return False

    def get_categories(self):
        """
        Get all product categories from the database.
        Returns a list of dictionaries with category id and name.
        """
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()
            cursor.close()
            return categories
        except mysql.connector.Error as err:
            print(f"Failed to get categories: {err}")
            return []

    def add_category(self, name):
        """
        Add a new category to the database.
        
        Args:
            name: Category name (must be unique)
            
        Returns:
            True if category was added successfully, False otherwise
        """
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO categories (name) VALUES (%s)"
            cursor.execute(query, (name,))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to add category: {err}")
            return False

    def update_category(self, category_id, name):
        """Update a category name by ID"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor()
            query = "UPDATE categories SET name = %s WHERE id = %s"
            cursor.execute(query, (name, category_id))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to update category: {err}")
            return False

    def delete_category(self, category_id):
        """Delete a category by ID"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        try:
            cursor = self.conn.cursor()
            
            # First check if any products use this category
            query = "SELECT COUNT(*) FROM products WHERE category_id = %s"
            cursor.execute(query, (category_id,))
            count = cursor.fetchone()[0]
            
            # If category is used by products, notify user
            if count > 0:
                print(f"This category is used by {count} products. Please reassign them first.")
                cursor.close()
                return False
            
            # Now delete the category
            cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
            self.conn.commit()
            cursor.close()
            return True
        except mysql.connector.Error as err:
            print(f"Failed to delete category: {err}")
            if self.conn:
                self.conn.rollback()
            return False

    def record_sale(self, product_id, quantity, total_price, seller_id):
        """Record a sale transaction and update product stock"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        # Start a transaction
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # First get current product stock
            cursor.execute("SELECT stock, min_stock_level FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                print("Failed to get product stock")
                return False
                
            current_stock = product['stock']
            min_stock_level = product['min_stock_level']
            
            # Check if enough stock
            if current_stock < quantity:
                print("Insufficient Stock")
                return False
                
            # Update product stock
            new_stock = current_stock - quantity
            
            # Determine new status
            status = "In Stock"
            if new_stock <= 0:
                status = "No Stock"
            elif new_stock <= min_stock_level:
                status = "Low Stock"
                
            cursor.execute("UPDATE products SET stock = %s, status = %s WHERE id = %s", 
                          (new_stock, status, product_id))
            
            # Record the sale
            cursor.execute("""
                INSERT INTO sales (product_id, quantity, total_price, seller_id) 
                VALUES (%s, %s, %s, %s)
            """, (product_id, quantity, total_price, seller_id))
            
            # Commit the transaction
            self.conn.commit()
            cursor.close()
            return True
            
        except mysql.connector.Error as err:
            if self.conn:
                self.conn.rollback()
            print(f"Error during sale: {str(err)}")
            return False

    def undo_sale(self, sale_id):
        """Undo a sale transaction and restore product stock"""
        # Always check connection before operations
        self._reconnect_if_needed()
        
        # Start a transaction
        try:
            cursor = self.conn.cursor(dictionary=True)
            
            # First get sale details
            cursor.execute("SELECT product_id, quantity FROM sales WHERE id = %s", (sale_id,))
            sale = cursor.fetchone()
            
            if not sale:
                print("Failed to get sale details")
                return False
                
            product_id = sale['product_id']
            quantity = sale['quantity']
            
            # If product_id is NULL (product was deleted), we can't restore stock but can delete the sale
            if product_id is None:
                cursor.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
                self.conn.commit()
                cursor.close()
                return True
                
            # Get current product stock and min_stock_level
            cursor.execute("SELECT stock, min_stock_level FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                print("Failed to get product stock")
                return False
                
            current_stock = product['stock']
            min_stock_level = product['min_stock_level']
            
            # Update product stock
            new_stock = current_stock + quantity
            
            # Determine new status
            status = "In Stock"
            if new_stock <= 0:
                status = "No Stock"
            elif new_stock <= min_stock_level:
                status = "Low Stock"
                
            cursor.execute("UPDATE products SET stock = %s, status = %s WHERE id = %s", 
                          (new_stock, status, product_id))
            
            # Delete the sale
            cursor.execute("DELETE FROM sales WHERE id = %s", (sale_id,))
            
            # Commit the transaction
            self.conn.commit()
            cursor.close()
            return True
            
        except mysql.connector.Error as err:
            if self.conn:
                self.conn.rollback()
            print(f"Error during sale undo: {str(err)}")
            return False

    def get_low_stock_items(self):
        # Check if we're using MySQL connector instead of QSql
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                query = """
                    SELECT p.id, p.name, p.brand, c.name as category, p.price, p.stock, 
                           p.min_stock_level, p.image_path, p.status
                    FROM products p 
                    JOIN categories c ON p.category_id = c.id 
                    WHERE p.stock <= p.min_stock_level AND p.stock > 0
                """
                cursor.execute(query)
                items = cursor.fetchall()
                cursor.close()
                return items
            except mysql.connector.Error as err:
                print(f"Failed to get low stock items: {err}")
                return []
        
        # Original QSql implementation
        query = QSqlQuery(self.db)
        query.prepare("""
            SELECT p.id, p.name, p.brand, c.name, p.price, p.stock, p.min_stock_level, p.image_path, p.status
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.stock <= p.min_stock_level AND p.stock > 0
        """)
        if not query.exec():
            print(f"Failed to get low stock items: {query.lastError().text()}")
            return []
            
        items = []
        while query.next():
            items.append({
                "id": query.value(0),
                "name": query.value(1),
                "brand": query.value(2),
                "category": query.value(3),
                "price": query.value(4),
                "stock": query.value(5),
                "min_stock_level": query.value(6),
                "image_path": query.value(7),
                "status": query.value(8)
            })
        return items

    def get_expiring_items(self, days_threshold=7):
        # Check if we're using MySQL connector instead of QSql
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                
                # MySQL date calculation for expiry threshold
                query = """
                    SELECT p.id, p.name, p.brand, c.name as category, p.price, p.stock, 
                           p.expiration_date, p.image_path, p.status
                    FROM products p 
                    JOIN categories c ON p.category_id = c.id 
                    WHERE p.expiration_date IS NOT NULL 
                    AND p.expiration_date <= DATE_ADD(CURRENT_DATE(), INTERVAL %s DAY)
                    AND p.expiration_date >= CURRENT_DATE()
                """
                cursor.execute(query, (days_threshold,))
                items = cursor.fetchall()
                
                # Convert datetime.date objects to strings for consistent return format
                for item in items:
                    if item['expiration_date']:
                        item['expiration_date'] = item['expiration_date'].isoformat()
                
                cursor.close()
                return items
            except mysql.connector.Error as err:
                print(f"Failed to get expiring items: {err}")
                return []
        
        # Original QSql implementation
        query = QSqlQuery(self.db)
        current_date = QDate.currentDate()
        expiry_threshold = current_date.addDays(days_threshold).toString("yyyy-MM-dd")
        
        query.prepare("""
            SELECT p.id, p.name, p.brand, c.name, p.price, p.stock, p.expiration_date, p.image_path, p.status
            FROM products p 
            JOIN categories c ON p.category_id = c.id 
            WHERE p.expiration_date IS NOT NULL 
            AND p.expiration_date <= ? 
            AND p.expiration_date >= CURRENT_DATE
        """)
        query.addBindValue(expiry_threshold)
        
        if not query.exec():
            print(f"Failed to get expiring items: {query.lastError().text()}")
            return []
            
        items = []
        while query.next():
            items.append({
                "id": query.value(0),
                "name": query.value(1),
                "brand": query.value(2),
                "category": query.value(3),
                "price": query.value(4),
                "stock": query.value(5),
                "expiration_date": query.value(6),
                "image_path": query.value(7),
                "status": query.value(8)
            })
        return items

    def get_sales_reports(self, start_date, end_date):
        """
        Get sales reports between the specified dates.
        
        Args:
            start_date: Start date for the report
            end_date: End date for the report
            
        Returns:
            List of sale dictionaries with detailed information
            
        This method handles both QSqlDatabase and direct mysql-connector connections.
        """
        # Convert dates to string format
        if isinstance(start_date, QDate):
            start_date = start_date.toString("yyyy-MM-dd")
        if isinstance(end_date, QDate):
            end_date = end_date.toString("yyyy-MM-dd")
            
        # Add time component to make it inclusive
        start_datetime = f"{start_date} 00:00:00"
        end_datetime = f"{end_date} 23:59:59"
        
        # If using direct mysql-connector
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                query = """
                    SELECT s.id, p.name, p.brand, c.name as category_name, s.quantity, s.total_price, 
                           u.username, s.sale_time
                    FROM sales s
                    LEFT JOIN products p ON s.product_id = p.id
                    LEFT JOIN categories c ON p.category_id = c.id
                    LEFT JOIN users u ON s.seller_id = u.id
                    WHERE s.sale_time BETWEEN %s AND %s
                    ORDER BY s.sale_time DESC
                """
                cursor.execute(query, (start_datetime, end_datetime))
                sales = cursor.fetchall()
                
                # Process results to match the format of the QSqlDatabase version
                for sale in sales:
                    # Handle case where product might have been deleted
                    sale['product_name'] = sale.get('name', 'Deleted Product')
                    if 'name' in sale:
                        del sale['name']
                    
                    sale['category'] = sale.pop('category_name', 'N/A')
                    
                    # Set defaults for NULL values
                    if sale['brand'] is None:
                        sale['brand'] = 'N/A'
                    
                    # Rename username to seller for consistent access
                    sale['seller'] = sale.pop('username', 'Unknown')
                
                cursor.close()
                return sales
                
            except mysql.connector.Error as err:
                print(f"Failed to get sales report: {err}")
                return []
        
        # If using QSqlDatabase
        query = QSqlQuery(self.db)
        query.prepare("""
            SELECT s.id, p.name, p.brand, c.name, s.quantity, s.total_price, 
                   u.username, s.sale_time
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.id
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN users u ON s.seller_id = u.id
            WHERE s.sale_time BETWEEN ? AND ?
            ORDER BY s.sale_time DESC
        """)
        query.addBindValue(start_datetime)
        query.addBindValue(end_datetime)
        
        if not query.exec():
            print(f"Failed to get sales report: {query.lastError().text()}")
            return []
            
        sales = []
        while query.next():
            # Handle case where product might have been deleted
            product_name = query.value(1) if query.value(1) else "Deleted Product"
            brand = query.value(2) if query.value(2) else "N/A"
            category = query.value(3) if query.value(3) else "N/A"
            
            sales.append({
                "id": query.value(0),
                "product_name": product_name,
                "brand": brand,
                "category": category,
                "quantity": query.value(4),
                "total_price": query.value(5),
                "seller": query.value(6),
                "sale_time": query.value(7)
            })
        return sales

    def get_inventory_history(self):
        # If using direct mysql-connector
        if self.conn is not None:
            try:
                cursor = self.conn.cursor(dictionary=True)
                query = """
                    SELECT p.id, p.name, p.brand, c.name as category, p.price, p.stock as current_stock, 
                           p.last_restocked, p.status
                    FROM products p
                    JOIN categories c ON p.category_id = c.id
                    ORDER BY p.last_restocked DESC
                """
                cursor.execute(query)
                history = cursor.fetchall()
                
                # Convert datetime objects to strings
                for item in history:
                    if item['last_restocked']:
                        item['last_restocked'] = item['last_restocked'].isoformat()
                        
                cursor.close()
                return history
            except mysql.connector.Error as err:
                print(f"Failed to get inventory history: {err}")
                return []
        
        # Original QSql implementation
        # This method will return a simulated inventory history
        # In a real system, you would track every inventory change in a separate table
        query = QSqlQuery(self.db)
        query.prepare("""
            SELECT p.id, p.name, p.brand, c.name, p.price, p.stock, p.last_restocked, p.status
            FROM products p
            JOIN categories c ON p.category_id = c.id
            ORDER BY p.last_restocked DESC
        """)
        
        if not query.exec():
            print(f"Failed to get inventory history: {query.lastError().text()}")
            return []
            
        history = []
        while query.next():
            history.append({
                "id": query.value(0),
                "name": query.value(1),
                "brand": query.value(2),
                "category": query.value(3),
                "price": query.value(4),
                "current_stock": query.value(5),
                "last_restocked": query.value(6),
                "status": query.value(7)
            })
        return history

    def execute_query(self, query, params=None):
        """
        Execute a general SQL query and return the results.
        
        Args:
            query (str): The SQL query to execute
            params (tuple): Optional parameters for the query
            
        Returns:
            list: List of results as tuples or None if query failed
        """
        self._reconnect_if_needed()
        try:
            cursor = self.conn.cursor()
            
            # Execute the query with or without parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Check if this is a SELECT query
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                # For INSERT, UPDATE, DELETE operations
                self.conn.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
                
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            print(f"Query: {query}")
            if params:
                print(f"Parameters: {params}")
            return None