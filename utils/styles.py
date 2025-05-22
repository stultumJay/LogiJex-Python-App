# utils/styles.py
from utils.config import AppConfig
from PyQt6.QtWidgets import QTableWidget, QHeaderView
from PyQt6.QtGui import QFont, QColor, QBrush
from PyQt6.QtCore import Qt # Import Qt for alignment

def get_global_stylesheet():
    """Returns the global stylesheet for the entire application."""
    return f"""
    QMainWindow {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
        font-family: {AppConfig.FONT_FAMILY};
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    #sidebar {{
        background-color: {AppConfig.DARK_BACKGROUND}; 
        border-right: 1px solid rgba(255,255,255,0.1);
    }}
    #sidebar QPushButton {{
        background-color: transparent;
        color: {AppConfig.TEXT_COLOR_ALT};
        border: none;
        padding: 15px 10px;
        text-align: left;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        border-radius: 0px;
        margin: 2px 0px;
    }}
    #sidebar QPushButton:hover {{
        background-color: rgba(255,255,255,0.1);
        color: {AppConfig.LIGHT_TEXT};
    }}
    #sidebar QPushButton:checked {{
        background-color: rgba(255,255,255,0.2);
        border-left: 3px solid {AppConfig.PRIMARY_COLOR};
        font-weight: bold;
        color: {AppConfig.LIGHT_TEXT};
    }}
    #contentArea {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        padding: 10px;
    }}
    QLabel#userNameLabel {{
        color: {AppConfig.LIGHT_TEXT};
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        padding: 10px;
    }}

    /* General Table Styling (applied globally or via apply_table_styles) */
    QTableWidget {{
        background-color: {AppConfig.CARD_BACKGROUND};
        color: {AppConfig.TEXT_COLOR};
        border: 1px solid {AppConfig.BORDER_COLOR};
        gridline-color: rgba(255,255,255,0.1);
        selection-background-color: {AppConfig.PRIMARY_COLOR};
        selection-color: white;
        border-radius: 8px;
    }}
    QTableWidget::item {{
        padding: 8px 5px; /* Increased padding for cell height */
        border-bottom: 1px solid rgba(255,255,255,0.05); /* Subtle row separator */
    }}
    QTableWidget QHeaderView::section {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        padding: 8px; /* Increased padding for header height */
        border: none;
        border-right: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-weight: bold;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QTableWidget QHeaderView::section:last-child {{
        border-right: none;
    }}

    /* General Button Styles */
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {AppConfig.SECONDARY_COLOR};
    }}
    QPushButton:pressed {{
        background-color: {AppConfig.PRIMARY_COLOR};
        border: 1px solid {AppConfig.LIGHT_TEXT};
    }}
    QPushButton:disabled {{
        background-color: #555;
        color: #bbb;
    }}

    /* General Input Styles */
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 5px;
        padding: 6px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus, QDateEdit:focus {{
        border: 1px solid {AppConfig.PRIMARY_COLOR};
    }}
    QComboBox::drop-down {{
        border: 0px;
    }}
    QComboBox::down-arrow {{
        image: url(assets/icons/chevron-down.png); /* Ensure this path is correct */
        width: 16px;
        height: 16px;
    }}
    QDateEdit::drop-down {{
        border: 0px;
    }}
    QDateEdit::down-arrow {{
        image: url(assets/icons/calendar.png); /* You might need a calendar icon */
        width: 16px;
        height: 16px;
    }}

    /* ScrollArea Styling */
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        border: none;
        background: rgba(255, 255, 255, 0.05);
        width: 10px;
        margin: 0px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: rgba(255, 255, 255, 0.2);
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        border: none;
        background: rgba(255, 255, 255, 0.05);
        height: 10px;
        margin: 0px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background: rgba(255, 255, 255, 0.2);
        min-width: 20px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    """

def get_dashboard_card_style(color):
    """Returns stylesheet for a general dashboard summary card."""
    return f"""
    QFrame.dashboard-card {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 {color}, 
                                    stop:1 {QColor(color).lighter(120).name()}); /* Lighter shade for gradient */
        border-radius: 12px;
        padding: 15px;
        margin: 5px;
        min-width: 180px;
        min-height: 120px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    QLabel {{
        color: {AppConfig.LIGHT_TEXT};
    }}
    QLabel.card-title {{
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    QLabel.card-value {{
        font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
        font-weight: bold;
    }}
    """

def get_admin_dashboard_style():
    """Returns stylesheet for the Admin Dashboard specific elements."""
    return f"""
    QWidget#AdminDashboardWidget {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{
        color: {AppConfig.PRIMARY_COLOR};
        font-weight: bold;
    }}
    QFrame.dashboard-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {AppConfig.BORDER_COLOR};
    }}
    """

def get_manager_dashboard_style():
    """Returns stylesheet for the Manager Dashboard specific elements."""
    return f"""
    QWidget#ManagerDashboardWidget {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{
        color: {AppConfig.SECONDARY_COLOR}; /* Different accent for manager */
        font-weight: bold;
    }}
    QFrame.dashboard-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {AppConfig.BORDER_COLOR};
    }}
    """

def get_retailer_dashboard_style():
    """Returns stylesheet for the Retailer Dashboard specific elements."""
    return f"""
    QWidget#RetailerDashboardWidget {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{
        color: {AppConfig.HIGHLIGHT_COLOR}; /* Different accent for retailer */
        font-weight: bold;
    }}
    QFrame.dashboard-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {AppConfig.BORDER_COLOR};
    }}
    """

