from PySide6.QtWidgets import QWidget, QScrollArea, QLabel,  QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout dla ImageViewer
        layout = QVBoxLayout(self)
        
        # ScrollArea dla większych obrazów
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Label do wyświetlania obrazu
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Ustawienie label wewnątrz ScrollArea
        self.scroll_area.setWidget(self.image_label)
        
        # Dodanie ScrollArea do layoutu
        layout.addWidget(self.scroll_area)
        
    def display_image(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)
