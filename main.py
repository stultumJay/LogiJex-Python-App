import sys
import os
import traceback  # Import traceback for detailed error reporting
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog, QSplashScreen
from PyQt6.QtGui import QPixmap, QFontDatabase, QIcon # Import QIcon
from PyQt6.QtCore import Qt
from ui.login_window import LoginWindow
from core.database_manager import DatabaseManager
from utils.styles import get_global_stylesheet  # Import global styles instead of ThemeManager
from utils.config import AppConfig
from dotenv import load_dotenv


def exception_hook(exc_type, exc_value, exc_traceback):
    """Custom exception hook to log unhandled exceptions"""
    print(f"Unhandled exception: {exc_type.__name__}: {exc_value}")
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    QMessageBox.critical(None, "Critical Error",
                         f"Unhandled exception: {exc_type.__name__}: {exc_value}\n\n"
                         f"{''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")


if __name__ == "__main__":
    # Install global exception handler
    sys.excepthook = exception_hook

    try:
        print("Starting application...")

        # Ensure assets directories exist
        print("Creating asset directories...")
        os.makedirs("assets/icons", exist_ok=True)
        os.makedirs("assets/images", exist_ok=True)
        os.makedirs(AppConfig.PRODUCT_IMAGE_DIR, exist_ok=True)

        # Load environment variables
        print("Loading environment variables...")
        load_dotenv()

        # Initialize the application
        print("Initializing QApplication...")
        app = QApplication(sys.argv)

        # Set the application icon (logo)
        logo_path = "assets/images/logo.png"
        if os.path.exists(logo_path):
            app.setWindowIcon(QIcon(logo_path))
            print(f"Application icon set from: {logo_path}")
        else:
            print(f"Warning: Logo file not found at {logo_path}")

        # Apply global stylesheet from utils.styles
        print("Applying application stylesheet...")
        app.setStyleSheet(get_global_stylesheet())

        # Initialize database
        print("Initializing database...")
        try:
            # First check if database exists, if not, set it up
            db_manager = DatabaseManager()
            db_manager.initialize_database()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(None, "Database Error",
                                 f"Failed to initialize database: {str(e)}\n\nPlease check your MySQL connection and credentials.")
            sys.exit(1)

        # Show login window
        print("Creating login window...")
        try:
            login_window = LoginWindow()
            print("Login window created successfully")
            login_window.show()
            print("Login window shown")
        except Exception as e:
            print(f"Error creating login window: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(None, "Login Window Error",
                                 f"Failed to create login window: {str(e)}\n\n{traceback.format_exc()}")
            sys.exit(1)

        # Execute the application
        print("Starting event loop...")
        sys.exit(app.exec())

    except Exception as e:
        print(f"Critical error: {e}")
        print(traceback.format_exc())
        QMessageBox.critical(None, "Critical Error",
                             f"An unexpected error occurred:\n\n{str(e)}\n\nDetails:\n{traceback.format_exc()}")
        sys.exit(1)