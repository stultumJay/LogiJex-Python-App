import os
import shutil
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import uuid

def get_product_image_dir():
    """Get the directory for storing product images"""
    return os.path.join("assets", "product_images")

def ensure_image_dir():
    """Ensure the product images directory exists"""
    os.makedirs(get_product_image_dir(), exist_ok=True)

def copy_image_to_assets(source_path):
    """
    Copy an image to the product images directory
    
    Args:
        source_path (str): The path to the source image
        
    Returns:
        str: The path to the copied image relative to the application root
    """
    if not source_path or not os.path.exists(source_path):
        return None
        
    # Ensure the product images directory exists
    ensure_image_dir()
    
    # Generate a unique filename for the image
    _, extension = os.path.splitext(source_path)
    filename = f"{uuid.uuid4().hex}{extension}"
    
    # Create the destination path
    dest_path = os.path.join(get_product_image_dir(), filename)
    
    # Copy the image
    try:
        shutil.copy2(source_path, dest_path)
        return os.path.join("assets", "product_images", filename)
    except Exception as e:
        print(f"Error copying image: {e}")
        return None

def get_scaled_pixmap(image_path, width=64, height=64):
    """
    Get a scaled pixmap from an image path
    
    Args:
        image_path (str): The path to the image
        width (int): The desired width of the pixmap
        height (int): The desired height of the pixmap
        
    Returns:
        QPixmap: A scaled pixmap of the image, or a placeholder if the image is not found
    """
    pixmap = QPixmap()
    
    if image_path and os.path.exists(image_path):
        pixmap.load(image_path)
        if not pixmap.isNull():
            return pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    # Return a placeholder pixmap if the image is not found
    return get_placeholder_pixmap(width, height)

def get_placeholder_pixmap(width=64, height=64):
    """
    Create a placeholder pixmap for products without images
    
    Args:
        width (int): The width of the placeholder
        height (int): The height of the placeholder
        
    Returns:
        QPixmap: A placeholder pixmap
    """
    # Create a blank image
    image = QImage(width, height, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.lightGray)
    
    return QPixmap.fromImage(image)

def delete_product_image(image_path):
    """
    Delete a product image
    
    Args:
        image_path (str): The path to the image
        
    Returns:
        bool: True if the image was deleted, False otherwise
    """
    if not image_path or not os.path.exists(image_path):
        return False
        
    try:
        os.remove(image_path)
        return True
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False 