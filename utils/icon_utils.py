from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QByteArray
import os

def get_icon(icon_name, color=None):
    """
    Load an SVG icon from the assets/icons directory
    
    Args:
        icon_name (str): The name of the icon file without the .svg extension
        color (str, optional): Color to apply to the icon
        
    Returns:
        QIcon: The loaded icon
    """
    icon_path = os.path.join("assets", "icons", f"{icon_name}.svg")
    
    if not os.path.exists(icon_path):
        print(f"Warning: Icon {icon_path} not found")
        return QIcon()
        
    if color:
        # If a color is specified, replace the stroke color in the SVG
        with open(icon_path, 'r') as f:
            svg_content = f.read()
            
        # Replace stroke color
        svg_content = svg_content.replace('stroke="currentColor"', f'stroke="{color}"')
        
        # Convert modified SVG to QIcon
        svg_bytes = QByteArray(svg_content.encode('utf-8'))
        pixmap = QPixmap()
        pixmap.loadFromData(svg_bytes)
        return QIcon(pixmap)
    else:
        # Simply load the icon directly
        return QIcon(icon_path) 