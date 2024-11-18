import sys
from PySide6.QtWidgets import QApplication
from window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

# main.py
# from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
# from PySide6.QtWidgets import QPushButton, QFileDialog, QSpinBox, QScrollArea, QMessageBox, QSizePolicy
# from PySide6.QtCore import Qt, QPoint
# from PySide6.QtGui import QImage, QPixmap, QPalette
# import sys
# import numpy as np
# from PIL import Image

# class ImageViewer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Image Viewer")
#         self.setGeometry(100, 100, 800, 600)

#         # Create central widget and layout
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.layout = QVBoxLayout(self.central_widget)

#         # Create toolbar
#         self.create_toolbar()

#         # Create image display area
#         self.scroll_area = QScrollArea()
#         self.image_label = QLabel()
#         self.image_label.setBackgroundRole(QPalette.Base)
#         self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
#         self.image_label.setScaledContents(True)
#         self.scroll_area.setWidget(self.image_label)
#         self.scroll_area.setVisible(False)
#         self.layout.addWidget(self.scroll_area)

#         # Initialize variables
#         self.image = None
#         self.zoom_factor = 1.0
#         self.current_file = None

#     def create_toolbar(self):
#         toolbar_widget = QWidget()
#         toolbar_layout = QHBoxLayout(toolbar_widget)

#         # Create buttons
#         self.open_button = QPushButton("Open")
#         self.save_button = QPushButton("Save JPEG")
#         self.zoom_in_button = QPushButton("Zoom In")
#         self.zoom_out_button = QPushButton("Zoom Out")

#         # Create quality spinner
#         self.quality_label = QLabel("JPEG Quality:")
#         self.quality_spinner = QSpinBox()
#         self.quality_spinner.setRange(1, 100)
#         self.quality_spinner.setValue(85)

#         # Add widgets to toolbar
#         toolbar_layout.addWidget(self.open_button)
#         toolbar_layout.addWidget(self.save_button)
#         toolbar_layout.addWidget(self.zoom_in_button)
#         toolbar_layout.addWidget(self.zoom_out_button)
#         toolbar_layout.addWidget(self.quality_label)
#         toolbar_layout.addWidget(self.quality_spinner)
#         toolbar_layout.addStretch()

#         # Connect signals
#         self.open_button.clicked.connect(self.open_file)
#         self.save_button.clicked.connect(self.save_file)
#         self.zoom_in_button.clicked.connect(self.zoom_in)
#         self.zoom_out_button.clicked.connect(self.zoom_out)

#         self.layout.addWidget(toolbar_widget)

#     def load_ppm_p3(self, filepath):
#         with open(filepath, 'r') as f:
#             # Read header
#             magic = f.readline().strip()
#             if magic != 'P3':
#                 raise ValueError('Not a PPM P3 file')

#             # Skip comments
#             line = f.readline()
#             while line.startswith('#'):
#                 line = f.readline()

#             # Read dimensions and max value
#             width, height = map(int, line.split())
#             max_val = int(f.readline())

#             # Read pixel data
#             pixels = []
#             for line in f:
#                 pixels.extend(map(int, line.split()))

#             # Convert to numpy array
#             image_data = np.array(pixels).reshape(height, width, 3)
#             if max_val != 255:
#                 image_data = (image_data * 255 // max_val).astype(np.uint8)
            
#             return image_data

#     def load_ppm_p6(self, filepath):
#         with open(filepath, 'rb') as f:
#             # Read header
#             magic = f.readline().decode().strip()
#             if magic != 'P6':
#                 raise ValueError('Not a PPM P6 file')

#             # Skip comments
#             line = f.readline()
#             while line.startswith(b'#'):
#                 line = f.readline()

#             # Read dimensions and max value
#             width, height = map(int, line.decode().split())
#             max_val = int(f.readline().strip())

#             # Read binary pixel data
#             raw_data = f.read()
#             image_data = np.frombuffer(raw_data, dtype=np.uint8).reshape(height, width, 3)
            
#             if max_val != 255:
#                 image_data = (image_data * 255 // max_val).astype(np.uint8)
            
#             return image_data

#     def open_file(self):
#         filepath, _ = QFileDialog.getOpenFileName(
#             self,
#             "Open Image",
#             "",
#             "Images (*.ppm *.jpg *.jpeg)"
#         )

#         if not filepath:
#             return

#         try:
#             if filepath.lower().endswith('.ppm'):
#                 # Check PPM type
#                 with open(filepath, 'rb') as f:
#                     magic = f.readline().decode().strip()
#                     if magic == 'P3':
#                         image_data = self.load_ppm_p3(filepath)
#                     elif magic == 'P6':
#                         image_data = self.load_ppm_p6(filepath)
#                     else:
#                         raise ValueError(f'Unsupported PPM format: {magic}')
#             else:
#                 # Load JPEG
#                 image = Image.open(filepath)
#                 image_data = np.array(image)

#             self.display_image(image_data)
#             self.current_file = filepath
#             self.scroll_area.setVisible(True)
            
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Could not load image: {str(e)}")

#     def display_image(self, image_data):
#         height, width = image_data.shape[:2]
#         bytes_per_line = 3 * width

#         # Convert numpy array to QImage
#         q_image = QImage(
#             image_data.data,
#             width,
#             height,
#             bytes_per_line,
#             QImage.Format_RGB888
#         )

#         # Convert QImage to QPixmap and display it
#         pixmap = QPixmap.fromImage(q_image)
#         self.image_label.setPixmap(pixmap)
#         self.image_label.resize(self.zoom_factor * pixmap.size())

#     def save_file(self):
#         if self.image_label.pixmap() is None:
#             QMessageBox.warning(self, "Warning", "No image to save!")
#             return

#         filepath, _ = QFileDialog.getSaveFileName(
#             self,
#             "Save Image",
#             "",
#             "JPEG (*.jpg *.jpeg)"
#         )

#         if filepath:
#             try:
#                 # Get the current pixmap and convert to QImage
#                 pixmap = self.image_label.pixmap()
#                 image = pixmap.toImage()
                
#                 # Convert QImage to PIL Image
#                 width = image.width()
#                 height = image.height()
#                 ptr = image.bits()
#                 ptr.setsize(height * width * 3)
#                 arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 3))
                
#                 # Save using PIL
#                 im = Image.fromarray(arr)
#                 im.save(filepath, quality=self.quality_spinner.value())
                
#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Could not save image: {str(e)}")

#     def zoom_in(self):
#         self.scale_image(1.25)

#     def zoom_out(self):
#         self.scale_image(0.8)

#     def scale_image(self, factor):
#         if self.image_label.pixmap() is None:
#             return

#         self.zoom_factor *= factor
#         self.update_image()

#     def update_image(self):
#         if self.image_label.pixmap() is None:
#             return

#         pixmap = self.image_label.pixmap()
#         scaled_pixmap = pixmap.scaled(
#             self.zoom_factor * pixmap.width(),
#             self.zoom_factor * pixmap.height(),
#             Qt.KeepAspectRatio,
#             Qt.SmoothTransformation
#         )
#         self.image_label.setPixmap(scaled_pixmap)
#         self.image_label.resize(scaled_pixmap.size())

# def main():
#     app = QApplication(sys.argv)
#     viewer = ImageViewer()
#     viewer.show()
#     sys.exit(app.exec())

# if __name__ == '__main__':
#     main()



    # XDDDDDDDDDDDD


