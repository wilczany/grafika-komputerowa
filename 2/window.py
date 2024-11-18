from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtWidgets import QPushButton, QFileDialog, QSpinBox, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage, QPixmap
from layout import do_main_layout
from image_loader import PPMLoader, JPEGLoader
from image_processor import ImageProcessor
from image_viewer_widget import ImageViewerWidget

import traceback
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        do_main_layout(self)
        

        self.ppm_loader = None
        self.jpeg_loader = JPEGLoader()
        self.image_processor = ImageProcessor()

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.ppm *.jpg *.jpeg)"
        )
        
        if not file_path:
            return
            
        try:
            if file_path.lower().endswith('.ppm'):
                self.ppm_loader=PPMLoader(file_path)
                image_data=self.ppm_loader.get_image_data()
            else:
                image_data = self.jpeg_loader.load(file_path)
                
            self.image_viewer.set_image(image_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            traceback.print_exc()
            
    def save_image(self):
        if not self.image_viewer.has_image():
            QMessageBox.warning(self, "Warning", "No image to save!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "JPEG (*.jpg *.jpeg)"
        )
        
        if not file_path:
            return
            
        try:
            quality = self.quality_spinner.value()
            self.jpeg_loader.save(
                self.image_viewer.get_image(),
                file_path,
                quality
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
