from PyQt6.QtWidgets import QMessageBox
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access to functions based on user role.
    `allowed_roles` can be a single string or a list of strings.
    """
    if not isinstance(allowed_roles, list):
        allowed_roles = [allowed_roles]

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Assumes the decorated class has a 'current_user' attribute
            if hasattr(self, 'current_user') and self.current_user:
                user_role = self.current_user.get("role")
                if user_role in allowed_roles:
                    return func(self, *args, **kwargs)
                else:
                    QMessageBox.warning(self, "Access Denied",
                                        f"You do not have the necessary permissions ({user_role}) to perform this action. "
                                        f"Required roles: {', '.join(allowed_roles)}")
            else:
                QMessageBox.critical(self, "Authentication Error", "User not authenticated.")
            return None # Or raise an exception
        return wrapper
    return decorator
