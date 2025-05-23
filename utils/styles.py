# utils/styles.py
#
# This module centralizes all PyQt6 stylesheet definitions for the application.
# It uses an AppConfig class (from utils.config) to access theme colors and font settings,
# promoting consistency and ease of theming across the entire UI.
#
# The module provides:
#   - `get_global_stylesheet()`: A comprehensive stylesheet for base elements like QMainWindow,
#     sidebars, QTableWidget, QPushButton, QLineEdit, QComboBox, QScrollArea, etc.
#   - Specific stylesheets for dashboard cards (`get_dashboard_card_style`), admin/manager/retailer
#     dashboards, product cards (`get_product_card_style`), category cards, and dialogs.
#   - `apply_table_styles()`: A helper function to apply detailed styling and behavior
#     (like row height, header font, alternating colors, column resizing) to QTableWidget instances.
#
# Usage: Stylesheets are typically fetched by the main window or specific widgets during their
# initialization and applied using `setStyleSheet()` or by calling `apply_table_styles()`.
#
# Helper modules: Uses utils.config (AppConfig) for all color and font definitions.
# Uses PyQt6.QtWidgets (QTableWidget, QHeaderView), PyQt6.QtGui (QFont, QColor, QBrush),
# and PyQt6.QtCore (Qt) for type hinting and specific Qt constants/classes.

from utils.config import AppConfig # For accessing theme colors and font settings.
from PyQt6.QtWidgets import QTableWidget, QHeaderView # For type hinting and header view modes.
from PyQt6.QtGui import QFont, QColor, QBrush # For font definitions and color handling.
from PyQt6.QtCore import Qt # For Qt.AlignmentFlag and other Qt enum/constants.