def get_product_card_style():
    """Returns stylesheet for product cards in ProductManagementWidget."""
    return f"""
    QFrame.product-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 10px;
        padding: 12px;
        margin: 5px;
    }}
    QFrame.product-card:hover {{
        border: 1px solid {AppConfig.PRIMARY_COLOR};
        background-color: rgba(108, 92, 231, 0.1); /* Subtle hover effect */
    }}
    QLabel.product-image {{
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        background-color: rgba(0,0,0,0.1);
        padding: 0;
        margin: 0;
    }}
    QLabel.product-title {{
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: bold;
        color: {AppConfig.LIGHT_TEXT};
        margin-top: 5px;
        margin-bottom: 2px;
    }}
    QLabel.product-detail {{
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        color: {AppConfig.TEXT_COLOR_ALT};
        margin: 1px 0;
    }}
    QLabel.product-price {{
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        color: {AppConfig.SECONDARY_COLOR};
        margin: 3px 0;
    }}
    QLabel.status-in-stock {{
        color: {AppConfig.SECONDARY_COLOR};
        font-weight: bold;
    }}
    QLabel.status-low-stock {{
        color: {AppConfig.HIGHLIGHT_COLOR};
        font-weight: bold;
    }}
    QLabel.status-no-stock {{
        color: {AppConfig.ACCENT_COLOR};
        font-weight: bold;
    }}
    QPushButton.card-button {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        margin-top: 5px;
    }}
    QPushButton.card-button:hover {{
        background-color: {AppConfig.SECONDARY_COLOR};
    }}
    #infoContainer {{
        background-color: rgba(255,255,255,0.05);
        border-radius: 5px;
        padding: 8px;
        margin-top: 5px;
    }}
    """

def get_category_card_style():
    """Returns stylesheet for category cards in CategoryManagementWidget."""
    return f"""
    QFrame.category-card {{
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 10px;
        padding: 10px;
    }}
    QFrame.category-card:hover {{
        border: 1px solid {AppConfig.PRIMARY_COLOR};
        background-color: rgba(108, 92, 231, 0.1);
    }}
    QLabel.category-title {{
        font-weight: bold;
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        color: {AppConfig.LIGHT_TEXT};
    }}
    """

def get_dialog_style():
    """Returns stylesheet for general dialog windows (ProductDialog, CategoryDialog, UserDialog, MFADialog)."""
    return f"""
    QDialog {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        border-radius: 10px;
        color: {AppConfig.TEXT_COLOR};
        font-family: {AppConfig.FONT_FAMILY};
    }}
    QLabel {{
        color: {AppConfig.TEXT_COLOR};
    }}
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 5px;
        padding: 6px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QPushButton:hover {{
        background-color: {AppConfig.SECONDARY_COLOR};
    }}
    #imagePreviewLabel {{ /* Specific for ProductDialog */
        border: 1px dashed {AppConfig.PRIMARY_COLOR};
        background-color: {AppConfig.INPUT_BACKGROUND};
        border-radius: 5px;
    }}
    """

def apply_table_styles(table_widget: QTableWidget):
    """Applies consistent styling and sizing to a QTableWidget."""
    table_widget.setStyleSheet(f"""
        QTableWidget {{
            background-color: {AppConfig.CARD_BACKGROUND};
            color: {AppConfig.TEXT_COLOR};
            border: 1px solid {AppConfig.BORDER_COLOR};
            gridline-color: rgba(255,255,255,0.1);
            selection-background-color: {AppConfig.PRIMARY_COLOR};
            selection-color: white;
            border-radius: 8px;
        }}
        QTableWidget::item {{
            padding: 8px 5px; /* Increased padding for cell height */
            border-bottom: 1px solid rgba(255,255,255,0.05); /* Subtle row separator */
            font-size: {AppConfig.FONT_SIZE_NORMAL}pt; /* Ensure item font size */
        }}
        QTableWidget QHeaderView::section {{
            background-color: {AppConfig.PRIMARY_COLOR};
            color: {AppConfig.LIGHT_TEXT};
            padding: 8px; /* Increased padding for header height */
            border: none;
            border-right: 1px solid rgba(255,255,255,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-weight: bold;
            font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        }}
        QTableWidget QHeaderView::section:last-child {{
            border-right: none;
        }}
        QTableWidget::item:selected {{
            background-color: {AppConfig.PRIMARY_COLOR};
            color: white;
        }}
        QTableWidget::item:alternate {{
            background-color: rgba(255,255,255,0.02); /* Subtle alternate row color */
        }}
    """)

    # Set default row height
    table_widget.verticalHeader().setDefaultSectionSize(40) # Ensure cells are tall enough

    # Set header font size
    header_font = QFont(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, QFont.Weight.Bold)
    table_widget.horizontalHeader().setFont(header_font)
    table_widget.verticalHeader().setFont(header_font) # Apply to vertical header too

    # Enable alternating row colors
    table_widget.setAlternatingRowColors(True)

    # Ensure column headers are fully visible and stretch appropriately
    header = table_widget.horizontalHeader()
    # Set all columns to stretch initially, then adjust specific ones if needed
    for i in range(table_widget.columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

    # If there's a last column that should stretch to fill space, ensure it
    header.setStretchLastSection(True)