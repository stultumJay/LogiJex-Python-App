from core.database_manager import DatabaseManager
from core.mfa_service import MFAService

class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance.db_manager = DatabaseManager()
            cls._instance.mfa_service = MFAService()
        return cls._instance

    def authenticate_user(self, username, password):
        user = self.db_manager.authenticate_user(username, password)
        return user

    def initiate_mfa(self, user):
        """Initiates MFA for a given user."""
        if user and user.get("email"):
            print(f"Initiating MFA for {user['username']} ({user['role']}). Sending code to {user['email']}")
            return self.mfa_service.send_mfa_code(user['email'], user['username'])
        print(f"MFA not initiated for {user['username']} (no email or user not found).")
        return False # No MFA needed or email not available

    def verify_mfa(self, username, code):
        """Verifies the MFA code."""
        return self.mfa_service.verify_mfa_code(username, code)

    def get_all_users(self):
        return self.db_manager.get_users()

    def add_user(self, username, password, role, email):
        return self.db_manager.add_user(username, password, role, email)

    def update_user(self, user_id, username, role, email, is_active, password=None):
        return self.db_manager.update_user(user_id, username, role, email, is_active, password)

    def delete_user(self, user_id):
        return self.db_manager.delete_user(user_id)
