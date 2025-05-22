from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from core.user_manager import UserManager
from core.activity_logger import ActivityLogger  # Add logger
from utils.helpers import get_feather_icon
from utils.config import AppConfig
from utils.decorators import role_required
from utils.styles import get_global_stylesheet, apply_table_styles, get_dialog_style  # Import styles


class UserManagementWidget(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.user_manager = UserManager()
        self.activity_logger = ActivityLogger()  # Initialize logger

        # Apply global style instead of inline stylesheet
        self.setStyleSheet(get_global_stylesheet())
        
        self.init_ui()
        self.load_users()

    def init_ui(self):
        """Initialize the user interface with widgets and layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Add User Button
        self.add_user_btn = QPushButton("Add New User")
        self.add_user_btn.setObjectName("addUserButton") # Set object name for easier access
        self.add_user_btn.setIcon(get_feather_icon("user-plus", size=16))
        self.add_user_btn.clicked.connect(self.add_user)
        main_layout.addWidget(self.add_user_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # User Table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(6)  # ID, Username, Role, Email, Active, Actions
        self.user_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Email", "Active", "Actions"])
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.user_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        main_layout.addWidget(self.user_table)

        self.apply_role_permissions()

    def load_users(self):
        users = self.user_manager.get_all_users()
        self.user_table.setRowCount(len(users))
        
        # Apply table styles using the centralized function
        apply_table_styles(self.user_table)
        
        # Set larger row heights for better readability
        self.user_table.verticalHeader().setDefaultSectionSize(50)  # Increase row height
        
        # Make header text larger
        header_font = self.user_table.horizontalHeader().font()
        header_font.setPointSize(12)  # Larger font
        self.user_table.horizontalHeader().setFont(header_font)
        
        for row, user in enumerate(users):
            # Create items with larger font for better readability
            id_item = QTableWidgetItem(str(user['id']))
            username_item = QTableWidgetItem(user['username'])
            role_item = QTableWidgetItem(user['role'].capitalize())
            email_item = QTableWidgetItem(user['email'] if user['email'] else "N/A")
            active_item = QTableWidgetItem("Yes" if user['is_active'] else "No")
            
            # Set larger font for all items
            font = id_item.font()
            font.setPointSize(12)  # Larger font
            
            id_item.setFont(font)
            username_item.setFont(font)
            role_item.setFont(font)
            email_item.setFont(font)
            active_item.setFont(font)
            
            self.user_table.setItem(row, 0, id_item)
            self.user_table.setItem(row, 1, username_item)
            self.user_table.setItem(row, 2, role_item)
            self.user_table.setItem(row, 3, email_item)
            self.user_table.setItem(row, 4, active_item)

            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(5)

            edit_btn = QPushButton("Edit")
            edit_btn.setIcon(get_feather_icon("edit", size=14))
            edit_btn.clicked.connect(lambda _, u=user: self.edit_user(u))
            edit_btn.setMinimumHeight(30)  # Taller button
            actions_layout.addWidget(edit_btn)

            delete_btn = QPushButton("Delete")
            delete_btn.setIcon(get_feather_icon("trash-2", size=14))
            delete_btn.clicked.connect(
                lambda _, u_id=user['id'], u_name=user['username']: self.delete_user(u_id, u_name))
            delete_btn.setMinimumHeight(30)  # Taller button
            actions_layout.addWidget(delete_btn)

            actions_layout.addStretch()

            self.user_table.setCellWidget(row, 5, actions_widget)
            
        self.user_table.resizeColumnsToContents()
        
        # Set minimum column widths
        min_width = 120
        for col in range(self.user_table.columnCount() - 1):  # All except the actions column
            if self.user_table.columnWidth(col) < min_width:
                self.user_table.setColumnWidth(col, min_width)
                
        self.user_table.horizontalHeader().setStretchLastSection(True)

    @role_required(["admin"])
    def add_user(self, *args):
        # Ignore any extra positional arguments that might be passed
        dialog = UserDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()
            if user_data:
                success = self.user_manager.add_user(
                    user_data['username'],
                    user_data['password'],
                    user_data['role'],
                    user_data['email']
                )
                if success:
                    QMessageBox.information(self, "Success", "User added successfully.")
                    self.load_users()
                    # Log user creation with consistent action name
                    self.activity_logger.log_activity(
                        user_info=self.current_user,
                        action="USER_ADDED",
                        target=user_data['username'],
                        details={"role": user_data['role'], "email": user_data['email']}
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to add user. Username or email might already exist.")

    @role_required(["admin"])
    def edit_user(self, user_data):
        dialog = UserDialog(user_data=user_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_user_data()
            if updated_data:
                success = self.user_manager.update_user(
                    user_data['id'],
                    updated_data['username'],
                    updated_data['role'],
                    updated_data['email'],
                    updated_data['is_active'],
                    updated_data.get('password')  # Only pass password if it was changed
                )
                if success:
                    QMessageBox.information(self, "Success", "User updated successfully.")
                    self.load_users()
                    # Log user update with consistent action name
                    self.activity_logger.log_activity(
                        user_info=self.current_user,
                        action="USER_UPDATED",
                        target=updated_data['username'],
                        details={
                            "user_id": user_data['id'],
                            "old_role": user_data['role'],
                            "new_role": updated_data['role'],
                            "is_active": updated_data['is_active'],
                            "email_changed": user_data.get('email') != updated_data.get('email'),
                            "password_changed": 'password' in updated_data
                        }
                    )
                else:
                    QMessageBox.critical(self, "Error", 
                                       "Failed to update user. Username or email might already exist with another user.")
                    # Add debug message to help identify the issue
                    print(f"Failed to update user {user_data['id']} to {updated_data['username']}")

    @role_required(["admin"])
    def delete_user(self, user_id, username):
        if user_id == self.current_user['id']:
            QMessageBox.warning(self, "Deletion Error", "You cannot delete your own account.")
            return

        reply = QMessageBox.question(self, "Delete User",
                                    f"Are you sure you want to delete user '{username}'?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.user_manager.delete_user(user_id)
                if success:
                    QMessageBox.information(self, "Success", "User deleted successfully.")
                    self.load_users()
                    # Log user deletion with consistent action name
                    self.activity_logger.log_activity(
                        user_info=self.current_user,
                        action="USER_DELETED",
                        target=username,
                        details={"user_id": user_id}
                    )
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete user. The database driver may not be loaded or another error occurred.")
                    # Add debug message
                    print(f"Failed to delete user {user_id} ({username})")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Exception occurred: {str(e)}")
                print(f"Exception deleting user: {e}")

    def apply_role_permissions(self):
        """Apply UI restrictions based on user role."""
        role = self.current_user['role']
        if role != 'admin':
            # Use direct reference to the button we created
            if hasattr(self, 'add_user_btn'):
                self.add_user_btn.hide()
            
            # Hide action buttons in the table
            for row in range(self.user_table.rowCount()):
                widget = self.user_table.cellWidget(row, 5)  # Actions column
                if widget:
                    widget.hide()


class UserDialog(QDialog):
    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.password_changed = False  # Track if password was explicitly changed

        if user_data:
            self.setWindowTitle(f"Edit User: {user_data.get('username')}")
        else:
            self.setWindowTitle("Add New User")
        self.setFixedSize(350, 350)

        # Apply dialog style using centralized style
        self.setStyleSheet(get_dialog_style())
        
        self.init_ui()
        self.load_user_data()

    def init_ui(self):
        form_layout = QFormLayout(self)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        self.username_input = QLineEdit()
        form_layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Leave blank to keep current password")
        self.password_input.textChanged.connect(self._password_text_changed)
        form_layout.addRow("Password:", self.password_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("user@example.com (Required for MFA)")
        form_layout.addRow("Email:", self.email_input)

        self.role_combo = QComboBox()
        self.role_combo.addItem("Admin", "admin")
        self.role_combo.addItem("Manager", "manager")
        self.role_combo.addItem("Retailer", "retailer")
        form_layout.addRow("Role:", self.role_combo)

        self.is_active_checkbox = QCheckBox("Account Active")
        self.is_active_checkbox.setChecked(True)
        form_layout.addRow("Status:", self.is_active_checkbox)

        button_box = QHBoxLayout()
        ok_button = QPushButton("Save")
        ok_button.setIcon(get_feather_icon("check-circle", size=16))
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.setIcon(get_feather_icon("x", size=16))
        cancel_button.clicked.connect(self.reject)
        button_box.addStretch()
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        form_layout.addRow(button_box)

    def _password_text_changed(self, text):
        self.password_changed = bool(text)  # Set flag if text is not empty

    def load_user_data(self):
        if self.user_data:
            self.username_input.setText(self.user_data.get('username', ''))
            self.email_input.setText(self.user_data.get('email', ''))

            role_index = self.role_combo.findData(self.user_data.get('role'))
            if role_index != -1:
                self.role_combo.setCurrentIndex(role_index)

            self.is_active_checkbox.setChecked(self.user_data.get('is_active', True))

            # Disable editing own role/status if current user is admin editing themselves
            if self.user_data.get('id') == self.parent().current_user.get('id') and \
                    self.parent().current_user.get('role') == 'admin':
                self.role_combo.setEnabled(False)
                self.is_active_checkbox.setEnabled(False)

    def get_user_data(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip() if self.password_changed else None
        email = self.email_input.text().strip()
        role = self.role_combo.currentData()
        is_active = self.is_active_checkbox.isChecked()

        if not username:
            QMessageBox.warning(self, "Input Error", "Username cannot be empty.")
            return None
        if not self.user_data and not password:  # Password required for new users only
            QMessageBox.warning(self, "Input Error", "Password is required for new users.")
            return None
        if email and "@" not in email:
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address or leave empty.")
            return None
        if role in ['manager', 'retailer'] and not email:
            QMessageBox.warning(self, "Input Error", "Email is required for Manager and Retailer roles for MFA.")
            return None

        # When editing a user, add its ID to the returned data
        data = {
            'username': username,
            'email': email if email else None,
            'role': role,
            'is_active': is_active
        }
        
        # Include the original ID if editing existing user
        if self.user_data and 'id' in self.user_data:
            data['id'] = self.user_data['id']
            
        if password:  # Only add password if it was provided/changed
            data['password'] = password
        return data