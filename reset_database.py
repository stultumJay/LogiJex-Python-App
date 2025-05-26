import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

def reset_database():
    """Reset the inventory database to reinitialize with updated passwords"""
    # Load environment variables
    load_dotenv()
    
    # Get MySQL connection settings from environment variables or use defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "inventory_db")
    
    try:
        # Connect to MySQL server (without specifying the database)
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        
        cursor = conn.cursor()
        
        # Drop the database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"Database '{db_name}' dropped successfully.")
        
        # Create the database again (it will be initialized when the app runs)
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created successfully. It will be initialized with updated passwords when you run the app.")
        
        cursor.close()
        conn.close()
        
        print("Database reset complete.")
        print("You can now run the application with 'python main.py'")
        print("Login with:")
        print("- Username: admin, Password: admin")
        print("- Username: manager, Password: password")
        print("- Username: retailer, Password: password")
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL username and password.")
        else:
            print(f"Error: {err}")

if __name__ == "__main__":
    reset_database() 