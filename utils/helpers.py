# helpers.py
#
# This module provides various utility functions for the application, primarily focused on UI and file handling.
# It includes functions for loading icons, managing product images (saving, deleting, loading for display),
# and potentially other reusable helper routines for Qt-based UI elements.
#
# Usage: Imported by UI modules (e.g., product management, dialogs) to handle common tasks like
# icon loading or image processing.
#
# Helper modules: Uses os, shutil, uuid for file operations and unique ID generation.
# Uses PyQt6.QtGui, PyQt6.QtCore, PyQt6.QtWidgets for UI-related tasks (icons, pixmaps, message boxes).
# Uses utils.config (AppConfig) for application-specific configurations like image directories and colors.

import os
import shutil
import uuid
from PyQt6.QtGui import QIcon, QPixmap, QImage, QPainter, QFont, QColor
from PyQt6.QtCore import QSize, Qt, QRectF
from PyQt6.QtWidgets import QMessageBox
from utils.config import AppConfig


# --- Icon Loading Utility ---
# Note: For SVG rendering with QIcon, ensure QtSvg is installed (e.g., `pip install PyQt6-QtSvg`).
# The current implementation directly uses QIcon(path), which works for basic SVGs and PNGs.

def get_feather_icon(icon_name, color=None, size=24):
    """
    Returns a QIcon by loading a PNG or SVG from the assets/icons/ directory.
    This function attempts to load a .png first, then a .svg if the .png is not found.
    It provides a fallback empty QIcon and a console warning if no icon file is found.

    Parameters:
        icon_name (str): Name of the icon file without extension (e.g., "user", "plus-circle").
        color (str, optional): Color to tint the icon if it were an SVG being dynamically rendered.
                             Currently not used in direct QIcon loading of SVG/PNG but kept for potential future use.
        size (int, optional): Desired size of the icon in pixels. Not directly applied to QIcon itself
                            but can be used by the caller or in advanced SVG rendering.
    Returns:
        QIcon: Icon object ready to use in buttons or labels. Returns an empty QIcon if not found.
    """
    # Define paths for both PNG and SVG versions of the icon.
    icon_path_png = os.path.join("assets", "icons", f"{icon_name}.png")
    icon_path_svg = os.path.join("assets", "icons", f"{icon_name}.svg")

    # Prioritize PNG if it exists.
    if os.path.exists(icon_path_png):
        return QIcon(icon_path_png)  # Load PNG directly.
    # Fallback to SVG if PNG is not found.
    elif os.path.exists(icon_path_svg):
        # QIcon can load basic SVGs directly. For advanced control like dynamic coloring or resizing,
        # you would render the SVG to a QPixmap first using QSvgRenderer.
        # Example (requires PyQt6-QtSvg and `from PyQt6.QtSvg import QSvgRenderer`):
        # pixmap = QPixmap(size, size)
        # pixmap.fill(Qt.GlobalColor.transparent)
        # painter = QPainter(pixmap)
        # svg_renderer = QSvgRenderer(icon_path_svg)
        # svg_renderer.render(painter, QRectF(0, 0, size, size))
        # painter.end()
        # return QIcon(pixmap)
        return QIcon(icon_path_svg)  # Load SVG directly.
    else:
        # If neither PNG nor SVG is found, print a warning and return an empty QIcon.
        print(f"Warning: Icon '{icon_name}' not found in assets/icons/. Returning empty QIcon.")
        return QIcon() # Return an empty icon as a fallback.

# --- Product Image Management Utilities ---

def save_product_image(source_path):
    """
    Saves a product image from a given source path to the application's designated product image directory.
    It generates a unique filename using UUID to prevent naming conflicts.
    The function also validates the file extension.

    Parameters:
        source_path (str): The absolute or relative path to the source image file.
        
    Returns:
        str or None: The new relative path (from the application's root) to the saved image file
                     if successful, otherwise None. The path is suitable for storing in the database.
    """
    # Check if a source path was provided.
    if not source_path:
        return None # No source path, nothing to save.

    # Ensure the target directory for product images exists, creating it if necessary.
    # AppConfig.PRODUCT_IMAGE_DIR should define the relative path (e.g., "assets/product_images").
    os.makedirs(AppConfig.PRODUCT_IMAGE_DIR, exist_ok=True)

    # Extract the file extension from the source path.
    file_extension = os.path.splitext(source_path)[1].lower() # Get extension and convert to lowercase.
    if not file_extension:
        # If no extension, show a warning and abort.
        QMessageBox.warning(None, "Image Error", "Could not determine file extension for the image.")
        return None

    # Ensure the extension includes the leading dot (e.g., converts "png" to ".png").
    if file_extension and not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Validate against a list of common, supported image extensions.
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if file_extension not in valid_extensions:
        QMessageBox.warning(None, "Image Error", f"Unsupported image format: {file_extension}. Please use JPG, PNG, GIF or BMP.")
        return None

    # Generate a universally unique identifier (UUID) for the filename to ensure uniqueness.
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    # Construct the full destination path for the new image file.
    destination_path = os.path.join(AppConfig.PRODUCT_IMAGE_DIR, unique_filename)

    try:
        # Copy the source image file to the destination path.
        shutil.copy(source_path, destination_path)
        print(f"Image saved: {destination_path}") # Log successful save.
        
        # Return the relative path to the saved image, from the current working directory.
        # This path is typically what gets stored in the database.
        return os.path.relpath(destination_path, start=os.getcwd())
    except Exception as e:
        # If copying fails, show a critical error message and return None.
        QMessageBox.critical(None, "Image Save Error", f"Failed to save image: {e}")
        return None


