import sys
import os
import traceback
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from core.database_manager import DatabaseManager
from dotenv import load_dotenv

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Test")
        self.setGeometry(100, 100, 400, 300)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Status label
        self.status_label = QLabel("Testing database connection...")
        layout.addWidget(self.status_label)
        
        # Test buttons
        self.test_db_btn = QPushButton("Test Database Connection")
        self.test_db_btn.clicked.connect(self.test_database)
        layout.addWidget(self.test_db_btn)
        
        self.test_users_btn = QPushButton("Test Get Users")
        self.test_users_btn.clicked.connect(self.test_get_users)
        layout.addWidget(self.test_users_btn)
        
        self.test_products_btn = QPushButton("Test Get Products")
        self.test_products_btn.clicked.connect(self.test_get_products)
        layout.addWidget(self.test_products_btn)
        
        # Initialize database manager
        self.db_manager = None
        
    def test_database(self):
        """Test basic database connection"""
        try:
            self.db_manager = DatabaseManager()
            self.db_manager.initialize_database()
            self.status_label.setText("Database connection successful!")
            QMessageBox.information(self, "Success", "Database connection successful!")
        except Exception as e:
            error_msg = f"Database connection failed: {str(e)}"
            self.status_label.setText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            print(error_msg)
            print(traceback.format_exc())
    
    def test_get_users(self):
        """Test getting users from database"""
        if not self.db_manager:
            self.status_label.setText("Please test database connection first")
            return
            
        try:
            users = self.db_manager.get_users()
            user_info = f"Found {len(users)} users:\n" + "\n".join([f"- {u['username']} ({u['role']})" for u in users])
            self.status_label.setText(user_info)
            QMessageBox.information(self, "Users", user_info)
        except Exception as e:
            error_msg = f"Failed to get users: {str(e)}"
            self.status_label.setText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            print(error_msg)
            print(traceback.format_exc())
    
    def test_get_products(self):
        """Test getting products from database"""
        if not self.db_manager:
            self.status_label.setText("Please test database connection first")
            return
            
        try:
            products = self.db_manager.get_products()
            product_info = f"Found {len(products)} products:\n" + "\n".join([f"- {p['name']} (Stock: {p['stock']})" for p in products[:5]])
            if len(products) > 5:
                product_info += f"\n... and {len(products) - 5} more"
            self.status_label.setText(product_info)
            QMessageBox.information(self, "Products", product_info)
        except Exception as e:
            error_msg = f"Failed to get products: {str(e)}"
            self.status_label.setText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)
            print(error_msg)
            print(traceback.format_exc())

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Create application
    app = QApplication(sys.argv)
    
    # Show test window
    window = TestWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec()) 