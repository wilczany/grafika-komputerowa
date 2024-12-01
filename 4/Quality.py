from PySide6.QtWidgets import QWidget, QFileDialog,QMessageBox
from PySide6.QtGui import QColor, QImage, QPixmap, Qt
from PIL import Image
import numpy as np

import Layout

class QualityEnchance(QWidget):
    def __init__(self):
        super().__init__()
        Layout.do_quality_layout(self)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                 "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            # Load as RGB
            self.original_image = np.array(Image.open(file_name))
            self.display_image(self.original_image, self.original_label)

    def display_image(self, image, label):
        if image is None:
            return
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        # Convert to RGB format
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(q_img).scaled(300, 300, Qt.KeepAspectRatio))

    def apply_filter(self, filter_type):
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first!")
            return
            
        if filter_type == 'mean':
            self.processed_image = self.apply_to_channels(self.mean_filter)
        elif filter_type == 'median':
            self.processed_image = self.apply_to_channels(self.median_filter)
        elif filter_type == 'sobel':
            self.processed_image = self.apply_to_channels(self.sobel_filter)
        elif filter_type == 'sharpen':
            self.processed_image = self.apply_to_channels(self.sharpen_filter)
        elif filter_type == 'gaussian':
            self.processed_image = self.apply_to_channels(self.gaussian_filter)
        
        self.display_image(self.processed_image, self.filtered_label)

    def apply_to_channels(self, filter_func):
        # Apply filter to each RGB channel separately
        result = np.zeros_like(self.original_image)
        for i in range(3):  # RGB channels
            result[:,:,i] = filter_func(self.original_image[:,:,i])
        return np.clip(result, 0, 255).astype(np.uint8)

    # Filter methods remain the same but will be applied to each channel separately
    def mean_filter(self, image, kernel_size=3):
        height, width = image.shape
        padded = np.pad(image, kernel_size//2)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                window = padded[i:i+kernel_size, j:j+kernel_size]
                result[i,j] = np.mean(window)
        return result

    def median_filter(self, image, kernel_size=3):
        height, width = image.shape
        padded = np.pad(image, kernel_size//2)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                window = padded[i:i+kernel_size, j:j+kernel_size]
                result[i,j] = np.median(window)
        return result

    def sobel_filter(self, image):
        kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        height, width = image.shape
        padded = np.pad(image, 1)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                window = padded[i:i+3, j:j+3]
                gx = np.sum(window * kernel_x)
                gy = np.sum(window * kernel_y)
                result[i,j] = np.sqrt(gx**2 + gy**2)
        return result

    def sharpen_filter(self, image):
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        height, width = image.shape
        padded = np.pad(image, 1)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                window = padded[i:i+3, j:j+3]
                result[i,j] = np.sum(window * kernel)
        return np.clip(result, 0, 255)

    def gaussian_filter(self, image, kernel_size=3, sigma=1.0):
        k = kernel_size // 2
        x, y = np.meshgrid(np.linspace(-k, k, kernel_size), np.linspace(-k, k, kernel_size))
        kernel = np.exp(-(x**2 + y**2)/(2*sigma**2))
        kernel = kernel / kernel.sum()
        
        height, width = image.shape
        padded = np.pad(image, k)
        result = np.zeros_like(image)
        
        for i in range(height):
            for j in range(width):
                window = padded[i:i+kernel_size, j:j+kernel_size]
                result[i,j] = np.sum(window * kernel)
        return result