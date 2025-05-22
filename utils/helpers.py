import os
import shutil
import uuid
from PyQt6.QtGui import QIcon, QPixmap, QImage, QPainter, QFont, QColor
from PyQt6.QtCore import QSize, Qt, QRectF
from PyQt6.QtWidgets import QMessageBox
from utils.config import AppConfig


# Note: For SVG rendering with QIcon, you might need to ensure QtSvg is installed
# (e.g., `pip install PyQt6-QtSvg` if using PyQt6) and import QSvgRenderer.
# For simplicity, this function directly uses QIcon(path) which works for basic SVGs.

def get_feather_icon(icon_name, color=None, size=24):
    """
    Returns a QIcon by loading a PNG or SVG from the assets/icons/ directory.
    Parameters:
        icon_name (str): Name of the icon file without extension
        color (str, optional): Color to tint the icon if SVG
        size (int, optional): Size of the icon in pixels
    Returns:
        QIcon: Icon object ready to use in buttons or labels
    """
    icon_path_png = os.path.join("assets", "icons", f"{icon_name}.png")
    icon_path_svg = os.path.join("assets", "icons", f"{icon_name}.svg")

    if os.path.exists(icon_path_png):
        return QIcon(icon_path_png)
    elif os.path.exists(icon_path_svg):
        # QIcon can load SVG directly. For more advanced control (e.g., coloring SVG dynamically),
        # you'd render it to a QPixmap first.
        # Example for SVG rendering (requires PyQt6-QtSvg):
        # from PyQt6.QtSvg import QSvgRenderer
        # pixmap = QPixmap(size, size)
        # pixmap.fill(Qt.GlobalColor.transparent)
        # painter = QPainter(pixmap)
        # svg_renderer = QSvgRenderer(icon_path_svg)
        # svg_renderer.render(painter, QRectF(0, 0, size, size))
        # painter.end()
        # return QIcon(pixmap)
        return QIcon(icon_path_svg)
    else:
        # Fallback if icon is not found, show a warning or return an empty QIcon
        print(f"Warning: Icon '{icon_name}' not found in assets/icons/. Returning empty QIcon.")
        return QIcon()


def save_product_image(source_path):
    """
    Saves a product image to the designated directory with a unique filename.
    
    Parameters:
        source_path (str): Path to the source image file
        
    Returns:
        str or None: The new relative path to the saved image or None on failure
    """
    if not source_path:
        return None

    # Ensure the product image directory exists
    os.makedirs(AppConfig.PRODUCT_IMAGE_DIR, exist_ok=True)

    # Generate a unique filename
    file_extension = os.path.splitext(source_path)[1].lower()
    if not file_extension:
        QMessageBox.warning(None, "Image Error", "Could not determine file extension for the image.")
        return None

    # Ensure the extension includes the dot
    if file_extension and not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Limit extensions to common image formats
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    if file_extension not in valid_extensions:
        QMessageBox.warning(None, "Image Error", f"Unsupported image format: {file_extension}. Please use JPG, PNG, GIF or BMP.")
        return None

    unique_filename = f"{uuid.uuid4()}{file_extension}"
    destination_path = os.path.join(AppConfig.PRODUCT_IMAGE_DIR, unique_filename)

    try:
        # Make a copy of the image to the product images directory
        shutil.copy(source_path, destination_path)
        print(f"Image saved: {destination_path}")
        
        # Return relative path from the current working directory
        return os.path.relpath(destination_path, start=os.getcwd())
    except Exception as e:
        QMessageBox.critical(None, "Image Save Error", f"Failed to save image: {e}")
        return None


def delete_product_image(relative_path):
    """
    Deletes a product image given its relative path.
    
    Parameters:
        relative_path (str): Relative path to the image file to delete
    """
    if not relative_path:
        return

    # Construct the absolute path
    full_path = os.path.join(os.getcwd(), relative_path)
    if os.path.exists(full_path):
        try:
            os.remove(full_path)
            print(f"Deleted image: {full_path}")
        except Exception as e:
            print(f"Error deleting image {full_path}: {e}")
    else:
        print(f"Image not found for deletion: {full_path}")


def load_product_image(image_path, target_size=(100, 100), keep_aspect_ratio=True):
    """
    Loads a product image from the given path, scales it, and returns a QPixmap.
    Returns a placeholder if the image is not found or cannot be loaded.
    
    Parameters:
        image_path (str): Path to the image file
        target_size (tuple): Target size (width, height) for the scaled image
        keep_aspect_ratio (bool): Whether to preserve the aspect ratio when scaling
        
    Returns:
        QPixmap: Scaled image or placeholder
    """
    if image_path and os.path.exists(image_path):
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                if keep_aspect_ratio:
                    return pixmap.scaled(target_size[0], target_size[1], 
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                else:
                    return pixmap.scaled(target_size[0], target_size[1], 
                                      Qt.AspectRatioMode.IgnoreAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")

    # Placeholder image if file not found or invalid
    placeholder_pixmap = QPixmap(target_size[0], target_size[1])
    placeholder_pixmap.fill(Qt.GlobalColor.transparent)  # Make background transparent

    # Draw "No Image" text on placeholder
    painter = QPainter(placeholder_pixmap)
    # Use QColor for color conversion
    text_color = QColor(AppConfig.TEXT_COLOR)
    font_name = AppConfig.FONT_FAMILY.split(',')[0].strip()  # Get first font name
    
    painter.setPen(text_color)
    painter.setFont(QFont(font_name, 8))
    
    # Draw a border
    painter.setPen(Qt.GlobalColor.gray)
    painter.drawRect(0, 0, target_size[0]-1, target_size[1]-1)
    
    # Draw icon and text - use QColor here too
    painter.setPen(QColor(AppConfig.TEXT_COLOR))
    painter.drawText(placeholder_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image")
    painter.end()
    return placeholder_pixmap
