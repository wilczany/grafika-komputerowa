from PySide6.QtWidgets import (
    QWidget,
    QInputDialog,
    QFileDialog,
    QMessageBox)
from PySide6.QtGui import QImage, QColor
import numpy as np
import Layout

class Transformations(QWidget):
    
    def __init__(self):
        super().__init__()

        Layout.do_transformation_layout(self)
        
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images ( *.jpg *.jpeg)"
        )

        if not file_path:
            return
        try:
            self.image = QImage(file_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        self.image_viewer.display_image(self.image)
        
    def transform(self):
        operations = {
            "Dodawanie": self.add_value,
            "Odejmowanie": self.subtract_value,
            "Mnożenie": self.multiply_value,
            "Dzielenie": self.divide_value,
            "Zmiana jasności": self.change_brightness
        }

        operation_name = self.button_group.checkedButton().text()
        operation = operations.get(operation_name)
        operation()


    def get_rgb_values(self):
        values = []
        for color in ["red", "green", "blue"]:
            values.append(getattr(self, f"{color}_spin").value())
        
        return values

    def add_value(self):
        print("Add value")

       
        arr = self.get_byte_array()   
        
        rgb_channels = arr[:, :, 2::-1]

        # Add the RGB adjustment values, clamping to 255
        adjusted_channels = np.minimum(rgb_channels.astype(np.int16) + self.get_rgb_values(), 255).astype(np.uint8)
        
        # Replace the original RGB channels
        arr[:, :, 2::-1] = adjusted_channels
        
        # Create a new QImage from the modified NumPy array
        # Use .copy() to ensure data is properly copied
        new_image = QImage(arr.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_ARGB32).copy()
        
        # Display the image
        self.image_viewer.display_image(new_image)

            
    def subtract_value(self):
        arr = self.get_byte_array()

        rgb_channels = arr[:, :, 2::-1]

        adjusted_channels = np.maximum(rgb_channels.astype(np.int16) - self.get_rgb_values(), 0).astype(np.uint8)

        arr[:, :, 2::-1] = adjusted_channels

        new_image = QImage(arr.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_ARGB32).copy()

        self.image_viewer.display_image(new_image)
        
    def multiply_value(self):
        arr = self.get_byte_array()

        rgb_channels = arr[:, :, 2::-1]

        adjusted_channels = np.minimum(rgb_channels.astype(np.int16) * self.get_rgb_values(), 255).astype(np.uint8)

        arr[:, :, 2::-1] = adjusted_channels

        new_image = QImage(arr.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_ARGB32).copy()

        self.image_viewer.display_image(new_image)
        
    def divide_value(self):
        
        rgb = self.get_rgb_values()

        if 0 in rgb:
            QMessageBox.critical(self, "Error", "Nie można dzielić przez 0")
            return

        arr = self.get_byte_array()

        rgb_channels = arr[:, :, 2::-1]

        adjusted_channels = np.minimum(rgb_channels.astype(np.int16) / self.get_rgb_values(), 255).astype(np.uint8)

        arr[:, :, 2::-1] = adjusted_channels

        new_image = QImage(arr.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_ARGB32).copy()

        self.image_viewer.display_image(new_image)

        
    def change_brightness(self):
        
        value = self.brightness_spin.value()

        arr = self.get_byte_array()

        rgb_channels = arr[:, :, 2::-1]

        adjusted_channels = np.clip(rgb_channels.astype(np.int16) + value, 0, 255).astype(np.uint8)

        arr[:, :, 2::-1] = adjusted_channels

        new_image = QImage(arr.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_ARGB32).copy()

        self.image_viewer.display_image(new_image)
    
    def convert_to_grayscale(self):
        method = self.grayscale_combo.currentText()    
        arr = self.get_byte_array()

        if method == "Średnia arytmetyczna":
            grayscale = np.mean(arr[:, :, 2::-1], axis=2).astype(np.uint8)
        else:
            # Convert to YUV
            # https://en.wikipedia.org/wiki/Grayscale#Luma_coding_in_video_systems
            yuv = np.dot(arr[:, :, 2::-1], [0.299, 0.587, 0.114])
            grayscale = yuv.astype(np.uint8)

        new_image = QImage(grayscale.data.tobytes(), self.image.width(), self.image.height(), QImage.Format_Grayscale8).copy()
        
        self.image_viewer.display_image(new_image)
        
    def get_byte_array(self):
        width = self.image.width()
        height = self.image.height()
        
        # Using QImage.bits() returns byte array
        ptr = self.image.bits()
        arr = np.array(ptr).reshape(height, width, 4)
        
        return arr
    