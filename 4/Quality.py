from PySide6.QtWidgets import QWidget, QFileDialog,QMessageBox
from PySide6.QtGui import QColor, QImage, QPixmap, Qt
from PIL import Image, ImageQt
import numpy as np

import Layout

class QualityEnhance(QWidget):
    def __init__(self):
        super().__init__()
        Layout.do_quality_layout(self)
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", 
                                                 "Image Files (*.png *.jpg *.bmp)")
        if file_name:
            self.original_image = np.array(Image.open(file_name))
            self.display_image(self.original_image, self.original_view)

    def display_image(self, image, imageview):
        if image is None:
            return
        height, width, _ = image.shape
        bytes_per_line = 3 * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        imageview.display_image(q_img)

    def apply_filter(self, filter_type):
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "Please load an image first!")
            return
        
        # Dictionary mapping filter types to their respective methods
        
        filters = {
            'mean': (self.channel_convolution, np.ones((3, 3)) / 9),
            'median': (self.channel_median, None),
            'sobel': (self.edge_detection, (
                np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
                np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
            )),
            'sharpen': (self.channel_convolution, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])),
            'gaussian': (self.channel_convolution, np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16)
        }
        
        filter_func, kernel = filters.get(filter_type, (None, None))
        
        if filter_func:

            self.processed_image = filter_func(self.original_image, kernel)
            self.display_image(self.processed_image, self.filtered_view)

    def channel_convolution(self, image, kernel):
    
        height, width, channels = image.shape
        pad = kernel.shape[0] // 2
        padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        
        filtered = np.zeros_like(image)
        
        for y in range(height):
            for x in range(width):
                for c in range(channels):
                    neighborhood = padded[y:y+kernel.shape[0], x:x+kernel.shape[1], c]
                    filtered[y, x, c] = np.clip(np.sum(neighborhood * kernel), 0, 255)
        
        return filtered

    def channel_median(self, image, _=None):
  
        height, width, channels = image.shape
        kernel_size = 3
        pad = kernel_size // 2
        padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        
        filtered = np.zeros_like(image)
        
        for y in range(height):
            for x in range(width):
                for c in range(channels):
                    neighborhood = padded[y:y+kernel_size, x:x+kernel_size, c]
                    filtered[y, x, c] = np.median(neighborhood)
        
        return filtered

    def edge_detection(self, image, kernels):

        sobel_x, sobel_y = kernels
        height, width, channels = image.shape
        
        padded = np.pad(image, ((1, 1), (1, 1), (0, 0)), mode='edge')
        filtered = np.zeros_like(image)
        
        for y in range(height):
            for x in range(width):
                for c in range(channels):
                    neighborhood = padded[y:y+3, x:x+3, c]
                    
                    gx = np.sum(neighborhood * sobel_x)
                    gy = np.sum(neighborhood * sobel_y)
                    
                    filtered[y, x, c] = np.sqrt(gx**2 + gy**2)
        
        filtered = (filtered / filtered.max() * 255).astype(np.uint8)
        return filtered