import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QSpinBox, QComboBox)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import cv2

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przekształcenia punktowe obrazu")
        self.setMinimumSize(800, 600)
        
        # Zmienne przechowujące obrazy
        self.original_image = None
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Główny widget i layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Panel kontrolny (lewy)
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # Przycisk wczytywania obrazu
        load_button = QPushButton("Wczytaj obraz")
        load_button.clicked.connect(self.load_image)
        control_layout.addWidget(load_button)
        
        # Wartość do operacji
        self.value_spinbox = QSpinBox()
        self.value_spinbox.setRange(-255, 255)
        self.value_spinbox.setValue(0)
        control_layout.addWidget(QLabel("Wartość:"))
        control_layout.addWidget(self.value_spinbox)
        
        # Przyciski operacji
        operations = [
            ("Dodawanie", self.add_value),
            ("Odejmowanie", self.subtract_value),
            ("Mnożenie", self.multiply_value),
            ("Dzielenie", self.divide_value),
            ("Zmiana jasności", self.change_brightness)
        ]
        
        for name, func in operations:
            btn = QPushButton(name)
            btn.clicked.connect(func)
            control_layout.addWidget(btn)
            
        # Kombobox dla skali szarości
        self.grayscale_combo = QComboBox()
        self.grayscale_combo.addItems(["Średnia arytmetyczna", "Ważona"])
        control_layout.addWidget(QLabel("Metoda skali szarości:"))
        control_layout.addWidget(self.grayscale_combo)
        
        grayscale_btn = QPushButton("Konwertuj do skali szarości")
        grayscale_btn.clicked.connect(self.convert_to_grayscale)
        control_layout.addWidget(grayscale_btn)
        
        # Przycisk resetowania
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_image)
        control_layout.addWidget(reset_button)
        
        control_layout.addStretch()
        
        # Panel obrazu (prawy)
        image_panel = QWidget()
        image_layout = QVBoxLayout(image_panel)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_layout.addWidget(self.image_label)
        
        # Dodanie paneli do głównego layoutu
        main_layout.addWidget(control_panel, 1)
        main_layout.addWidget(image_panel, 4)
        
    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz",
                                                 "", "Obrazy (*.png *.jpg *.bmp)")
        if file_name:
            self.original_image = cv2.imread(file_name)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.reset_image()
            
    def display_image(self, image):
        if image is not None:
            h, w, ch = image.shape
            bytes_per_line = ch * w
            qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            
            # Skalowanie z zachowaniem proporcji
            scaled_pixmap = pixmap.scaled(self.image_label.size(), 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            
    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            
    def add_value(self):
        if self.current_image is not None:
            value = self.value_spinbox.value()
            result = cv2.add(self.current_image, np.full_like(self.current_image, value))
            self.current_image = result
            self.display_image(self.current_image)
            
    def subtract_value(self):
        if self.current_image is not None:
            value = self.value_spinbox.value()
            result = cv2.subtract(self.current_image, np.full_like(self.current_image, value))
            self.current_image = result
            self.display_image(self.current_image)
            
    def multiply_value(self):
        if self.current_image is not None:
            value = self.value_spinbox.value()
            result = cv2.multiply(self.current_image.astype(float), value)
            result = np.clip(result, 0, 255).astype(np.uint8)
            self.current_image = result
            self.display_image(self.current_image)
            
    def divide_value(self):
        if self.current_image is not None:
            value = self.value_spinbox.value()
            if value != 0:
                result = cv2.divide(self.current_image.astype(float), value)
                result = np.clip(result, 0, 255).astype(np.uint8)
                self.current_image = result
                self.display_image(self.current_image)
                
    def change_brightness(self):
        if self.current_image is not None:
            value = self.value_spinbox.value()
            hsv = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.add(v, value)
            final_hsv = cv2.merge((h, s, v))
            result = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
            self.current_image = result
            self.display_image(self.current_image)
            
    def convert_to_grayscale(self):
        if self.current_image is not None:
            if self.grayscale_combo.currentText() == "Średnia arytmetyczna":
                # Metoda 1: średnia arytmetyczna
                result = np.mean(self.current_image, axis=2).astype(np.uint8)
            else:
                # Metoda 2: ważona (standardowa konwersja OpenCV)
                result = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
            
            # Konwersja z powrotem do 3 kanałów dla wyświetlenia
            self.current_image = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
            self.display_image(self.current_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec())