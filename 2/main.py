from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFileDialog)
from PySide6.QtGui import QPixmap, QImage, QColor
from PySide6.QtCore import Qt
import sys
import struct

class PPMViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Przeglądarka PPM")
        self.setGeometry(100, 100, 800, 600)

        # Główny widget i layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Przyciski
        self.btn_load_p3 = QPushButton("Wczytaj PPM P3")
        self.btn_load_p6 = QPushButton("Wczytaj PPM P6")
        self.btn_load_p3.clicked.connect(lambda: self.load_ppm("P3"))
        self.btn_load_p6.clicked.connect(lambda: self.load_ppm("P6"))

        # Label na obraz
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        # Dodanie widgetów do layoutu
        layout.addWidget(self.btn_load_p3)
        layout.addWidget(self.btn_load_p6)
        layout.addWidget(self.image_label)

    def load_ppm(self, format_type):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik PPM",
            "",
            "PPM Files (*.ppm);;All Files (*)"
        )
        
        if file_name:
            if format_type == "P3":
                self.load_p3(file_name)
            else:
                self.load_p6(file_name)

    def load_p3(self, file_name):
        try:
            with open(file_name, 'r') as f:
                # Pomijanie komentarzy
                magic_number = f.readline().strip()
                if magic_number != "P3":
                    raise ValueError("Nieprawidłowy format pliku P3")

                while True:
                    line = f.readline().strip()
                    if line and not line.startswith('#'):
                        width, height = map(int, line.split())
                        break

                max_val = int(f.readline().strip())
                
                # Wczytywanie pikseli
                pixels = []
                while True:
                    line = f.readline().strip()
                    if not line:
                        continue
                    if line.startswith('#'):
                        continue
                    pixels.extend(map(int, line.split()))
                    if len(pixels) >= width * height * 3:
                        break

                # Tworzenie obrazu
                image = QImage(width, height, QImage.Format_RGB888)
                idx = 0
                for y in range(height):
                    for x in range(width):
                        r = int(pixels[idx] * 255 / max_val)
                        g = int(pixels[idx + 1] * 255 / max_val)
                        b = int(pixels[idx + 2] * 255 / max_val)
                        image.setPixelColor(x, y, QColor(r, g, b))
                        idx += 3

                # Wyświetlanie obrazu
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))

        except Exception as e:
            print(f"Błąd podczas wczytywania pliku P3: {str(e)}")

    def load_p6(self, file_name):
        try:
            with open(file_name, 'rb') as f:
                # Wczytywanie nagłówka
                header = b''
                while True:
                    byte = f.read(1)
                    header += byte
                    if byte == b'\n':
                        magic_number = header.decode().strip()
                        if magic_number != "P6":
                            raise ValueError("Nieprawidłowy format pliku P6")
                        break

                # Pomijanie komentarzy i wczytywanie wymiarów
                dimensions = b''
                while True:
                    byte = f.read(1)
                    if byte == b'#':
                        while f.read(1) != b'\n':
                            pass
                        continue
                    dimensions += byte
                    if byte == b'\n':
                        width, height = map(int, dimensions.decode().strip().split())
                        break

                # Wczytywanie maksymalnej wartości
                max_val_str = b''
                while True:
                    byte = f.read(1)
                    max_val_str += byte
                    if byte == b'\n':
                        max_val = int(max_val_str.decode().strip())
                        break

                # Wczytywanie danych pikseli
                raw_data = f.read()
                image = QImage(width, height, QImage.Format_RGB888)
                idx = 0
                for y in range(height):
                    for x in range(width):
                        r = raw_data[idx]
                        g = raw_data[idx + 1]
                        b = raw_data[idx + 2]
                        image.setPixelColor(x, y, QColor(r, g, b))
                        idx += 3

                # Wyświetlanie obrazu
                pixmap = QPixmap.fromImage(image)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))

        except Exception as e:
            print(f"Błąd podczas wczytywania pliku P6: {str(e)}")

def main():
    app = QApplication(sys.argv)
    viewer = PPMViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()