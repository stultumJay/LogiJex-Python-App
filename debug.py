import os
import sys
import mysql.connector
from dotenv import load_dotenv
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication

def check_mysql_direct():
    """Test direct MySQL connection"""
    load_dotenv()
    
    # Get MySQL connection settings from environment variables or use defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "akosijayster")
    db_name = os.getenv("DB_NAME", "inventory_db")
    
    print(f"\n--- Testing direct MySQL connection ---")
    print(f"Host: {db_host}")
    print(f"User: {db_user}")
    print(f"Database: {db_name}")
    
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        print("✅ MySQL connection successful!")
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT VERSION() as version")
        version = cursor.fetchone()
        print(f"MySQL version: {version['version']}")
        
        # Test users table
        cursor.execute("SHOW TABLES")
        tables = [t['Tables_in_' + db_name] for t in cursor.fetchall()]
        print(f"Tables: {', '.join(tables)}")
        
        if 'users' in tables:
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            print(f"User count: {user_count}")
            
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            for user in users:
                print(f"- {user['username']} ({user['role']})")
        else:
            print("⚠️ Users table not found!")
            
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL connection error: {err}")

def check_qsql(app):
    """Test QSqlDatabase connection"""
    load_dotenv()
    
    # Get MySQL connection settings from environment variables or use defaults
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "akosijayster")
    db_name = os.getenv("DB_NAME", "inventory_db")
    
    print(f"\n--- Testing QSqlDatabase connection ---")
    
    # Show available drivers
    drivers = QSqlDatabase.drivers()
    print(f"Available drivers: {', '.join(drivers)}")
    
    # Try connecting with QMYSQL driver
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName(db_host)
    db.setUserName(db_user)
    db.setPassword(db_password)
    db.setDatabaseName(db_name)
    
    if db.open():
        print("✅ QSqlDatabase connection successful!")
        
        query = QSqlQuery(db)
        if query.exec("SELECT VERSION()") and query.next():
            version = query.value(0)
            print(f"MySQL version via QSql: {version}")
        
        tables_query = QSqlQuery(db)
        if tables_query.exec("SHOW TABLES"):
            tables = []
            while tables_query.next():
                tables.append(tables_query.value(0))
            print(f"Tables via QSql: {', '.join(tables)}")
        
        if 'users' in tables:
            users_query = QSqlQuery(db)
            if users_query.exec("SELECT username, role FROM users"):
                print("Users from QSql:")
                while users_query.next():
                    username = users_query.value(0)
                    role = users_query.value(1)
                    print(f"- {username} ({role})")
        else:
            print("⚠️ Users table not found via QSql")
            
        db.close()
    else:
        print(f"❌ QSqlDatabase connection error: {db.lastError().text()}")

if __name__ == "__main__":
    print("=== MySQL Connection Diagnostics ===")
    
    # Check paths and environment
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    # Test direct MySQL connection
    check_mysql_direct()
    
    # Create QApplication for QSql tests
    app = QApplication(sys.argv)
    check_qsql(app)
    
    print("\nDiagnostics complete.") 