def get_global_stylesheet():
    """Returns the global stylesheet string for the entire application.
    This stylesheet defines the base appearance for common Qt widgets, ensuring a consistent look and feel.
    It leverages AppConfig for colors and font properties.
    """
    return f"""
    /* --- QMainWindow --- */
    QMainWindow {{
        background-color: {AppConfig.BACKGROUND_COLOR}; /* Main window background */
        color: {AppConfig.TEXT_COLOR}; /* Default text color */
        font-family: {AppConfig.FONT_FAMILY}; /* Default font family */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt; /* Default font size */
    }}

    /* --- Sidebar Styling (identified by #sidebar objectName) --- */
    #sidebar {{
        background-color: {AppConfig.DARK_BACKGROUND}; /* Sidebar distinct background */
        border-right: 1px solid rgba(255,255,255,0.1); /* Subtle right border */
    }}
    #sidebar QPushButton {{ /* Styling for buttons within the sidebar */
        background-color: transparent; /* Transparent background by default */
        color: {AppConfig.TEXT_COLOR_ALT}; /* Alternative text color for less emphasis */
        border: none; /* No border for sidebar buttons */
        padding: 15px 10px; /* Generous padding for larger clickable area */
        text-align: left; /* Align text to the left */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        border-radius: 0px; /* No rounded corners for a flush look */
        margin: 2px 0px; /* Small vertical margin between buttons */
    }}
    #sidebar QPushButton:hover {{ /* Hover state for sidebar buttons */
        background-color: rgba(255,255,255,0.1); /* Slight highlight on hover */
        color: {AppConfig.LIGHT_TEXT}; /* Brighter text on hover */
    }}
    #sidebar QPushButton:checked {{ /* Styling for the active/checked sidebar button */
        background-color: rgba(255,255,255,0.2); /* Darker highlight for active state */
        border-left: 3px solid {AppConfig.PRIMARY_COLOR}; /* Accent color indicator on the left */
        font-weight: bold; /* Bold text for active button */
        color: {AppConfig.LIGHT_TEXT}; /* Bright text for active button */
    }}

    /* --- Main Content Area (identified by #contentArea objectName) --- */
    #contentArea {{
        background-color: {AppConfig.BACKGROUND_COLOR}; /* Matches main window background */
        padding: 10px; /* Padding around the content */
    }}

    /* --- User Name Label in Header (identified by #userNameLabel objectName) --- */
    QLabel#userNameLabel {{
        color: {AppConfig.LIGHT_TEXT};
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        padding: 10px;
    }}

    /* --- General QTableWidget Styling --- */
    /* This can be applied globally or specifically using apply_table_styles() */
    QTableWidget {{
        background-color: {AppConfig.CARD_BACKGROUND}; /* Table background color */
        color: {AppConfig.TEXT_COLOR}; /* Table text color */
        border: 1px solid {AppConfig.BORDER_COLOR}; /* Border around the table */
        gridline-color: rgba(255,255,255,0.1); /* Color for grid lines */
        selection-background-color: {AppConfig.PRIMARY_COLOR}; /* Background of selected cells */
        selection-color: white; /* Text color of selected cells */
        border-radius: 8px; /* Rounded corners for the table */
    }}
    QTableWidget::item {{ /* Styling for individual table cells (items) */
        padding: 8px 5px; /* Padding within cells, increases row height */
        border-bottom: 1px solid rgba(255,255,255,0.05); /* Subtle separator line between rows */
    }}
    QTableWidget QHeaderView::section {{ /* Styling for table header sections */
        background-color: {AppConfig.PRIMARY_COLOR}; /* Header background color */
        color: {AppConfig.LIGHT_TEXT}; /* Header text color */
        padding: 8px; /* Padding within header sections, increases header height */
        border: none; /* No default border */
        border-right: 1px solid rgba(255,255,255,0.1); /* Separator line to the right */
        border-bottom: 1px solid rgba(255,255,255,0.1); /* Separator line at the bottom */
        font-weight: bold; /* Bold header text */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QTableWidget QHeaderView::section:last-child {{ /* Remove right border from the last header section */
        border-right: none;
    }}

    /* --- General QPushButton Styling --- */
    QPushButton {{
        background-color: {AppConfig.PRIMARY_COLOR};
        color: {AppConfig.LIGHT_TEXT};
        border: none;
        border-radius: 5px; /* Rounded corners */
        padding: 8px 15px; /* Padding inside buttons */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        font-weight: 500; /* Medium font weight */
    }}
    QPushButton:hover {{
        background-color: {AppConfig.SECONDARY_COLOR}; /* Change color on hover */
    }}
    QPushButton:pressed {{ /* Style when button is pressed */
        background-color: {AppConfig.PRIMARY_COLOR}; /* Can revert or use a darker shade */
        border: 1px solid {AppConfig.LIGHT_TEXT}; /* Optional pressed border */
    }}
    QPushButton:disabled {{ /* Style for disabled buttons */
        background-color: #555; /* Darker, muted background */
        color: #bbb; /* Lighter, muted text */
    }}

    /* --- General Input Field Styling (QLineEdit, QComboBox, QSpinBox, QDateEdit) --- */
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND}; /* Background for input fields */
        border: 1px solid {AppConfig.BORDER_COLOR}; /* Border for input fields */
        border-radius: 5px; /* Rounded corners */
        padding: 6px; /* Padding inside input fields */
        color: {AppConfig.TEXT_COLOR}; /* Text color inside input fields */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus, QDateEdit:focus {{ /* Style when input field has focus */
        border: 1px solid {AppConfig.PRIMARY_COLOR}; /* Highlight border with primary color */
    }}
    /* Styling for QComboBox dropdown arrow */
    QComboBox::drop-down {{
        border: 0px; /* No border for the dropdown button part */
    }}
    QComboBox::down-arrow {{
        image: url(assets/icons/chevron-down.png); /* Path to dropdown arrow icon */
        width: 16px;
        height: 16px;
    }}
    /* Styling for QDateEdit dropdown arrow (calendar icon) */
    QDateEdit::drop-down {{
        border: 0px;
    }}
    QDateEdit::down-arrow {{
        image: url(assets/icons/calendar.png); /* Path to calendar icon */
        width: 16px;
        height: 16px;
    }}

    /* --- QScrollArea and QScrollBar Styling --- */
    QScrollArea {{
        background-color: transparent; /* Transparent background for scroll area widget itself */
        border: none; /* No border for scroll area */
    }}
    /* Vertical ScrollBar */
    QScrollBar:vertical {{
        border: none;
        background: rgba(255, 255, 255, 0.05); /* Background of the scrollbar track */
        width: 10px; /* Width of the vertical scrollbar */
        margin: 0px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{ /* The draggable part of the scrollbar */
        background: rgba(255, 255, 255, 0.2); /* Handle color */
        min-height: 20px; /* Minimum height of the handle */
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: rgba(255, 255, 255, 0.3); /* Handle color on hover */
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ /* Hide add/sub line buttons */
        height: 0px;
    }}
    /* Horizontal ScrollBar */
    QScrollBar:horizontal {{
        border: none;
        background: rgba(255, 255, 255, 0.05);
        height: 10px; /* Height of the horizontal scrollbar */
        margin: 0px;
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal {{
        background: rgba(255, 255, 255, 0.2);
        min-width: 20px; /* Minimum width of the handle */
        border-radius: 5px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ /* Hide add/sub line buttons */
        width: 0px;
    }}
    """

