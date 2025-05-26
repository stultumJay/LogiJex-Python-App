import random
import string
from datetime import datetime, timedelta
from utils.config import AppConfig

# Add default configuration values if they're not defined in AppConfig
if not hasattr(AppConfig, 'MFA_SENDER_EMAIL'):
    setattr(AppConfig, 'MFA_SENDER_EMAIL', 'noreply@inventorysystem.com')

class MFAService:
    _instance = None
    _active_mfa_codes = {} # Stores {username: {'code': 'XYZ', 'expiry': datetime_obj}}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MFAService, cls).__new__(cls)
        return cls._instance

    def generate_mfa_code(self):
        """Generates a random N-character alphanumeric code."""
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for i in range(AppConfig.MFA_CODE_LENGTH))

    def send_mfa_code(self, user_email, username):
        """
        Simulates sending an MFA code to the user's email.
        """
        code = self.generate_mfa_code()
        # Convert minutes to seconds for the expiry calculation
        expiry_seconds = AppConfig.MFA_CODE_EXPIRY_MINUTES * 60
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        self._active_mfa_codes[username] = {'code': code, 'expiry': expiry_time}

        subject = "Your Inventory Management System Login Code"
        body = f"""
Dear {username},

Your Multi-Factor Authentication (MFA) code for logging into the Inventory Management System is:

{code}

This code is valid for {AppConfig.MFA_CODE_EXPIRY_MINUTES} minutes. Please enter it into the application to complete your login.

If you did not request this code, please ignore this email.

Sincerely,
Inventory Management System Team
"""
        # --- SIMULATED EMAIL SENDING ---
        print(f"\n--- SIMULATED MFA EMAIL SENT ---")
        print(f"TO: {user_email}")
        print(f"FROM: {AppConfig.MFA_SENDER_EMAIL}")
        print(f"SUBJECT: {subject}")
        print(f"BODY:\n{body}")
        print(f"--- END SIMULATED EMAIL ---\n")

        return True # Assume success for simulation

    def verify_mfa_code(self, username, entered_code):
        """Verifies the entered MFA code against the stored one."""
        if username not in self._active_mfa_codes:
            print("No MFA code generated for this user or session expired.")
            return False

        stored_info = self._active_mfa_codes[username]
        stored_code = stored_info['code']
        expiry_time = stored_info['expiry']

        if datetime.now() > expiry_time:
            del self._active_mfa_codes[username] # Remove expired code
            print("MFA code expired.")
            return False

        if entered_code == stored_code:
            del self._active_mfa_codes[username] # Code used, remove it
            print("MFA code verified successfully.")
            return True
        else:
            print("Invalid MFA code.")
            return False