def delete_product_image(relative_path):
    """
    Deletes a product image file given its relative path (as stored in the database).

    Parameters:
        relative_path (str): The relative path to the image file to be deleted.
                             This path is typically retrieved from the product's database record.
    """
    # Check if a relative path was provided.
    if not relative_path:
        return # No path, nothing to delete.

    # Construct the absolute path from the relative path and the current working directory.
    full_path = os.path.join(os.getcwd(), relative_path)
    # Check if the file exists at the constructed absolute path.
    if os.path.exists(full_path):
        try:
            # Attempt to remove the file.
            os.remove(full_path)
            print(f"Deleted image: {full_path}") # Log successful deletion.
        except Exception as e:
            # If deletion fails, print an error message to the console.
            print(f"Error deleting image {full_path}: {e}")
    else:
        # If the file does not exist, print a message to the console.
        print(f"Image not found for deletion: {full_path}")


def load_product_image(image_path, target_size=(100, 100), keep_aspect_ratio=True):
    """
    Loads a product image from the given path, scales it to the target size, and returns a QPixmap.
    If the image cannot be loaded or is not found, it returns a placeholder QPixmap with "No Image" text.

    Parameters:
        image_path (str): The absolute or relative path to the image file.
        target_size (tuple): A tuple (width, height) for the desired dimensions of the scaled QPixmap.
        keep_aspect_ratio (bool): If True, the image is scaled while maintaining its aspect ratio,
                                fitting within the target_size. If False, it's scaled to fill target_size exactly.
        
    Returns:
        QPixmap: The scaled QPixmap of the product image, or a placeholder QPixmap if loading fails.
    """
    # Check if an image path is provided and if the file exists.
    if image_path and os.path.exists(image_path):
        try:
            # Attempt to load the image into a QPixmap.
            pixmap = QPixmap(image_path)
            # Check if the pixmap was loaded successfully (is not null).
            if not pixmap.isNull():
                # Scale the pixmap based on the keep_aspect_ratio flag.
                if keep_aspect_ratio:
                    return pixmap.scaled(target_size[0], target_size[1], 
                                      Qt.AspectRatioMode.KeepAspectRatio, # Maintain aspect ratio.
                                      Qt.TransformationMode.SmoothTransformation) # Use smooth scaling.
                else:
                    return pixmap.scaled(target_size[0], target_size[1], 
                                      Qt.AspectRatioMode.IgnoreAspectRatio, # Ignore aspect ratio, fill target size.
                                      Qt.TransformationMode.SmoothTransformation) # Use smooth scaling.
        except Exception as e:
            # If any error occurs during loading or scaling, print it to the console.
            print(f"Error loading image {image_path}: {e}")

    # --- Placeholder Image Generation ---
    # This code executes if image_path is None, the file doesn't exist, or loading failed.
    
    # Create a new QPixmap with the target dimensions for the placeholder.
    placeholder_pixmap = QPixmap(target_size[0], target_size[1])
    placeholder_pixmap.fill(Qt.GlobalColor.transparent)  # Make the placeholder background transparent.

    # Initialize a QPainter to draw on the placeholder pixmap.
    painter = QPainter(placeholder_pixmap)
    
    # Set the text color using AppConfig (ensure AppConfig.TEXT_COLOR is a valid color string like "#RRGGBB").
    text_color = QColor(AppConfig.TEXT_COLOR) # Convert hex string to QColor.
    # Attempt to get the primary font family name from AppConfig.
    font_name = AppConfig.FONT_FAMILY.split(',')[0].strip()  # Get the first font name from a potential list (e.g., "Inter, sans-serif").
    
    # Set painter pen for text.
    painter.setPen(text_color)
    # Set painter font with specified family and small size.
    painter.setFont(QFont(font_name, 8))
    
    # Draw a border around the placeholder.
    painter.setPen(Qt.GlobalColor.gray) # Use a standard gray color for the border.
    painter.drawRect(0, 0, target_size[0]-1, target_size[1]-1) # Draw rectangle slightly inside the pixmap bounds.
    
    # Draw the "No Image" text, centered within the placeholder.
    # Re-set pen to text_color if it was changed for the border.
    painter.setPen(QColor(AppConfig.TEXT_COLOR))
    painter.drawText(placeholder_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image")
    
    # End painting operations.
    painter.end()
    return placeholder_pixmap # Return the generated placeholder.