def get_dashboard_card_style(color):
    """Returns a stylesheet string for a general dashboard summary card.
    These cards are typically used to display key metrics (e.g., total sales, user count).
    They feature a gradient background based on the provided color.

    Args:
        color (str): The base hex color string for the card's gradient background.
    Returns:
        str: Stylesheet string for a QFrame with class 'dashboard-card'.
    """
    # QColor(color).lighter(120).name() creates a lighter shade of the base color for the gradient.
    return f"""
    QFrame.dashboard-card {{ /* Selects QFrame widgets with the 'dashboard-card' dynamic property or class */
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                    stop:0 {color}, 
                                    stop:1 {QColor(color).lighter(120).name()}); /* Horizontal gradient */
        border-radius: 12px; /* Rounded corners */
        padding: 15px; /* Padding inside the card */
        margin: 5px; /* Margin around the card */
        min-width: 180px; /* Minimum width */
        min-height: 120px; /* Minimum height */
        border: 1px solid rgba(255,255,255,0.1); /* Subtle border */
    }}
    QLabel {{ /* General QLabel styling within these cards */
        color: {AppConfig.LIGHT_TEXT}; /* Light text color for readability on dark/colored backgrounds */
    }}
    QLabel.card-title {{ /* QLabel for the card's title */
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    QLabel.card-value {{ /* QLabel for the card's main value/metric */
        font-size: {AppConfig.FONT_SIZE_XXLARGE}pt;
        font-weight: bold;
    }}
    """

def get_admin_dashboard_style():
    """Returns a stylesheet string for elements specific to the Admin Dashboard.
    This can be used to apply styles to the main widget of the Admin Dashboard (e.g., QWidget#AdminDashboardWidget)
    and its specific components like titles or cards if they need unique styling beyond the general card style.
    """
    return f"""
    QWidget#AdminDashboardWidget {{ /* Style for the main AdminDashboardWidget (if objectName is set) */
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{ /* Styling for QLabel elements used as headers (using rich text <h1>, <h2>) */
        color: {AppConfig.PRIMARY_COLOR}; /* Primary color for admin headers */
        font-weight: bold;
    }}
    /* Overriding general card style if needed for admin dashboard specifically */
    /* QFrame.dashboard-card (within AdminDashboardWidget context if nested) ... */
    QFrame.dashboard-card {{ /* Default styling for cards if not using get_dashboard_card_style with specific colors */
        background-color: {AppConfig.CARD_BACKGROUND};
        border-radius: 10px;
        padding: 15px;
        border: 1px solid {AppConfig.BORDER_COLOR};
    }}
    """

