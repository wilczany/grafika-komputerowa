# from PySide6.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QVBoxLayout,
#     QPushButton,
#     QLabel,
#     QFileDialog,
# )

# from PySide6.QtGui import QPixmap, QImage, QColor

# from PySide6.QtCore import Qt

# from layout import do_main_layout

# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         do_main_layout(self)

#     def load_ppm(self, format_type):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self, "Wybierz plik PPM", "", "PPM Files (*.ppm);;All Files (*)"
#         )

#         if file_name:
#             if format_type == "P3":
#                 self.load_p3(file_name)
#             else:
#                 self.load_p6(file_name)

#     def load_p3(self, file_name):
#         try:
#             with open(file_name, "r") as f:
#                 # Pomijanie komentarzy
#                 magic_number = f.readline().strip()
#                 if magic_number != "P3":
#                     raise ValueError("Nieprawidłowy format pliku P3")

#                 while True:
#                     line = f.readline().strip()
#                     if line and not line.startswith("#"):
#                         width, height = map(int, line.split())
#                         break

#                 max_val = int(f.readline().strip())

#                 # Wczytywanie pikseli
#                 pixels = []
#                 while True:
#                     line = f.readline().strip()
#                     if not line:
#                         continue
#                     if line.startswith("#"):
#                         continue
#                     pixels.extend(map(int, line.split()))
#                     if len(pixels) >= width * height * 3:
#                         break

#                 # Tworzenie obrazu
#                 image = QImage(width, height, QImage.Format_RGB888)
#                 idx = 0
#                 for y in range(height):
#                     for x in range(width):
#                         r = int(pixels[idx] * 255 / max_val)
#                         g = int(pixels[idx + 1] * 255 / max_val)
#                         b = int(pixels[idx + 2] * 255 / max_val)
#                         image.setPixelColor(x, y, QColor(r, g, b))
#                         idx += 3

#                 # Wyświetlanie obrazu
#                 pixmap = QPixmap.fromImage(image)
#                 self.image_label.setPixmap(
#                     pixmap.scaled(
#                         self.image_label.size(),
#                         Qt.KeepAspectRatio,
#                         Qt.SmoothTransformation,
#                     )
#                 )

#         except Exception as e:
#             print(f"Błąd podczas wczytywania pliku P3: {str(e)}")

#     def load_from PySide6.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QVBoxLayout,
#     QPushButton,
#     QLabel,
#     QFileDialog,
# )

# from PySide6.QtGui import QPixmap, QImage, QColor

# from PySide6.QtCore import Qt

# from layout import do_main_layout

# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         do_main_layout(self)

#     def load_ppm(self, format_type):
#         file_name, _ = QFileDialog.getOpenFileName(
#             self, "Wybierz plik PPM", "", "PPM Files (*.ppm);;All Files (*)"
#         )

#         if file_name:
#             if format_type == "P3":
#                 self.load_p3(file_name)
#             else:
#                 self.load_p6(file_name)

#     def load_p3(self, file_name):
#         try:
#             with open(file_name, "r") as f:
#                 # Pomijanie komentarzy
#                 magic_number = f.readline().strip()
#                 if magic_number != "P3":
#                     raise ValueError("Nieprawidłowy format pliku P3")

#                 while True:
#                     line = f.readline().strip()
#                     if line and not line.startswith("#"):
#                         width, height = map(int, line.split())
#                         break

#                 max_val = int(f.readline().strip())

#                 # Wczytywanie pikseli
#                 pixels = []
#                 while True:
#                     line = f.readline().strip()
#                     if not line:
#                         continue
#                     if line.startswith("#"):
#                         continue
#                     pixels.extend(map(int, line.split()))
#                     if len(pixels) >= width * height * 3:
#                         break

#                 # Tworzenie obrazu
#                 image = QImage(width, height, QImage.Format_RGB888)
#                 idx = 0
#                 for y in range(height):
#                     for x in range(width):
#                         r = int(pixels[idx] * 255 / max_val)
#                         g = int(pixels[idx + 1] * 255 / max_val)
#                         b = int(pixels[idx + 2] * 255 / max_val)
#                         image.setPixelColor(x, y, QColor(r, g, b))
#                         idx += 3

#                 # Wyświetlanie obrazu
#                 pixmap = QPixmap.fromImage(image)
#                 self.image_label.setPixmap(
#                     pixmap.scaled(
#                         self.image_label.size(),
#                         Qt.KeepAspectRatio,
#                         Qt.SmoothTransformation,
#                     )
#                 )

#         except Exception as e:
#             print(f"Błąd podczas wczytywania pliku P3: {str(e)}")

#     def load_p6(self, file_name):
#         try:
#             with open(file_name, "rb") as f:
#                 # Wczytywanie nagłówka
#                 header = b""
#                 while True:
#                     byte = f.read(1)
#                     header += byte
#                     if byte == b"\n":
#                         magic_number = header.decode().strip()
#                         if magic_number != "P6":
#                             raise ValueError("Nieprawidłowy format pliku P6")
#                         break

