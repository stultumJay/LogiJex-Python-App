# user_manager.py
#
# This module provides the UserManager class, a singleton for user authentication and user CRUD operations.
# It is used for login, MFA, and user management in the inventory system.
#
# Usage: Instantiated as a singleton (UserManager()), used by login UI and user management UIs.
#
# Helper modules: Uses DatabaseManager for DB access, MFAService for multi-factor authentication.

from core.database_manager import DatabaseManager
from core.mfa_service import MFAService

class UserManager:
    """
    Singleton class for user authentication and management.
    Provides login, MFA, and CRUD for users.
    Used by login UI and user management UIs.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
            cls._instance.mfa_service = MFAService()
        return cls._instance

    def authenticate_user(self, username, password):
        """
        Authenticate a user by username and password.
        Returns user dict if valid, None otherwise.
        Used by login UI.
        """
        user = self.db_manager.authenticate_user(username, password)
        return user

    def initiate_mfa(self, user):
        """
        Initiate multi-factor authentication for a user (send code to email).
        Returns True if MFA initiated, False otherwise.
        Used by login UI after password check.
        """
        if user and user.get("email"):
            print(f"Initiating MFA for {user['username']} ({user['role']}). Sending code to {user['email']}")
            return self.mfa_service.send_mfa_code(user['email'], user['username'])
        print(f"MFA not initiated for {user['username']} (no email or user not found).")
        return False # No MFA needed or email not available

    def verify_mfa(self, username, code):
        """
        Verify the MFA code for a username.
        Returns True if code is valid, False otherwise.
        Used by login UI after code entry.
        """
        return self.mfa_service.verify_mfa_code(username, code)

    def get_all_users(self):
        """
        Return a list of all users.
        Used by user management UI.
        """
        return self.db_manager.get_users()

    def add_user(self, username, password, role, email):
        """
        Add a new user to the database.
        Used by user creation UI.
        """
        return self.db_manager.add_user(username, password, role, email)

    def update_user(self, user_id, username, role, email, is_active, password=None):
        """
        Update an existing user in the database.
        Used by user editing UI.
        """
        return self.db_manager.update_user(user_id, username, role, email, is_active, password)

    def delete_user(self, user_id):
        """
        Delete a user by their ID.
        Used by user management UI.
        """
        return self.db_manager.delete_user(user_id)
