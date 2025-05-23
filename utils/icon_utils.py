# icon_utils.py
#
# This module provides utility functions for loading and manipulating icons, specifically SVGs.
# It focuses on loading SVG files from a designated assets directory and allows for basic
# color manipulation by replacing the 'currentColor' stroke property within the SVG content.
#
# Usage: Imported by UI modules that need to display icons, particularly if dynamic coloring
# of SVG icons is required.
#
# Helper modules: Uses os for path manipulation, PyQt6.QtGui (QIcon, QPixmap) and
# PyQt6.QtCore (QByteArray) for handling icon data and display.

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QByteArray # Required for loading QPixmap from SVG string bytes.
import os

def get_icon(icon_name, color=None):
    """
    Load an SVG icon from the 'assets/icons' directory and optionally apply a color.
    If a color is provided, the function attempts to replace 'stroke="currentColor"'
    in the SVG file content with the specified color.

    Args:
        icon_name (str): The name of the icon file (without the .svg extension).
                         Example: "user", "settings", "trash-2".
        color (str, optional): A color string (e.g., "#FF0000" for red, "blue") to apply to the icon.
                               If None, the icon is loaded as is.
        
    Returns:
        QIcon: The loaded QIcon object. Returns an empty QIcon if the file is not found.
    """
    # Construct the full path to the SVG icon file.
    icon_path = os.path.join("assets", "icons", f"{icon_name}.svg")
    
    # Check if the icon file exists at the constructed path.
    if not os.path.exists(icon_path):
        # If the file doesn't exist, print a warning and return an empty QIcon.
        print(f"Warning: Icon {icon_path} not found")
        return QIcon() # Fallback to an empty icon.
        
    # If a color is specified, attempt to modify the SVG content.
    if color:
        try:
            # Read the SVG file content.
            with open(icon_path, 'r') as f:
                svg_content = f.read()
            
            # Replace the placeholder 'stroke="currentColor"' with the specified color.
            # This is a common convention in SVG icons designed for theming.
            svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
            
            # Convert the modified SVG string content to bytes.
            svg_bytes = QByteArray(svg_content.encode('utf-8'))
            # Create a QPixmap and load the SVG data from bytes.
            pixmap = QPixmap()
            if pixmap.loadFromData(svg_bytes):
                # If loading to pixmap is successful, create QIcon from it.
                return QIcon(pixmap)
            else:
                # If loading from modified SVG bytes fails, print a warning and load the original icon.
                print(f"Warning: Could not load modified SVG for {icon_name} with color {color}. Loading original.")
                return QIcon(icon_path)
        except Exception as e:
            # If any error occurs during file reading or processing, print a warning and load original.
            print(f"Error processing SVG {icon_name} with color {color}: {e}. Loading original.")
            return QIcon(icon_path) # Fallback to original icon on error.
    else:
        # If no color is specified, load the icon directly from the file path.
        return QIcon(icon_path) 