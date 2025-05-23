# decorators.py
#
# This module provides custom decorators for use in the application.
# Currently, it includes `role_required` to restrict access to methods based on user roles.
#
# Usage: Imported and used as @role_required(['admin']) on methods within Qt classes.
#
# Helper modules: Uses functools.wraps for proper decorator metadata, QMessageBox for error messages.

from PyQt6.QtWidgets import QMessageBox
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator to restrict access to methods based on user role.
    Checks the `current_user` attribute of the instance for role information.

    Args:
        allowed_roles (str or list): A single role string or a list of allowed role strings.
    """
    if not isinstance(allowed_roles, list):
        allowed_roles = [allowed_roles]  # Convert single role to list for easier checking

    def decorator(func):
        """The actual decorator that wraps the function."""
        @wraps(func)  # Preserves function metadata (name, docstring, etc.)
        def wrapper(self, *args, **kwargs):
            """The wrapper function that performs the role check before calling the original method."""
            # Assumes the decorated class instance (`self`) has a `current_user` attribute (dict).
            if hasattr(self, 'current_user') and self.current_user:
                user_role = self.current_user.get("role")
                if user_role in allowed_roles:
                    return func(self, *args, **kwargs)  # User has permission, execute the method
                else:
                    # User does not have permission, show a warning message.
                    QMessageBox.warning(self, "Access Denied",
                                        f"You do not have the necessary permissions ({user_role}) to perform this action. "
                                        f"Required roles: {', '.join(allowed_roles)}")
            else:
                # `current_user` not found or not authenticated, show a critical error.
                QMessageBox.critical(self, "Authentication Error", "User not authenticated.")
            return None  # Or raise an appropriate exception if preferred for unauthenticated/unauthorized access
        return wrapper
    return decorator
