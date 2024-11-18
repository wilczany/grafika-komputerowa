from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QImageWriter

from layout import do_main_layout
from image_loader import PPMLoader, JPEGLoader

import traceback


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        do_main_layout(self)

        self.ppm_loader = None
        self.jpeg_loader = JPEGLoader()

        self.image_data: QImage = None

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.ppm *.jpg *.jpeg)"
        )

        if not file_path:
            return

        try:
            if file_path.lower().endswith(".ppm"):
                self.ppm_loader = PPMLoader(file_path)
                self.image_data = self.ppm_loader.get_image_data()
            else:
                self.image_data = self.jpeg_loader.load(file_path)

            self.image_viewer.set_image(self.image_data)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            traceback.print_exc()

    def save_image(self):
        if not self.image_viewer.has_image():
            QMessageBox.warning(self, "Warning", "No image to save!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "JPEG (*.jpg *.jpeg)"
        )
        if not file_path.lower().endswith(".jpg") and not file_path.lower().endswith(
            ".jpeg"
        ):
            file_path += ".jpg"
        if not file_path:
            return

        try:
            quality = self.quality_spinner.value()
            self.image_data.save(file_path, "JPG", quality)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
