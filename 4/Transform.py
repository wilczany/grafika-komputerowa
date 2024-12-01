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
        # rgb = self.get_rgb_values()

        # for i in range(self.image.width()):
        #     for j in range(self.image.height()):
        #         color = self.image.pixelColor(i, j)
        #         red = min(color.red() + rgb[0], 255)
        #         green = min(color.green() + rgb[1], 255)
        #         blue = min(color.blue() + rgb[2], 255)
        #         self.image.setPixelColor(i, j, QColor(red, green, blue))

       
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
        pass
    
        
    def get_byte_array(self):
        width = self.image.width()
        height = self.image.height()
        
        # Using QImage.bits() returns byte array
        ptr = self.image.bits()
        arr = np.array(ptr).reshape(height, width, 4)
        
        return arr
    