from PySide6.QtWidgets import QWidget, QScrollArea, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage, QPixmap, QPainter, QColor, QFont
import numpy as np

class ImageViewerWidget(QScrollArea):
    def __init__(self):
        super().__init__()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.image_label)
        self.setWidgetResizable(True)
        
        self.image_data = None
        self.zoom_factor = 4.0  # Set initial zoom factor to 4.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        
        # For pixel value display
        self.show_pixel_values = False
        self.last_mouse_pos = QPoint()        

        
    def set_image(self, image_data):
        self.image_data = image_data
        self.zoom_factor = 4.0  # Reset zoom factor when a new image is set
        self.update_view()
        
    def has_image(self):
        return self.image_data is not None
        
    def get_image(self):
        return self.image_data
        
    def update_view(self):
        if self.image_data is None:
            return
            
        pixmap = QPixmap.fromImage(self.image_data)
        # scaled_pixmap = pixmap.scaled(
        #     pixmap.width() * self.zoom_factor,
        #     pixmap.height() * self.zoom_factor,
        #     Qt.KeepAspectRatio,
        #     Qt.SmoothTransformation
        # )
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        # if self.zoom_factor >= 4.0:  # Show pixel values when zoomed in
        #     self.show_pixel_values = True
        #     scaled_pixmap = self.draw_pixel_values(scaled_pixmap)
        # else:
        #     self.show_pixel_values = False
            
        self.image_label.setPixmap(scaled_pixmap)
        
    def draw_pixel_values(self, pixmap):
        if self.image_data is None:
            return pixmap
            
        painter = QPainter(pixmap)
        painter.setFont(QFont("Arial", 8))
        
        pixel_size = int(self.zoom_factor)
        height, width = self.image_data.shape[:2]
        
        for y in range(height):
            for x in range(width):
                screen_x = int(x * self.zoom_factor)
                screen_y = int(y * self.zoom_factor)
                
                r, g, b = self.image_data[y, x]
                text = f"R:{r}\nG:{g}\nB:{b}"
                
                # Choose text color based on background brightness
                brightness = (r + g + b) / 3
                text_color = Qt.white if brightness < 128 else Qt.black
                
                painter.setPen(text_color)
                painter.drawText(
                    screen_x,
                    screen_y,
                    pixel_size,
                    pixel_size,
                    Qt.AlignCenter,
                    text
                )
                
        painter.end()
        return pixmap
        
    def zoom_in(self):
        if self.zoom_factor * 1.2 <= self.max_zoom:
            self.zoom_factor *= 1.2
            self.update_view()
            
    def zoom_out(self):
        if self.zoom_factor / 1.2 >= self.min_zoom:
            self.zoom_factor /= 1.2
            self.update_view()
            
