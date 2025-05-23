import os
import shutil
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import uuid

# image_utils.py
#
# This module provides a collection of utility functions for handling product images.
# It includes functions for ensuring the image directory exists, copying images to a
# standardized assets location with unique names, loading and scaling images for display (QPixmap),
# generating placeholder images, and deleting product images.
#
# Usage: Primarily used by product management UI and related dialogs that require
# image uploading, display, and deletion functionalities.
#
# Helper modules: Uses os, shutil, uuid for file and directory operations and unique ID generation.
# Uses PyQt6.QtGui (QPixmap, QImage) and PyQt6.QtCore (Qt) for image manipulation and display.

def get_product_image_dir():
    """Returns the designated directory path for storing product images.
    This path is relative to the application root (e.g., "assets/product_images").
    """
    # Define the standard sub-directory for product images within the 'assets' folder.
    return os.path.join("assets", "product_images")

def ensure_image_dir():
    """Ensures that the product images directory exists, creating it if necessary.
    This is typically called before attempting to save any images.
    """
    # Get the target directory path using the helper function.
    image_dir = get_product_image_dir()
    # Create the directory. os.makedirs() will not raise an error if the directory already exists (exist_ok=True).
    os.makedirs(image_dir, exist_ok=True)

def copy_image_to_assets(source_path):
    """
    Copies an image file from a given source path to the application's product images directory.
    It generates a unique filename using UUID to prevent overwrites and ensure uniqueness.
    
    Args:
        source_path (str): The full path to the source image file.
        
    Returns:
        str or None: The new relative path to the copied image within the application's assets
                     (e.g., "assets/product_images/unique_name.jpg"), or None if copying fails.
                     This relative path is suitable for storing in a database.
    """
    # Validate the source path.
    if not source_path or not os.path.exists(source_path):
        print(f"Source image path is invalid or does not exist: {source_path}")
        return None
        
    # Ensure the target directory for product images exists.
    ensure_image_dir()
    
    # Generate a unique filename to avoid conflicts and to anonymize original filenames.
    # Extracts the original file extension (e.g., ".png", ".jpg").
    _, extension = os.path.splitext(source_path)
    # Creates a filename like "uuid_hex_string.extension".
    filename = f"{uuid.uuid4().hex}{extension}"
    
    # Construct the full destination path within the product image directory.
    dest_path_absolute = os.path.join(get_product_image_dir(), filename)
    
    # Attempt to copy the image file.
    try:
        # shutil.copy2 preserves metadata like timestamps, shutil.copy only copies content.
        shutil.copy2(source_path, dest_path_absolute)
        # Construct the relative path to be stored (e.g., in a database).
        # This makes the path portable if the application root directory changes.
        relative_dest_path = os.path.join("assets", "product_images", filename)
        print(f"Image copied successfully to: {relative_dest_path}")
        return relative_dest_path
    except Exception as e:
        # Log any error during the copy operation.
        print(f"Error copying image from {source_path} to {dest_path_absolute}: {e}")
        return None

def get_scaled_pixmap(image_path, width=64, height=64):
    """
    Loads an image from the specified path and returns a QPixmap scaled to the given dimensions.
    If the image cannot be loaded or is not found, a placeholder pixmap is returned.
    Maintains aspect ratio while scaling.
    
    Args:
        image_path (str): The path to the image file.
        width (int): The target width for the scaled QPixmap.
        height (int): The target height for the scaled QPixmap.
        
    Returns:
        QPixmap: A scaled QPixmap of the image, or a placeholder QPixmap if loading fails.
    """
    pixmap = QPixmap() # Initialize an empty QPixmap.
    
    # Check if the image path is valid and the file exists.
    if image_path and os.path.exists(image_path):
        # Attempt to load the image into the QPixmap.
        if pixmap.load(image_path):
            # If loading is successful and the pixmap is not null (i.e., valid image data).
            if not pixmap.isNull():
                # Scale the pixmap, keeping aspect ratio and using smooth transformation for better quality.
                return pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            print(f"Failed to load image into QPixmap: {image_path}")
    else:
        if image_path:
             print(f"Image file not found at path: {image_path}")
    
    # If image loading failed or path was invalid, return a placeholder pixmap.
    return get_placeholder_pixmap(width, height)

def get_placeholder_pixmap(width=64, height=64):
    """
    Creates and returns a simple placeholder QPixmap, typically used when a product image is missing.
    It displays a light gray background.
    
    Args:
        width (int): The width of the placeholder pixmap.
        height (int): The height of the placeholder pixmap.
        
    Returns:
        QPixmap: A QPixmap object representing the placeholder image.
    """
    # Create a QImage with the specified dimensions and ARGB32 format (supports transparency).
    image = QImage(width, height, QImage.Format.Format_ARGB32)
    # Fill the image with a light gray color. Qt.GlobalColor provides predefined colors.
    image.fill(Qt.GlobalColor.lightGray)
    
    # Convert the QImage to QPixmap and return it.
    return QPixmap.fromImage(image)

def delete_product_image(image_path):
    """
    Deletes a product image file given its path (usually a relative path from app root).
    
    Args:
        image_path (str): The path to the image file to be deleted.
                          This can be an absolute path or a relative path from the application root.
                          Typically, this is the path stored in the database.
        
    Returns:
        bool: True if the image was successfully deleted, False otherwise.
    """
    # Validate the image path.
    if not image_path:
        print("No image path provided for deletion.")
        return False
    
    # If the path is relative, it's assumed to be relative to the current working directory (app root).
    # os.path.exists will handle both absolute and relative paths correctly in most contexts.
    if not os.path.exists(image_path):
        print(f"Image not found at path for deletion: {image_path}")
        return False
        
    # Attempt to delete the file.
    try:
        os.remove(image_path)
        print(f"Image deleted successfully: {image_path}")
        return True
    except Exception as e:
        # Log any error during the deletion.
        print(f"Error deleting image at {image_path}: {e}")
        return False