#                 # Pomijanie komentarzy i wczytywanie wymiarów
#                 dimensions = b""
#                 while True:
#                     byte = f.read(1)
#                     if byte == b"#":
#                         while f.read(1) != b"\n":
#                             pass
#                         continue
#                     dimensions += byte
#                     if byte == b"\n":
#                         width, height = map(int, dimensions.decode().strip().split())
#                         break

#                 # Wczytywanie maksymalnej wartości
#                 max_val_str = b""
#                 while True:
#                     byte = f.read(1)
#                     max_val_str += byte
#                     if byte == b"\n":
#                         max_val = int(max_val_str.decode().strip())
#                         break

#                 # Wczytywanie danych pikseli
#                 raw_data = f.read()
#                 image = QImage(width, height, QImage.Format_RGB888)
#                 idx = 0
#                 for y in range(height):
#                     for x in range(width):
#                         r = raw_data[idx]
#                         g = raw_data[idx + 1]
#                         b = raw_data[idx + 2]
#                         image.setPixelColor(x, y, QColor(r, g, b))
#                         idx += 3

#                 # Wyświetlanie obrazu
#                 pixmap = QPixmap.fromImage(image)
#                 self.image_label.setPixmap(
#                     pixmap.scaled(
#                         self.image_label.size(),
#                         Qt.KeepAspectRatio,
#                         Qt.SmoothTransformation,
#                     )
#                 )

#         except Exception as e:
#             print(f"Błąd podczas wczytywania pliku P6: {str(e)}")
            
#         try:
#             with open(file_name, "rb") as f:
            # p6(self, file_name):
#                 # Wczytywanie nagłówka
#                 header = b""
#                 while True:
#                     byte = f.read(1)
#                     header += byte
#                     if byte == b"\n":
#                         magic_number = header.decode().strip()
#                         if magic_number != "P6":
#                             raise ValueError("Nieprawidłowy format pliku P6")
#                         break

#                 # Pomijanie komentarzy i wczytywanie wymiarów
#                 dimensions = b""
#                 while True:
#                     byte = f.read(1)
#                     if byte == b"#":
#                         while f.read(1) != b"\n":
#                             pass
#                         continue
#                     dimensions += byte
#                     if byte == b"\n":
#                         width, height = map(int, dimensions.decode().strip().split())
#                         break

#                 # Wczytywanie maksymalnej wartości
#                 max_val_str = b""
#                 while True:
#                     byte = f.read(1)
#                     max_val_str += byte
#                     if byte == b"\n":
#                         max_val = int(max_val_str.decode().strip())
#                         break

#                 # Wczytywanie danych pikseli
#                 raw_data = f.read()
#                 image = QImage(width, height, QImage.Format_RGB888)
#                 idx = 0
#                 for y in range(height):
#                     for x in range(width):
#                         r = raw_data[idx]
#                         g = raw_data[idx + 1]
#                         b = raw_data[idx + 2]
#                         image.setPixelColor(x, y, QColor(r, g, b))
#                         idx += 3

#                 # Wyświetlanie obrazu
#                 pixmap = QPixmap.fromImage(image)
#                 self.image_label.setPixmap(
#                     pixmap.scaled(
#                         self.image_label.size(),
#                         Qt.KeepAspectRatio,
#                         Qt.SmoothTransformation,
#                     )
#                 )

#         except Exception as e:
#             print(f"Błąd podczas wczytywania pliku P6: {str(e)}")
            
            
##
#
#
#
#
##

# main.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtWidgets import QPushButton, QFileDialog, QSpinBox, QScrollArea, QMessageBox
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QImage, QPixmap
import sys
from image_loader import PPMLoader, JPEGLoader
from image_processor import ImageProcessor
from image_viewer_widget import ImageViewerWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setMinimumSize(800, 600)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        # Buttons
        self.load_button = QPushButton("Load Image")
        self.save_button = QPushButton("Save as JPEG")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        
        # JPEG compression quality spinner
        self.quality_label = QLabel("JPEG Quality:")
        self.quality_spinner = QSpinBox()
        self.quality_spinner.setRange(1, 100)
        self.quality_spinner.setValue(85)
        
        # Add widgets to toolbar
        toolbar.addWidget(self.load_button)
        toolbar.addWidget(self.save_button)
        toolbar.addWidget(self.zoom_in_button)
        toolbar.addWidget(self.zoom_out_button)
        toolbar.addWidget(self.quality_label)
        toolbar.addWidget(self.quality_spinner)
        toolbar.addStretch()
        
        # Image viewer
        self.image_viewer = ImageViewerWidget()
        
        # Add layouts to main layout
        layout.addLayout(toolbar)
        layout.addWidget(self.image_viewer)
        
        # Connect signals
        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_image)
        self.zoom_in_button.clicked.connect(self.image_viewer.zoom_in)
        self.zoom_out_button.clicked.connect(self.image_viewer.zoom_out)
        
        # Initialize loaders and processor
        self.ppm_loader = PPMLoader()
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
            print("No file selected")
            return
            
        try:
            print("trying to load image")
            if file_path.lower().endswith('.ppm'):
                image_data = self.ppm_loader.load(file_path)
            else:
                image_data = self.jpeg_loader.load(file_path)
                
            self.image_viewer.set_image(image_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
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

