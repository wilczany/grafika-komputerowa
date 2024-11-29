from PySide6.QtWidgets import QScrollArea, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

class ImageViewerWidget(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.setWidget(self.image_label)

    def set_image(self, image_path):
        image = QImage(image_path)
        if image.isNull():
            print(f"Failed to load image: {image_path}")
            return
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)