def get_manager_dashboard_style():
    """Returns a stylesheet string for elements specific to the Manager Dashboard.
    Similar to the admin dashboard style but might use different accent colors (e.g., SECONDARY_COLOR).
    """
    return f"""
    QWidget#ManagerDashboardWidget {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{
        color: {AppConfig.SECONDARY_COLOR}; /* Secondary color for manager headers */
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
    """Returns a stylesheet string for elements specific to the Retailer Dashboard.
    Might use a different accent color (e.g., HIGHLIGHT_COLOR).
    """
    return f"""
    QWidget#RetailerDashboardWidget {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        color: {AppConfig.TEXT_COLOR};
    }}
    QLabel h1, QLabel h2 {{
        color: {AppConfig.HIGHLIGHT_COLOR}; /* Highlight color for retailer headers */
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
    """Returns a detailed stylesheet string for individual product cards,
    typically used in a grid or list view in product management UIs.
    This style defines the appearance of product title, details, price, status, and action buttons.
    """
    return f"""
    QFrame#productCard {{ /* Style for QFrame with objectName 'productCard' */
        background-color: #2b2e3b; /* Dark card background */
        border: 1px solid rgba(255,255,255,0.15); /* Subtle border */
        border-radius: 10px;
        padding: 12px;
        margin: 5px;
        /* box-shadow: 0 2px 6px rgba(0,0,0,0.2); */ /* Removed unsupported property as it causes warnings */
    }}
    QFrame#productCard:hover {{ /* Hover effect for product cards */
        border: 1px solid {AppConfig.PRIMARY_COLOR}; /* Highlight border on hover */
        background-color: #343747; /* Slightly lighter background on hover */
    }}
    /* General QLabel styling within product cards */
    QLabel {{
        color: #f8f8f2; /* Light text color (Dracula theme inspired) */
    }}
    QLabel.product-title {{ /* Class for product title QLabel */
        font-size: {AppConfig.FONT_SIZE_MEDIUM}pt;
        font-weight: bold;
        color: #8be9fd; /* Bright cyan for title */
        margin-top: 5px;
        margin-bottom: 2px;
    }}
    QLabel.product-detail {{ /* Class for product detail QLabels (brand, category, stock) */
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        color: #f8f8f2;
        margin: 1px 0;
    }}
    QLabel.product-price {{ /* Class for product price QLabel */
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        font-weight: bold;
        color: #bd93f9; /* Purple for price */
        background-color: rgba(189, 147, 249, 0.1); /* Subtle background for price */
        border-radius: 4px;
        padding: 2px 5px;
        margin: 3px 0;
    }}
    /* Status label styling based on product status */
    QLabel.status-in-stock {{
        color: #50fa7b; /* Green for in stock */
        font-weight: bold;
    }}
    QLabel.status-low-stock {{
        color: #f1fa8c; /* Yellow for low stock */
        font-weight: bold;
    }}
    QLabel.status-no-stock {{
        color: #ff5555; /* Red for no stock */
        font-weight: bold;
    }}
    /* QPushButton styling within product cards (e.g., Edit, Delete buttons) */
    QPushButton {{
        background-color: #44475a; /* Darker button background */
        color: #f8f8f2;
        border: none;
        border-radius: 5px;
        padding: 8px 12px;
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        margin-top: 5px;
    }}
    QPushButton:hover {{
        background-color: #6272a4; /* Lighter blue-purple on hover */
    }}
    QPushButton:pressed {{
        background-color: #51587b;
    }}
    /* Styling for specific containers within the product card if used */
    #infoContainer {{ /* e.g., a QFrame holding text details */
        background-color: #3b3e4f; /* Slightly lighter than main card background */
        border-radius: 5px;
        padding: 8px;
        margin-top: 5px;
    }}
    #image_container {{ /* e.g., a QLabel or QFrame holding the product image */
        background-color: #f8f8f2; /* White background for image area */
        border: 1px solid #44475a;
        border-radius: 5px;
    }}
    """

def get_category_card_style():
    """Returns a stylesheet string for category cards, used in category management UIs.
    These cards are simpler, typically displaying the category name.
    """
    return f"""
    QFrame.category-card {{ /* Selects QFrame with class 'category-card' */
        background-color: {AppConfig.CARD_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 10px;
        padding: 10px;
    }}
    QFrame.category-card:hover {{ /* Hover effect for category cards */
        border: 1px solid {AppConfig.PRIMARY_COLOR};
        background-color: rgba(108, 92, 231, 0.1); /* Subtle primary color tint on hover */
    }}
    QLabel.category-title {{ /* QLabel for the category name/title */
        font-weight: bold;
        font-size: {AppConfig.FONT_SIZE_LARGE}pt;
        color: {AppConfig.LIGHT_TEXT};
    }}
    """

def get_dialog_style():
    """Returns a general stylesheet string for QDialog windows.
    This ensures consistent styling for various dialogs like ProductDialog, CategoryDialog, UserDialog, MFADialog.
    """
    return f"""
    QDialog {{
        background-color: {AppConfig.BACKGROUND_COLOR};
        border-radius: 10px; /* Rounded corners for the dialog window */
        color: {AppConfig.TEXT_COLOR};
        font-family: {AppConfig.FONT_FAMILY};
    }}
    QLabel {{ /* General QLabel styling within dialogs */
        color: {AppConfig.TEXT_COLOR};
    }}
    /* Input field styling within dialogs (consistent with global input styles) */
    QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QDateEdit {{
        background-color: {AppConfig.INPUT_BACKGROUND};
        border: 1px solid {AppConfig.BORDER_COLOR};
        border-radius: 5px;
        padding: 6px;
        color: {AppConfig.TEXT_COLOR};
        font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
    }}
    /* QPushButton styling within dialogs (consistent with global button styles) */
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
    /* Specific styling for image preview label in ProductDialog (if objectName is set) */
    #imagePreviewLabel {{
        border: 1px dashed {AppConfig.PRIMARY_COLOR}; /* Dashed border to indicate drop area or preview */
        background-color: {AppConfig.INPUT_BACKGROUND};
        border-radius: 5px;
        /* Alignment etc. should be handled in widget code, not stylesheet for text */
    }}
    """

def apply_table_styles(table_widget: QTableWidget):
    """Applies a detailed and consistent set of styles and behaviors to a QTableWidget instance.
    This includes colors, fonts, row height, header properties, selection behavior, and alternating row colors.

    Args:
        table_widget (QTableWidget): The QTableWidget instance to be styled.
    """
    # Apply stylesheet for basic appearance (colors, borders, padding).
    table_widget.setStyleSheet(f"""
        QTableWidget {{
            background-color: {AppConfig.CARD_BACKGROUND};
            color: {AppConfig.TEXT_COLOR};
            border: 1px solid {AppConfig.BORDER_COLOR};
            gridline-color: rgba(255,255,255,0.1); /* Subtle grid lines */
            selection-background-color: {AppConfig.PRIMARY_COLOR}; /* Color for selected cells */
            selection-color: white; /* Text color for selected cells */
            border-radius: 8px;
        }}
        QTableWidget::item {{ /* Styling for individual cells */
            padding: 8px 5px; /* Padding for cell content, affects row height */
            border-bottom: 1px solid rgba(255,255,255,0.05); /* Subtle row separator */
            font-size: {AppConfig.FONT_SIZE_NORMAL}pt; /* Ensure item font size */
        }}
        QTableWidget QHeaderView::section {{ /* Styling for header sections */
            background-color: {AppConfig.PRIMARY_COLOR};
            color: {AppConfig.LIGHT_TEXT};
            padding: 8px;
            border: none;
            border-right: 1px solid rgba(255,255,255,0.1);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-weight: bold;
            font-size: {AppConfig.FONT_SIZE_NORMAL}pt;
        }}
        QTableWidget QHeaderView::section:last-child {{
            border-right: none; /* No right border for the last header section */
        }}
        QTableWidget::item:selected {{ /* Style for selected items */
            background-color: {AppConfig.PRIMARY_COLOR}; /* Use primary color for selection background */
            color: white; /* White text for selected items */
        }}
        /* QTableWidget::item:alternate is not standard, use setAlternatingRowColors(True) instead */
        /* However, if you want to manually style alternate rows via stylesheet for more control: */
        /* QTableWidget QAbstractItemView::item:alternate {{ background-color: #another_color; }} */
        /* This is often better handled by setAlternatingRowColors and palette or specific item delegates. */
    """)

    # Set default row height for better readability and touch-friendliness.
    table_widget.verticalHeader().setDefaultSectionSize(40) # Standard row height of 40 pixels.
    table_widget.verticalHeader().setVisible(False) # Typically, vertical row numbers are not needed.

    # Set font for horizontal (column) headers.
    header_font = QFont(AppConfig.FONT_FAMILY, AppConfig.FONT_SIZE_NORMAL, QFont.Weight.Bold)
    table_widget.horizontalHeader().setFont(header_font)
    # table_widget.verticalHeader().setFont(header_font) # If vertical header is visible and needs styling.

    # Enable alternating row colors for improved readability of tabular data.
    # The actual colors are often determined by the QPalette or can be further customized.
    table_widget.setAlternatingRowColors(True)

    # Configure horizontal header behavior.
    header = table_widget.horizontalHeader()
    # Set all columns to stretch initially to fill available width. Specific columns can be overridden later.
    for i in range(table_widget.columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
    
    # Ensure the last column stretches to fill any remaining space if other columns are fixed or interactive.
    header.setStretchLastSection(True)

    # Allow rows to be selected.
    table_widget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    # Allow only one row to be selected at a time.
    table_widget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
    # Disable direct editing of cells by double-clicking, if edits should go through dialogs.
    table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)