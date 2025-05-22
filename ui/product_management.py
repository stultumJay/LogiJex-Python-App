from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QComboBox,
                             QDoubleSpinBox, QSpinBox, QDateEdit, QFileDialog,
                             QScrollArea, QGridLayout, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QSize, QMargins
from PyQt6.QtGui import QPixmap, QIcon
import os
from core.product_manager import ProductManager
from core.activity_logger import ActivityLogger
from utils.helpers import get_feather_icon, save_product_image, delete_product_image, load_product_image
from utils.config import AppConfig
from utils.decorators import role_required
from utils.styles import get_global_stylesheet, get_product_card_style, get_dialog_style, apply_table_styles


class ProductCard(QFrame):
    """A custom widget representing a product card in the grid view"""
    def __init__(self, product_data, on_edit_callback=None, on_delete_callback=None, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.on_edit_callback = on_edit_callback
        self.on_delete_callback = on_delete_callback
        
        self.setObjectName("productCard")
        self.setProperty("class", "product-card")
        self.setFixedSize(220, 300) # Ensure uniform size for all cards

        self.setStyleSheet(get_product_card_style()) # Apply specific product card styling
        
        # Setup layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Product image with better container
        image_container = QFrame()
        image_container.setFixedSize(200, 200)
        image_container.setStyleSheet(f"""
            background-color: white;
            border-radius: 5px;
            border: 1px solid rgba(0,0,0,0.1);
        """)
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        self.image_label.setFixedSize(200, 200)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)  # Scale the image to fit the label
        
        image_path = product_data.get('image_path')
        pixmap = load_product_image(image_path, target_size=(200, 200), keep_aspect_ratio=True)
        self.image_label.setPixmap(pixmap)
        
        image_layout.addWidget(self.image_label)
        layout.addWidget(image_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Product info in a separate stylized container
        info_container = QFrame()
        info_container.setObjectName("infoContainer")
        info_container.setStyleSheet(f"""
            #infoContainer {{
                background-color: rgba(255,255,255,0.05);
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(8, 8, 8, 8)
        info_layout.setSpacing(5)
        
        # Product name with bold styling
        name_label = QLabel(product_data['name'])
        name_label.setProperty("class", "product-title")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(name_label)
        
        # Brand
        brand_label = QLabel(f"Brand: {product_data.get('brand', 'N/A')}")
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(brand_label)
        
        # Price with highlight color
        price_label = QLabel(f"${product_data['price']:.2f}")
        price_label.setProperty("class", "product-price")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(price_label)
        
        # Stock info with status color
        stock_status_class = ""
        if product_data['status'] == "Low Stock":
            stock_status_class = "status-low-stock"
        elif product_data['status'] == "No Stock":
            stock_status_class = "status-no-stock"
        else:
            stock_status_class = "status-in-stock"
            
        stock_label = QLabel(f"Stock: {product_data['stock']} ({product_data['status']})")
        stock_label.setProperty("class", stock_status_class)
        stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(stock_label)
        
        # Category
        category_label = QLabel(f"Category: {product_data['category']}")
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(category_label)
        
        layout.addWidget(info_container)
        
        # Actions buttons
        if on_edit_callback or on_delete_callback:
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(10)
            
            if on_edit_callback:
                edit_btn = QPushButton("Edit")
                edit_btn.setIcon(get_feather_icon("edit", size=14))
                edit_btn.clicked.connect(lambda: on_edit_callback(product_data))
                buttons_layout.addWidget(edit_btn)
            
            if on_delete_callback:
                delete_btn = QPushButton("Delete")
                delete_btn.setIcon(get_feather_icon("trash-2", size=14))
                delete_btn.clicked.connect(lambda: on_delete_callback(product_data['id'], 
                                                                    product_data['name'],
                                                                    product_data['image_path']))
                buttons_layout.addWidget(delete_btn)
                
            layout.addLayout(buttons_layout)


class ProductManagementWidget(QWidget):
    def __init__(self, current_user, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.product_manager = ProductManager()
        self.activity_logger = ActivityLogger()

        self.setStyleSheet(get_global_stylesheet()) # Apply global styles
        
        self.init_ui()
        self.refresh_products_display()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Search and Filter Bar
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.textChanged.connect(self.load_products)
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input)

        self.category_filter_combo = QComboBox()
        self.category_filter_combo.addItem("All Categories", None)
        self.category_filter_combo.currentIndexChanged.connect(self.load_products)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter_combo)
        filter_layout.addStretch()
        main_layout.addLayout(filter_layout)

        # Sort Bar
        sort_bar = QWidget()
        sort_bar.setObjectName("sortBar")
        sort_layout = QHBoxLayout(sort_bar)
        sort_layout.setContentsMargins(10, 5, 10, 5)
        
        sort_layout.addWidget(QLabel("Sort by:"))
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Name (A-Z)", "name_asc")
        self.sort_combo.addItem("Name (Z-A)", "name_desc")
        self.sort_combo.addItem("Price (Low to High)", "price_asc")
        self.sort_combo.addItem("Price (High to Low)", "price_desc")
        self.sort_combo.addItem("Stock (Low to High)", "stock_asc")
        self.sort_combo.addItem("Stock (High to Low)", "stock_desc")
        self.sort_combo.currentIndexChanged.connect(self.load_products)
        sort_layout.addWidget(self.sort_combo)
        
        sort_layout.addStretch()
        
        # View options - could add list/grid toggle in future
        view_label = QLabel("View:")
        sort_layout.addWidget(view_label)
        
        self.grid_size_combo = QComboBox()
        self.grid_size_combo.addItem("3 Cards per Row", 3)
        self.grid_size_combo.addItem("4 Cards per Row", 4)
        self.grid_size_combo.addItem("5 Cards per Row", 5)
        self.grid_size_combo.currentIndexChanged.connect(self.refresh_products_display)
        sort_layout.addWidget(self.grid_size_combo)
        
        main_layout.addWidget(sort_bar)

        # Add Product Button
        self.add_product_btn = QPushButton("Add New Product")
        self.add_product_btn.setObjectName("addProductButton")
        self.add_product_btn.setIcon(get_feather_icon("plus", size=16))
        self.add_product_btn.clicked.connect(self.add_product)
        main_layout.addWidget(self.add_product_btn, alignment=Qt.AlignmentFlag.AlignRight)

        # Scroll area for product cards grid
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Container widget for grid layout
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(15)
        
        self.scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(self.scroll_area)

        self.load_categories()
        self.apply_role_permissions()

    def load_categories(self):
        categories = self.product_manager.get_categories()
        self.category_filter_combo.clear()
        self.category_filter_combo.addItem("All Categories", None)
        for cat in categories:
            self.category_filter_combo.addItem(cat['name'], cat['id'])

    def refresh_products_display(self):
        self.load_products()

    def load_products(self):
        search_term = self.search_input.text().strip()
        category_id = self.category_filter_combo.currentData()
        
        products = self.product_manager.get_products(category_id=category_id, search_term=search_term)
        
        # Apply sorting
        sort_option = self.sort_combo.currentData()
        if sort_option == "name_asc":
            products.sort(key=lambda x: x['name'])
        elif sort_option == "name_desc":
            products.sort(key=lambda x: x['name'], reverse=True)
        elif sort_option == "price_asc":
            products.sort(key=lambda x: float(x['price']))
        elif sort_option == "price_desc":
            products.sort(key=lambda x: float(x['price']), reverse=True)
        elif sort_option == "stock_asc":
            products.sort(key=lambda x: x['stock'])
        elif sort_option == "stock_desc":
            products.sort(key=lambda x: x['stock'], reverse=True)
        
        # Clear existing product cards
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Set up grid parameters
        cards_per_row = self.grid_size_combo.currentData()
        
        # Create product cards and add to grid
        for i, product in enumerate(products):
            row = i // cards_per_row
            col = i % cards_per_row
            
            # Determine if edit/delete callbacks should be enabled based on role
            edit_callback = self.edit_product if self.current_user['role'] in ['admin', 'manager'] else None
            delete_callback = self.delete_product if self.current_user['role'] in ['admin', 'manager'] else None
            
            product_card = ProductCard(product, edit_callback, delete_callback)
            self.grid_layout.addWidget(product_card, row, col)
            
        # Add empty widgets to fill the last row if needed
        total_items = len(products)
        if total_items % cards_per_row != 0:
            remaining = cards_per_row - (total_items % cards_per_row)
            for i in range(remaining):
                empty_widget = QWidget()
                self.grid_layout.addWidget(empty_widget, total_items // cards_per_row, (total_items % cards_per_row) + i)

    @role_required(["admin", "manager"])
    def add_product(self, *args):
        # Ignore any extra positional arguments that might be passed
        dialog = ProductDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                # Handle the image
                saved_image_rel_path = None
                image_path = product_data.get('image_path')
                if image_path:
                    # Only save if it's not already in our product_images directory
                    if not image_path.startswith(AppConfig.PRODUCT_IMAGE_DIR):
                        saved_image_rel_path = save_product_image(image_path)
                    else:
                        saved_image_rel_path = image_path  # Already in the right directory

                success = self.product_manager.add_product(
                    product_data['name'],
                    product_data['category_id'],
                    product_data['brand'],  # Correct order: brand before price
                    product_data['price'],
                    product_data['stock'],
                    saved_image_rel_path,  # Use the saved relative path
                    product_data['expiration_date'],
                    product_data['min_stock_level']
                )
                if success:
                    # Log product creation with consistent action name
                    self.activity_logger.log_activity(
                        user_info=self.current_user,
                        action="PRODUCT_ADDED",
                        target=product_data['name'],
                        details={
                            "brand": product_data['brand'],
                            "category_id": product_data['category_id'],
                            "price": float(product_data['price']),
                            "stock": product_data['stock'],
                            "min_stock_level": product_data['min_stock_level'],
                            "has_image": saved_image_rel_path is not None,
                            "added_by_role": self.current_user.get("role")
                        }
                    )
                    QMessageBox.information(self, "Success", "Product added successfully.")
                    self.load_products()  # Refresh display
                else:
                    QMessageBox.critical(self, "Error", "Failed to add product.")

    @role_required(["admin", "manager"])
    def edit_product(self, product_data):
        dialog = ProductDialog(product_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_data = dialog.get_product_data()
            if updated_data:
                # Handle image update: delete old if new one selected and different
                old_image_path = product_data.get('image_path')
                new_image_path_from_dialog = updated_data.get(
                    'image_path')  # This is the original path or new selected path

                final_image_path_for_db = old_image_path  # Assume no change initially

                if new_image_path_from_dialog and new_image_path_from_dialog != old_image_path:
                    # A new image was selected or existing one was re-selected (need to re-save if it's a temp path)
                    # Check if it's a new file (not already in our assets/product_images)
                    if not new_image_path_from_dialog.startswith(AppConfig.PRODUCT_IMAGE_DIR):
                        saved_image_rel_path = save_product_image(new_image_path_from_dialog)
                        if saved_image_rel_path:
                            final_image_path_for_db = saved_image_rel_path
                            # Delete old image if it exists
                            if old_image_path and os.path.exists(old_image_path):
                                delete_product_image(old_image_path)
                        else:
                            QMessageBox.warning(self, "Image Save Error",
                                                "Could not save new image. Product updated without new image.")
                            final_image_path_for_db = old_image_path  # Revert to old path if new save failed
                    else:
                        # Image was already in the product_images directory, no need to re-save
                        final_image_path_for_db = new_image_path_from_dialog
                elif not new_image_path_from_dialog and old_image_path:  # Image was removed
                    delete_product_image(old_image_path)
                    final_image_path_for_db = None  # Set to None in DB

                success = self.product_manager.update_product(
                    product_data['id'],
                    updated_data['name'],
                    updated_data['category_id'],
                    updated_data['brand'],  # Correct order: brand before price
                    updated_data['price'],
                    updated_data['stock'],
                    final_image_path_for_db,  # Use the final path for DB
                    updated_data['expiration_date'],
                    updated_data['min_stock_level']
                )
                if success:
                    # Log product update with consistent action name
                    self.activity_logger.log_activity(
                        user_info=self.current_user,
                        action="PRODUCT_UPDATED",
                        target=updated_data['name'],
                        details={
                            "product_id": product_data['id'],
                            "old_name": product_data.get('name'),
                            "brand": updated_data['brand'],
                            "category_id": updated_data['category_id'],
                            "price": float(updated_data['price']),
                            "stock": updated_data['stock'],
                            "min_stock_level": updated_data['min_stock_level'],
                            "image_changed": old_image_path != final_image_path_for_db,
                            "updated_by_role": self.current_user.get("role")
                        }
                    )
                    QMessageBox.information(self, "Success", "Product updated successfully.")
                    self.load_products()  # Refresh display
                else:
                    QMessageBox.critical(self, "Error", "Failed to update product.")

    @role_required(["admin", "manager"])
    def delete_product(self, product_id, product_name, image_path):
        reply = QMessageBox.question(self, "Delete Product",
                                     f"Are you sure you want to delete product '{product_name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            success = self.product_manager.delete_product(product_id)
            if success:
                # Also delete the associated image file
                delete_product_image(image_path)
                
                # Log product deletion with consistent action name
                self.activity_logger.log_activity(
                    user_info=self.current_user,
                    action="PRODUCT_DELETED",
                    target=product_name,
                    details={
                        "product_id": product_id,
                        "had_image": image_path is not None and image_path != "",
                        "deleted_by_role": self.current_user.get("role")
                    }
                )
                
                QMessageBox.information(self, "Success", "Product deleted successfully.")
                self.load_products()  # Refresh display
            else:
                QMessageBox.critical(self, "Error", "Failed to delete product.")

    def apply_role_permissions(self):
        """Apply UI restrictions based on user role."""
        role = self.current_user['role']
        if role == 'retailer':
            # Use direct reference to the button we created
            if hasattr(self, 'add_product_btn'):
                self.add_product_btn.hide()


class ProductDialog(QDialog):
    def __init__(self, product_data=None, parent=None):
        super().__init__(parent)
        self.product_manager = ProductManager()
        self.product_data = product_data
        self.selected_image_path = product_data.get('image_path') if product_data else None

        if product_data:
            self.setWindowTitle(f"Edit Product: {product_data.get('name')}")
        else:
            self.setWindowTitle("Add New Product")
        self.setFixedSize(400, 550)  # Increased height for image preview

        self.setStyleSheet(get_dialog_style())
        self.init_ui()
        self.load_categories()
        self.load_product_data()

    def init_ui(self):
        form_layout = QFormLayout(self)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(10)

        self.name_input = QLineEdit()
        form_layout.addRow("Product Name:", self.name_input)

        self.brand_input = QLineEdit()
        form_layout.addRow("Brand:", self.brand_input)  # New brand field

        self.category_combo = QComboBox()
        form_layout.addRow("Category:", self.category_combo)

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 99999.99)
        self.price_input.setPrefix("$")
        self.price_input.setDecimals(2)
        form_layout.addRow("Price:", self.price_input)

        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 99999)
        form_layout.addRow("Stock Quantity:", self.stock_input)

        self.min_stock_input = QSpinBox()
        self.min_stock_input.setRange(0, 1000)
        self.min_stock_input.setValue(5)  # Default min stock level
        form_layout.addRow("Min Stock Level:", self.min_stock_input)

        self.expiration_date_input = QDateEdit(calendarPopup=True)
        self.expiration_date_input.setMinimumDate(QDate.currentDate())
        self.expiration_date_input.setDate(QDate.currentDate().addYears(1))  # Default to 1 year from now
        form_layout.addRow("Expiration Date:", self.expiration_date_input)

        # Image selection
        image_layout = QHBoxLayout()
        self.image_preview_label = QLabel("No Image Selected")
        self.image_preview_label.setObjectName("imagePreviewLabel")
        self.image_preview_label.setFixedSize(120, 120)
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setWordWrap(True)
        image_layout.addWidget(self.image_preview_label)

        image_buttons_layout = QVBoxLayout()
        self.select_image_btn = QPushButton("Select Image")
        self.select_image_btn.setIcon(get_feather_icon("image", size=16))
        self.select_image_btn.clicked.connect(self.select_image)
        image_buttons_layout.addWidget(self.select_image_btn)

        self.clear_image_btn = QPushButton("Clear Image")
        self.clear_image_btn.setIcon(get_feather_icon("x-circle", size=16))
        self.clear_image_btn.clicked.connect(self.clear_image)
        image_buttons_layout.addWidget(self.clear_image_btn)
        image_buttons_layout.addStretch()
        image_layout.addLayout(image_buttons_layout)
        form_layout.addRow("Product Image:", image_layout)

        # Buttons
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

    def load_categories(self):
        categories = self.product_manager.get_categories()
        self.category_combo.clear()
        for cat in categories:
            self.category_combo.addItem(cat['name'], cat['id'])
        if not categories:
            self.category_combo.addItem("No Categories (Add in Category Mgmt)", -1)
            self.category_combo.setEnabled(False)  # Disable if no categories exist

    def load_product_data(self):
        if self.product_data:
            self.name_input.setText(self.product_data.get('name', ''))
            self.brand_input.setText(self.product_data.get('brand', ''))  # Set brand

            # Select category
            category_id = self.product_data.get('category_id')
            if category_id:
                index = self.category_combo.findData(category_id)
                if index != -1:
                    self.category_combo.setCurrentIndex(index)

            self.price_input.setValue(self.product_data.get('price', 0.0))
            self.stock_input.setValue(self.product_data.get('stock', 0))
            self.min_stock_input.setValue(self.product_data.get('min_stock_level', 5))

            # Handle expiration date properly
            exp_date_value = self.product_data.get('expiration_date')
            if exp_date_value:
                try:
                    # Handle different date formats properly
                    if isinstance(exp_date_value, str):
                        # If it's a string, try to parse in different formats
                        from datetime import datetime
                        try:
                            # Try first with standard ISO format
                            parsed_date = datetime.strptime(exp_date_value, "%Y-%m-%d").date()
                            qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
                            if qdate.isValid():
                                self.expiration_date_input.setDate(qdate)
                        except ValueError:
                            # Try with QDate.fromString
                            qdate = QDate.fromString(exp_date_value, "yyyy-MM-dd")
                            if qdate.isValid():
                                self.expiration_date_input.setDate(qdate)
                            else:
                                # Try other common formats
                                try:
                                    parsed_date = datetime.strptime(exp_date_value, "%m/%d/%Y").date()
                                    qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
                                    if qdate.isValid():
                                        self.expiration_date_input.setDate(qdate)
                                except ValueError:
                                    # Fall back to default
                                    self.expiration_date_input.setDate(QDate.currentDate().addYears(1))
                    elif hasattr(exp_date_value, 'year') and hasattr(exp_date_value, 'month') and hasattr(exp_date_value, 'day'):
                        # If it's a date or datetime object, convert directly to QDate
                        qdate = QDate(exp_date_value.year, exp_date_value.month, exp_date_value.day)
                        if qdate.isValid():
                            self.expiration_date_input.setDate(qdate)
                        else:
                            self.expiration_date_input.setDate(QDate.currentDate().addYears(1))
                    else:
                        # Unknown format, use default
                        self.expiration_date_input.setDate(QDate.currentDate().addYears(1))
                except Exception as e:
                    print(f"Error setting expiration date: {e}, value was {exp_date_value} of type {type(exp_date_value)}")
                    # Fall back to default (today + 1 year)
                    self.expiration_date_input.setDate(QDate.currentDate().addYears(1))
            else:
                # No expiration date provided, use default
                self.expiration_date_input.setDate(QDate.currentDate().addYears(1))

            # Load image preview
            if self.selected_image_path and os.path.exists(self.selected_image_path):
                pixmap = load_product_image(self.selected_image_path, target_size=(120, 120))
                self.image_preview_label.setPixmap(pixmap)
                self.image_preview_label.setText("")  # Clear "No Image" text
            else:
                self.image_preview_label.clear()
                self.image_preview_label.setText("No Image Selected")

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.gif *.bmp *.svg)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            filenames = file_dialog.selectedFiles()
            if filenames:
                self.selected_image_path = filenames[0]
                pixmap = load_product_image(self.selected_image_path, target_size=(120, 120))
                self.image_preview_label.setPixmap(pixmap)
                self.image_preview_label.setText("")  # Clear "No Image" text

    def clear_image(self):
        self.selected_image_path = None
        self.image_preview_label.clear()
        self.image_preview_label.setText("No Image Selected")
        self.image_preview_label.setPixmap(load_product_image(None, target_size=(120, 120)))  # Show placeholder

    def get_product_data(self):
        name = self.name_input.text().strip()
        brand = self.brand_input.text().strip()  # Get brand
        category_id = self.category_combo.currentData()
        price = self.price_input.value()
        stock = self.stock_input.value()
        min_stock_level = self.min_stock_input.value()
        expiration_date = self.expiration_date_input.date().toString("yyyy-MM-dd")

        if not name:
            QMessageBox.warning(self, "Input Error", "Product Name cannot be empty.")
            return None
        if category_id is None or category_id == -1:
            QMessageBox.warning(self, "Input Error", "Please select a category.")
            return None
        if not brand:
            QMessageBox.warning(self, "Input Error", "Brand cannot be empty.")
            return None

        return {
            'name': name,
            'brand': brand,  # Return brand
            'category_id': category_id,
            'price': price,
            'stock': stock,
            'image_path': self.selected_image_path,
            'expiration_date': expiration_date,
            'min_stock_level': min_stock_level
        }

def load_product_image(image_path, target_size=(150, 150), keep_aspect_ratio=True):
    """
    Load a product image from path and scale it to target size.
    If path is invalid or none provided, returns a default placeholder.
    
    Args:
        image_path: Path to the image file
        target_size: Tuple of (width, height) for the displayed image
        keep_aspect_ratio: Whether to preserve aspect ratio
        
    Returns:
        QPixmap object scaled to the target size
    """
    placeholder_path = os.path.join("assets", "images", "no-image.png")
    
    if not image_path or not os.path.exists(image_path):
        # Use placeholder image
        if os.path.exists(placeholder_path):
            pixmap = QPixmap(placeholder_path)
        else:
            # Create a blank pixmap if placeholder doesn't exist
            pixmap = QPixmap(target_size[0], target_size[1])
            pixmap.fill(Qt.GlobalColor.transparent)
    else:
        # Load actual image
        pixmap = QPixmap(image_path)
        
    # Scale the image
    if not pixmap.isNull():
        if keep_aspect_ratio:
            pixmap = pixmap.scaled(target_size[0], target_size[1], 
                                  Qt.AspectRatioMode.KeepAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
        else:
            pixmap = pixmap.scaled(target_size[0], target_size[1], 
                                  Qt.AspectRatioMode.IgnoreAspectRatio, 
                                  Qt.TransformationMode.SmoothTransformation)
    
    return pixmap