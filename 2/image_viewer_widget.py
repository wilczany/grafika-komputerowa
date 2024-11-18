from PySide6.QtWidgets import QScrollArea, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

class ImageViewerWidget(QScrollArea):
            
    def __init__(self):

        super().__init__()
        self.viewed_image :QImage = None
        self.image :QImage = None
        self.pixmap = None
        self.current_zoom = 1.0
        self.target_min_size = 400 

        self.setMouseTracking(True)
        # self.imageLabel.setMouseTracking(True)

    def set_image(self, image: QImage):
        self.imageLabel = QLabel()
        self.imageLabel.setMouseTracking(True)
        self.image = image
        width = image.width()
        height = image.height()
        if width < self.target_min_size or height < self.target_min_size:
            width_zoom = self.target_min_size / width if width < self.target_min_size else 1
            height_zoom = self.target_min_size / height if height < self.target_min_size else 1
            self.current_zoom = max(width_zoom, height_zoom)
        else:
            self.current_zoom = 1.0
            
        self.update_zoom()

    def zoom_in(self):
        self.current_zoom *= 1.2
        self.update_zoom()


    def zoom_out(self):
        self.current_zoom /= 1.2
        self.update_zoom()

    def update_zoom(self):
        
        old_width = self.image.width()
        old_height = self.image.height()

        new_width = int(old_width * self.current_zoom)
        new_height = int(old_height * self.current_zoom)

        scaled_pixmap = QPixmap.fromImage(self.image.scaled(
            new_width,
            new_height,
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        ))
        
        self.imageLabel.setPixmap(scaled_pixmap)
        self.imageLabel.resize(scaled_pixmap.size())
        self.setWidget(self.imageLabel)


    def mouseMoveEvent(self, event):
        if not self.image:
            return

        # Get position relative to image
        pos = self.imageLabel.mapFrom(self, event.position().toPoint())
        
        # Convert to original image coordinates
        x = int(pos.x() / self.current_zoom)
        y = int(pos.y() / self.current_zoom)
        
        if (0 <= x < self.image.width() and 
            0 <= y < self.image.height()):
            color = self.image.pixelColor(x, y)
            rgb_text = f"RGB: ({color.red()}, {color.green()}, {color.blue()})"
            # Find main window
            main_window = self.window()
            if main_window:
                main_window.rgb_label.setText(rgb_text)
        else:
            main_window = self.window()
            if main_window:
                main_window.rgb_label.setText("RGB: ---")

    def has_image(self):
        return self.image is not None
    
    def get_image(self):
        return self.image