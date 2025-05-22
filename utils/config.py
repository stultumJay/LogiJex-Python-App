import os
    
class AppConfig:
    # --- General Colors ---
    BACKGROUND_COLOR = "#2C3E50"  # Dark blue-gray for main backgrounds
    DARK_BACKGROUND = "#23303E"   # Even darker for sidebars/headers
    CARD_BACKGROUND = "#34495E"   # Slightly lighter dark for cards/panels
    INPUT_BACKGROUND = "#3F5161"  # For input fields
    BORDER_COLOR = "#455D7A"      # Border color for UI elements

    # --- Text Colors ---
    TEXT_COLOR = "#ECF0F1"        # Light gray for general text on dark backgrounds
    LIGHT_TEXT = "#FFFFFF"        # Pure white for titles, important text
    TEXT_COLOR_ALT = "#BDC3C7"    # Slightly darker light gray for secondary text

    # --- Accent Colors ---
    PRIMARY_COLOR = "#6C5CE7"     # Vibrant purple/blue for main actions, highlights
    SECONDARY_COLOR = "#00B894"   # Teal/green for success, positive indicators
    ACCENT_COLOR = "#D63031"      # Red for errors, critical alerts
    HIGHLIGHT_COLOR = "#FDCB6E"   # Yellow/orange for warnings, low stock

    # --- Specific Card Colors (for Manager/Admin Dashboards) ---
    # These are examples, adjust as needed for visual distinction
    SALES_CARD_COLOR = "#FFA502"  # Orange/Gold for sales
    PRODUCTS_CARD_COLOR = "#2ED573" # Green for products
    USERS_CARD_COLOR = "#1E90FF"  # Blue for users
    LOW_STOCK_CARD_COLOR = "#FF6B6B" # Light Red for low stock
    EXPIRING_CARD_COLOR = "#A55EEA" # Purple for expiring items

    # --- Font Configuration ---
    FONT_FAMILY = "Inter" # Or a suitable sans-serif font
    FONT_SIZE_SMALL = 9
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_XLARGE = 18
    FONT_SIZE_XXLARGE = 24
    
    # --- MFA Configuration ---
    MFA_CODE_LENGTH = 6  # Length of the MFA verification code
    MFA_CODE_EXPIRY_MINUTES = 5  # MFA code expires after this many minutes
    MFA_CODE_EXPIRY_SECONDS = MFA_CODE_EXPIRY_MINUTES * 60  # For backward compatibility
    MFA_SENDER_EMAIL = 'noreply@inventorysystem.com'  # Default sender email
    
    # --- File Paths ---
    PRODUCT_IMAGE_DIR = "assets/product_images"  # Directory for product images
    
    # Make sure the product image directory exists
    os.makedirs(PRODUCT_IMAGE_DIR, exist_ok=True)