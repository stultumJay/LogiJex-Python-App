import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

def setup_mysql_database():
    """
    Set up MySQL database for the inventory application.
    This will create the database and required tables if they don't exist.
    """
    # Load environment variables
    load_dotenv()
    
    # Get MySQL connection settings from environment variables or use defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "akosijayster")
    db_name = os.getenv("DB_NAME", "inventory_db")
    
    # Connect to MySQL server (without specifying a database)
    try:
        cnx = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = cnx.cursor()
        
        # Create database if it doesn't exist
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created or already exists.")
        except mysql.connector.Error as err:
            print(f"Failed to create database: {err}")
            return False
            
        # Switch to the created database
        cursor.execute(f"USE {db_name}")
        
        # Create tables
        tables = {}
        tables['users'] = (
            "CREATE TABLE IF NOT EXISTS users ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  username VARCHAR(50) UNIQUE NOT NULL,"
            "  password_hash VARCHAR(64) NOT NULL,"
            "  role VARCHAR(20) NOT NULL,"
            "  email VARCHAR(100) UNIQUE,"
            "  is_active BOOLEAN DEFAULT 1,"
            "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  CONSTRAINT chk_role CHECK (role IN ('admin', 'manager', 'retailer'))"
            ")"
        )
        
        tables['categories'] = (
            "CREATE TABLE IF NOT EXISTS categories ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  name VARCHAR(50) UNIQUE NOT NULL"
            ")"
        )
        
        tables['products'] = (
            "CREATE TABLE IF NOT EXISTS products ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  name VARCHAR(100) NOT NULL,"
            "  category_id INT,"
            "  brand VARCHAR(50),"
            "  price DECIMAL(10,2) NOT NULL,"
            "  stock INT NOT NULL,"
            "  image_path VARCHAR(255),"
            "  expiration_date DATE,"
            "  last_restocked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  min_stock_level INT DEFAULT 5,"
            "  status VARCHAR(20) DEFAULT 'In Stock',"
            "  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL"
            ")"
        )
        
        tables['sales'] = (
            "CREATE TABLE IF NOT EXISTS sales ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  product_id INT,"
            "  quantity INT NOT NULL,"
            "  total_price DECIMAL(10,2) NOT NULL,"
            "  seller_id INT,"
            "  sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,"
            "  FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE SET NULL"
            ")"
        )
        
        # Execute table creation queries
        for table_name, table_query in tables.items():
            try:
                cursor.execute(table_query)
                print(f"Table '{table_name}' created or already exists.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(f"Table '{table_name}' already exists.")
                else:
                    print(f"Failed to create table '{table_name}': {err}")
        
        # Add default data if the tables are empty
        
        # Check if users table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Add default users with consistent SHA-256 hashing
            default_users = [
                ("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "admin", "admin@example.com", 1),  # Password: admin
                ("manager", "6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17", "manager", "manager@example.com", 1),  # Password: managerpass
                ("retailer", "11f9cd36ed06ea5a0711c2857a42a9886958e3202ac146eb226c66e87e23bd04", "retailer", "retailer@example.com", 1)  # Password: retailerpass
            ]
            
            user_insert_query = (
                "INSERT INTO users (username, password_hash, role, email, is_active) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            
            for user in default_users:
                try:
                    cursor.execute(user_insert_query, user)
                    print(f"Default user '{user[0]}' created.")
                except mysql.connector.Error as err:
                    print(f"Error adding default user '{user[0]}': {err}")
        
        # Check if categories table is empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        
        if category_count == 0:
            # Add default categories
            default_categories = [
                ("Meat",),
                ("Seafood",),
                ("Pantry Items",),
                ("Junk Food",),
                ("Pet Food (Wet & Dry)",)
            ]
            
            category_insert_query = "INSERT INTO categories (name) VALUES (%s)"
            
            for category in default_categories:
                try:
                    cursor.execute(category_insert_query, category)
                    print(f"Default category '{category[0]}' created.")
                except mysql.connector.Error as err:
                    print(f"Error adding default category '{category[0]}': {err}")
        
        # Get category IDs for sample products
        cursor.execute("SELECT id, name FROM categories")
        categories = {name: id for id, name in cursor.fetchall()}
        
        # Check if products table is empty
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        
        if product_count == 0 and categories:
            # Add sample products
            sample_products = [
                ("Chicken Breast", categories.get("Meat"), "FreshFarms", 150.00, 15, None, None, 5, "In Stock"),
                ("Tuna Steak", categories.get("Seafood"), "OceanHarvest", 120.00, 2, None, None, 5, "Low Stock"),
                ("Potato Chips", categories.get("Junk Food"), "CrispyBite", 50.00, 20, None, None, 5, "In Stock"),
                ("Dog Food Premium", categories.get("Pet Food (Wet & Dry)"), "PetNutri", 200.00, 4, None, None, 5, "Low Stock")
            ]
            
            product_insert_query = (
                "INSERT INTO products (name, category_id, brand, price, stock, image_path, expiration_date, min_stock_level, status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            
            for product in sample_products:
                try:
                    cursor.execute(product_insert_query, product)
                    print(f"Sample product '{product[0]}' created.")
                except mysql.connector.Error as err:
                    print(f"Error adding sample product '{product[0]}': {err}")
        
        # Commit changes
        cnx.commit()
        print("MySQL database setup completed successfully.")
        
        # Close cursor and connection
        cursor.close()
        cnx.close()
        return True
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{db_name}' does not exist.")
        else:
            print(f"Error: {err}")
        return False

if __name__ == "__main__":
    setup_mysql_database() 