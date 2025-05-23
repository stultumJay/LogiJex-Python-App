# config.py
#
# This module defines the AppConfig class, which centralizes application-wide configurations.
# It includes color schemes for UI theming, font settings, MFA parameters, and file paths.
# Access these settings via AppConfig.PROPERTY_NAME.
#
# Usage: Imported by UI modules for consistent styling and by core modules for path/MFA settings.
#
# Helper modules: Uses os for directory creation.

import os
    
class AppConfig:
    """
    Centralized configuration class for the application.
    Stores UI theme colors, font settings, MFA parameters, and file paths.
    """
    
    # --- General Colors ---
    # Used for main backgrounds, sidebars, cards, inputs, and borders.
    BACKGROUND_COLOR = "#2C3E50"  # Dark blue-gray for main backgrounds
    DARK_BACKGROUND = "#23303E"   # Even darker for sidebars/headers
    CARD_BACKGROUND = "#34495E"   # Slightly lighter dark for cards/panels
    INPUT_BACKGROUND = "#3F5161"  # For input fields
    BORDER_COLOR = "#455D7A"      # Border color for UI elements

    # --- Text Colors ---
    # For general text, titles, and secondary text on dark backgrounds.
    TEXT_COLOR = "#ECF0F1"        # Light gray for general text on dark backgrounds
    LIGHT_TEXT = "#FFFFFF"        # Pure white for titles, important text
    TEXT_COLOR_ALT = "#BDC3C7"    # Slightly darker light gray for secondary text

    # --- Accent Colors ---
    # Used for primary actions, success/error indicators, and warnings.
    PRIMARY_COLOR = "#6C5CE7"     # Vibrant purple/blue for main actions, highlights
    SECONDARY_COLOR = "#00B894"   # Teal/green for success, positive indicators
    ACCENT_COLOR = "#D63031"      # Red for errors, critical alerts
    HIGHLIGHT_COLOR = "#FDCB6E"   # Yellow/orange for warnings, low stock

    # --- Specific Card Colors (for Manager/Admin Dashboards) ---
    # Example colors for different types of dashboard summary cards.
    SALES_CARD_COLOR = "#FFA502"  # Orange/Gold for sales
    PRODUCTS_CARD_COLOR = "#2ED573" # Green for products
    USERS_CARD_COLOR = "#1E90FF"  # Blue for users
    LOW_STOCK_CARD_COLOR = "#FF6B6B" # Light Red for low stock
    EXPIRING_CARD_COLOR = "#A55EEA" # Purple for expiring items

    # --- Font Configuration ---
    # Defines font family and various sizes for consistent typography.
    FONT_FAMILY = "Inter" # Or a suitable sans-serif font
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_XLARGE = 18
    FONT_SIZE_XXLARGE = 24
    
    # --- MFA Configuration ---
    # Parameters for Multi-Factor Authentication code generation and expiry.
    MFA_CODE_LENGTH = 6  # Length of the MFA verification code
    MFA_CODE_EXPIRY_MINUTES = 5  # MFA code expires after this many minutes
    MFA_CODE_EXPIRY_SECONDS = MFA_CODE_EXPIRY_MINUTES * 60  # For backward compatibility
    MFA_SENDER_EMAIL = 'noreply@inventorysystem.com'  # Default sender email for MFA codes
    
    # --- File Paths ---
    # Defines the directory for storing product images.
    PRODUCT_IMAGE_DIR = "assets/product_images"  # Directory for product images
    
    # Ensure the product image directory exists upon class definition.
    # This is called when the AppConfig class is first defined/imported.
    os.makedirs(PRODUCT_IMAGE_DIR, exist_ok=True)