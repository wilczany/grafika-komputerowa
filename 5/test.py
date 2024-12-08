import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QSlider, QFileDialog, QWidget)
from PySide6.QtGui import QImage, QPixmap, QImageReader
from PySide6.QtCore import Qt

class BinaryImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binaryzacja obrazów")
        self.setGeometry(100, 100, 800, 600)
        
        # Główny widget i layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Layout dla obrazów
        image_layout = QHBoxLayout()
        
        # Oryginalny obraz
        self.original_label = QLabel("Oryginalny obraz")
        self.original_label.setFixedSize(350, 350)
        self.original_label.setAlignment(Qt.AlignCenter)
        
        # Obraz zbinaryzowany
        self.binary_label = QLabel("Obraz zbinaryzowany")
        self.binary_label.setFixedSize(350, 350)
        self.binary_label.setAlignment(Qt.AlignCenter)
        
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.binary_label)
        
        # Slider do wyboru progu
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(127)
        self.threshold_slider.valueChanged.connect(self.update_binary_image)
        
        # Przycisk wczytania obrazu
        load_button = QPushButton("Wczytaj obraz")
        load_button.clicked.connect(self.load_image)
        
        # Dodanie elementów do głównego layoutu
        main_layout.addLayout(image_layout)
        main_layout.addWidget(self.threshold_slider)
        main_layout.addWidget(load_button)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self.original_image = None
        
    def load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", 
                                                  "Obrazy (*.png *.jpg *.bmp)")
        if filename:
            reader = QImageReader(filename)
            reader.setAutoTransform(True)
            qimage = reader.read()
            
            # Konwersja QImage na numpy array w skali szarości
            self.original_image = self.qimage_to_numpy(qimage)
            
            # Wyświetlenie oryginalnego obrazu
            pixmap = QPixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.original_label.setPixmap(scaled_pixmap)
            
            # Aktualizacja binaryzacji
            self.update_binary_image()
    
    def qimage_to_numpy(self, qimage):
        # Konwersja QImage do numpy array w skali szarości
        qimage = qimage.convertToFormat(QImage.Format_Grayscale8)
        width = qimage.width()
        height = qimage.height()
        
        # Bezpieczna konwersja do numpy
        buffer = qimage.constBits().tobytes()
        arr = np.frombuffer(buffer, np.uint8).reshape((height, width))
        return arr
    
    def custom_binarization(self, image, threshold):
        # Własna implementacja binaryzacji
        binary_image = np.zeros_like(image)
        binary_image[image > threshold] = 255
        return binary_image
    
    def percent_black_selection(self, image, percent):
        # Obliczenie progu binaryzacji na podstawie procentu czarnego
        threshold = np.percentile(image, percent)
        return threshold
            
    
    def update_binary_image(self):
        if self.original_image is not None:
            threshold = self.threshold_slider.value()
            # binary_image = self.custom_binarization(self.original_image, threshold)
            binary_image = self.percent_black_selection(self.original_image, threshold)
            # Konwersja wyniku binaryzacji do QImage
            binary_qimage = QImage(binary_image.tobytes(), 
                                   binary_image.shape[1], 
                                   binary_image.shape[0], 
                                   QImage.Format_Grayscale8)
            
            pixmap = QPixmap.fromImage(binary_qimage)
            scaled_pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.binary_label.setPixmap(scaled_pixmap)

def main():
    app = QApplication(sys.argv)
    processor = BinaryImageProcessor()
    processor.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()