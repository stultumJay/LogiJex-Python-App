import sys
import os
import traceback
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from dotenv import load_dotenv
import mysql.connector

class SimpleLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Login")
        self.setFixedSize(300, 200)
        self.setStyleSheet("""
            QWidget { background-color: #2c3e50; color: white; }
            QLineEdit { padding: 5px; background-color: #34495e; color: white; border: 1px solid #3498db; }
            QPushButton { background-color: #3498db; color: white; padding: 5px; border: none; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("Inventory System Login")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Initialize database connection outside normal UI flow
        try:
            self.init_database()
        except Exception as e:
            self.status_label.setText(f"DB Error: {str(e)[:30]}...")
            self.status_label.setStyleSheet("color: red;")
    
    def init_database(self):
        """Initialize database connection"""
        # Load environment variables
        load_dotenv()
        
        # Get MySQL connection settings
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "root")
        self.db_password = os.getenv("DB_PASSWORD", "akosijayster")
        self.db_name = os.getenv("DB_NAME", "inventory_db")
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.status_label.setText("Please enter username and password")
            self.status_label.setStyleSheet("color: yellow;")
            return
        
        try:
            # Connect to database
            conn = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            
            # Hash the password (SHA-256)
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Check credentials
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, username, role FROM users WHERE username = %s AND password_hash = %s AND is_active = 1",
                (username, password_hash)
            )
            
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                self.status_label.setText(f"Login successful! Welcome {user['username']} ({user['role']})")
                self.status_label.setStyleSheet("color: lightgreen;")
                
                # Show main window
                self.main_window = SimpleMainWindow(user)
                self.main_window.show()
                self.hide()
            else:
                self.status_label.setText("Invalid username or password")
                self.status_label.setStyleSheet("color: red;")
                self.password_input.clear()
        
        except Exception as e:
            self.status_label.setText(f"Login error: {str(e)[:30]}...")
            self.status_label.setStyleSheet("color: red;")
            print(f"Login error: {e}")
            print(traceback.format_exc())

class SimpleMainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.setWindowTitle(f"Inventory System - {user_data['role'].capitalize()}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #2c3e50; color: white; }
            QLabel { color: white; }
            QPushButton { background-color: #3498db; color: white; padding: 10px; border: none; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Welcome header
        welcome = QLabel(f"Welcome, {user_data['username']}!")
        welcome.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome)
        
        role_label = QLabel(f"Role: {user_data['role'].capitalize()}")
        role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(role_label)
        
        # Buttons for different sections
        self.create_buttons(layout)
        
        # Status area 
        self.status_label = QLabel("System ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Initialize database connection
        try:
            self.init_database()
            self.load_dashboard_data()
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)[:50]}...")
            print(f"Main window error: {e}")
            print(traceback.format_exc())
    
    def create_buttons(self, layout):
        """Create dashboard buttons"""
        # Different buttons based on role
        if self.user_data['role'] == 'admin':
            buttons = [
                ("Manage Products", self.show_products),
                ("Manage Users", self.show_users),
                ("View Reports", self.show_reports)
            ]
        elif self.user_data['role'] == 'manager':
            buttons = [
                ("Manage Products", self.show_products),
                ("View Reports", self.show_reports)
            ]
        else:  # retailer
            buttons = [
                ("View Products", self.show_products),
                ("Sales", self.show_sales)
            ]
        
        buttons_layout = QHBoxLayout()
        for label, callback in buttons:
            btn = QPushButton(label)
            btn.clicked.connect(callback)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        
        # Always add logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        logout_btn.setStyleSheet("background-color: #e74c3c;")
        layout.addWidget(logout_btn)
    
    def init_database(self):
        """Initialize database connection"""
        # Load environment variables
        load_dotenv()
        
        # Get MySQL connection settings
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "root")
        self.db_password = os.getenv("DB_PASSWORD", "akosijayster")
        self.db_name = os.getenv("DB_NAME", "inventory_db")
    
    def load_dashboard_data(self):
        """Load basic dashboard data"""
        try:
            # Connect to database
            conn = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            
            # Count products, users, etc.
            cursor = conn.cursor(dictionary=True)
            
            # Count products
            cursor.execute("SELECT COUNT(*) as count FROM products")
            product_count = cursor.fetchone()['count']
            
            # Count users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            # Count low stock items
            cursor.execute("SELECT COUNT(*) as count FROM products WHERE stock <= min_stock_level AND stock > 0")
            low_stock_count = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            self.status_label.setText(f"Products: {product_count} | Users: {user_count} | Low Stock Items: {low_stock_count}")
            
        except Exception as e:
            self.status_label.setText(f"Error loading data: {str(e)[:30]}...")
            print(f"Dashboard data error: {e}")
            print(traceback.format_exc())
    
    def show_products(self):
        self.status_label.setText("Product management would appear here")
    
    def show_users(self):
        self.status_label.setText("User management would appear here")
    
    def show_reports(self):
        self.status_label.setText("Reports would appear here")
    
    def show_sales(self):
        self.status_label.setText("Sales interface would appear here")
    
    def logout(self):
        reply = QMessageBox.question(self, "Confirm Logout", 
                                  "Are you sure you want to logout?",
                                  QMessageBox.StandardButton.Yes | 
                                  QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Show login window again
            from PyQt6.QtWidgets import QApplication
            login_window = SimpleLoginWindow()
            login_window.show()
            self.close()

if __name__ == "__main__":
    # Handle uncaught exceptions
    def exception_hook(exc_type, exc_value, exc_traceback):
        print(f"Unhandled exception: {exc_value}")
        print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        QMessageBox.critical(None, "Error", f"An unhandled error occurred: {exc_value}")
    
    sys.excepthook = exception_hook
    
    # Start application
    app = QApplication(sys.argv)
    window = SimpleLoginWindow()
    window.show()
    sys.exit(app.exec()) 