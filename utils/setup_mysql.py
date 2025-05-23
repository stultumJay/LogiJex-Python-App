# setup_mysql.py
#
# This script provides a standalone function `setup_mysql_database` to initialize
# the MySQL database required by the inventory management application.
# It handles database creation, table creation (users, categories, products, sales),
# and populates them with default/sample data if they are empty.
# Configuration for DB connection (host, user, password, db_name) is loaded from
# .env environment variables, with sensible defaults.
#
# Usage: Can be run directly (python utils/setup_mysql.py) to set up the database schema
# before running the main application for the first time or for resetting the database.
# It is not directly imported by the main application runtime but serves as a setup utility.
#
# Helper modules: Uses mysql-connector for MySQL interaction, os and dotenv for environment variables.

import mysql.connector
from mysql.connector import errorcode # For specific MySQL error codes.
import os
from dotenv import load_dotenv # For loading database credentials from a .env file.

def setup_mysql_database():
    """
    Sets up the MySQL database for the inventory management application.
    This function performs the following steps:
    1. Loads database connection settings from environment variables (.env file or system env).
       Defaults are provided if environment variables are not set.
    2. Connects to the MySQL server (initially without specifying a database).
    3. Creates the target database (e.g., 'inventory_db') if it doesn't already exist.
    4. Switches to the target database.
    5. Defines and executes CREATE TABLE IF NOT EXISTS statements for:
        - users: Stores user credentials and roles.
        - categories: Stores product categories.
        - products: Stores product details, stock, pricing, etc.
        - sales: Stores sales transaction records.
    6. Adds default data (e.g., admin user, sample categories, sample products)
       if the respective tables are found to be empty. This helps in initial setup and testing.
    7. Commits all changes and closes the database connection.

    Returns:
        bool: True if the database setup completes successfully, False otherwise.
              Prints detailed error messages to the console in case of failure.
    """
    # Load environment variables from a .env file if present in the project root.
    load_dotenv()
    
    # Get MySQL connection settings from environment variables or use predefined defaults.
    # This allows flexible configuration without hardcoding credentials.
    db_host = os.getenv("DB_HOST", "localhost") # Default to localhost if DB_HOST not set.
    db_user = os.getenv("DB_USER", "root")      # Default to root user if DB_USER not set.
    db_password = os.getenv("DB_PASSWORD", "akosijayster") # Default password (ensure this is secure or changed).
    db_name = os.getenv("DB_NAME", "inventory_db") # Default database name.
    
    # Attempt to connect to the MySQL server (without selecting a specific database initially).
    try:
        cnx = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = cnx.cursor() # Create a cursor object to execute SQL queries.
        
        # --- Database Creation ---
        # Attempt to create the specified database if it does not already exist.
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{db_name}' created or already exists.")
        except mysql.connector.Error as err:
            print(f"Failed to create database: {err}")
            if cnx.is_connected():
                cursor.close()
                cnx.close()
            return False # Exit if database creation fails.
            
        # Switch the connection to use the newly created (or existing) database.
        cursor.execute(f"USE {db_name}")
        
        # --- Table Creation ---
        # Define a dictionary to hold table names and their corresponding CREATE TABLE SQL statements.
        tables = {}
        tables['users'] = (
            "CREATE TABLE IF NOT EXISTS users ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  username VARCHAR(50) UNIQUE NOT NULL,"
            "  password_hash VARCHAR(64) NOT NULL,  -- Assuming SHA-256 hash length"
            "  role VARCHAR(20) NOT NULL,"
            "  email VARCHAR(100) UNIQUE,"
            "  is_active BOOLEAN DEFAULT 1,"
            "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  CONSTRAINT chk_role CHECK (role IN ('admin', 'manager', 'retailer'))"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        
        tables['categories'] = (
            "CREATE TABLE IF NOT EXISTS categories ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  name VARCHAR(50) UNIQUE NOT NULL"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
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
            "  last_restocked TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
            "  min_stock_level INT DEFAULT 5,"
            "  status VARCHAR(20) DEFAULT 'In Stock', -- e.g., In Stock, Low Stock, No Stock"
            "  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        
        tables['sales'] = (
            "CREATE TABLE IF NOT EXISTS sales ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  product_id INT,"
            "  quantity INT NOT NULL,"
            "  total_price DECIMAL(10,2) NOT NULL,"
            "  seller_id INT, -- Foreign key to the users table (who made the sale)"
            "  sale_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL, -- Set to NULL if product deleted"
            "  FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE SET NULL -- Set to NULL if user deleted"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        )
        
        # Execute the CREATE TABLE queries for each table defined above.
        for table_name, table_query in tables.items():
            try:
                print(f"Creating table '{table_name}'...")
                cursor.execute(table_query)
                print(f"Table '{table_name}' created or already exists.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    # This specific error is fine, means table already exists.
                    print(f"Table '{table_name}' already exists.")
                else:
                    # For other errors during table creation, print the error and stop.
                    print(f"Failed to create table '{table_name}': {err}")
                    # No return here, will be caught by the outer try-except for general errors.
                    raise # Re-raise the exception to be caught by the outer block
        
        # --- Default Data Population ---
        # This section adds initial data if the tables are empty.
        
        # Check and add default users (admin, manager, retailer).
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        if user_count == 0:
            print("Users table is empty. Adding default users...")
            # Passwords should be hashed. Example: 'admin' (SHA256), 'managerpass', 'retailerpass'.
            # Hashes should match those expected by DatabaseManager.authenticate_user.
            default_users_data = [
                ("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "admin", "admin@example.com", 1),
                ("manager", "6ee4a469cd4e91053847f5d3fcb61dbcc91e8f0ef10be7748da4c4a1ba382d17", "manager", "manager@example.com", 1),
                ("retailer", "11f9cd36ed06ea5a0711c2857a42a9886958e3202ac146eb226c66e87e23bd04", "retailer", "retailer@example.com", 1)
            ]
            user_insert_query = "INSERT INTO users (username, password_hash, role, email, is_active) VALUES (%s, %s, %s, %s, %s)"
            for user_data_tuple in default_users_data:
                try:
                    cursor.execute(user_insert_query, user_data_tuple)
                    print(f"Default user '{user_data_tuple[0]}' created.")
                except mysql.connector.Error as err:
                    print(f"Error adding default user '{user_data_tuple[0]}': {err}")
        
        # Check and add default categories.
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        if category_count == 0:
            print("Categories table is empty. Adding default categories...")
            default_categories_data = [("Meat",), ("Seafood",), ("Pantry Items",), ("Junk Food",), ("Pet Food (Wet & Dry)",)]
            category_insert_query = "INSERT INTO categories (name) VALUES (%s)"
            for cat_data_tuple in default_categories_data:
                try:
                    cursor.execute(category_insert_query, cat_data_tuple)
                    print(f"Default category '{cat_data_tuple[0]}' created.")
                except mysql.connector.Error as err:
                    print(f"Error adding default category '{cat_data_tuple[0]}': {err}")

        # Fetch category IDs to use for sample products.
        cursor.execute("SELECT id, name FROM categories")
        # Create a dictionary mapping category name to ID for easy lookup.
        categories_map = {name: cat_id for cat_id, name in cursor.fetchall()}
        
        # Check and add sample products.
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        if product_count == 0 and categories_map: # Only add if products table is empty AND categories exist.
            print("Products table is empty. Adding sample products...")
            sample_products_data = [
                ("Chicken Breast", categories_map.get("Meat"), "FreshFarms", 150.00, 15, None, None, 5, "In Stock"),
                ("Tuna Steak", categories_map.get("Seafood"), "OceanHarvest", 120.00, 2, None, None, 5, "Low Stock"),
                ("Potato Chips", categories_map.get("Junk Food"), "CrispyBite", 50.00, 20, None, None, 5, "In Stock"),
                ("Dog Food Premium", categories_map.get("Pet Food (Wet & Dry)"), "PetNutri", 200.00, 4, None, None, 5, "Low Stock")
            ]
            product_insert_query = (
                "INSERT INTO products (name, category_id, brand, price, stock, image_path, expiration_date, min_stock_level, status) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
            for prod_data_tuple in sample_products_data:
                if prod_data_tuple[1] is not None: # Ensure category_id was found.
                    try:
                        cursor.execute(product_insert_query, prod_data_tuple)
                        print(f"Sample product '{prod_data_tuple[0]}' created.")
                    except mysql.connector.Error as err:
                        print(f"Error adding sample product '{prod_data_tuple[0]}': {err}")
                else:
                    print(f"Skipping sample product '{prod_data_tuple[0]}' due to missing category ID.")
        
        # Commit all DDL and DML changes to the database.
        cnx.commit()
        print("MySQL database setup completed successfully.")
        
        # Close the cursor and connection.
        cursor.close()
        cnx.close()
        return True # Indicate successful setup.
        
    except mysql.connector.Error as err:
        # Handle specific MySQL connection errors for more informative feedback.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL username and password in .env or defaults.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            # This error might occur if the DB_NAME is invalid during initial connection attempt (though we connect without DB first).
            print(f"Database '{db_name}' does not exist or cannot be accessed.")
        elif err.errno == errorcode.CR_CONN_HOST_ERROR:
            print(f"Error: Cannot connect to MySQL host '{db_host}'. Check if the server is running and accessible.")
        else:
            # For any other MySQL errors during the process.
            print(f"MySQL Error: {err}")
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close() # Ensure cursor is closed if it was opened
            cnx.close() # Ensure connection is closed
        return False # Indicate failure.
    except Exception as e:
        # Catch any other non-MySQL exceptions during setup.
        print(f"An unexpected error occurred during database setup: {e}")
        if 'cnx' in locals() and cnx.is_connected():
            cursor.close()
            cnx.close()
        return False # Indicate failure.

if __name__ == "__main__":
    # This block executes if the script is run directly (e.g., `python utils/setup_mysql.py`).
    # Call the setup function and print a status message based on its return value.
    if setup_mysql_database():
        print("Database setup was successful.")
    else:
        print("Database setup failed. Please check the console output for errors.") 