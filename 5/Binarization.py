from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Qt
from ImageView import ImageViewer
import numpy as np
from PIL import Image
from PySide6.QtGui import QImage
import Layout

class Binarization(QWidget):
    def __init__(self):
        super().__init__()
        self.image_viewer = ImageViewer()
        self.original_image = None
        self.current_image = None
        Layout.do_binarization_layout(self)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)"
        )
        if file_name:
            self.original_image = QImage(file_name)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            
    def display_image(self, image):
        if image:
            self.image_viewer.display_image(image)

    def qimage_to_numpy(self, qimage):
        width = qimage.width()
        height = qimage.height()
        # Convert image to RGBA8888 format
        if qimage.format() != QImage.Format_RGBA8888:
            qimage = qimage.convertToFormat(QImage.Format_RGBA8888)
            
        # Create numpy array directly from memoryview
        arr = np.array(qimage.bits()).reshape(height, width, 4)
        # Convert to grayscale using luminance formula
        gray = np.dot(arr[...,:3], [0.299, 0.587, 0.114])
        
        return gray

    def numpy_to_qimage(self, arr):
        height, width = arr.shape
        bytes_per_line = width
        # Convert grayscale to RGB
        rgb = np.stack((arr,) * 3, axis=-1)
        print(height, width)
        return QImage(rgb.data, width, height, bytes_per_line * 3, QImage.Format_RGB888)

    def manual_threshold(self, threshold):
        if self.current_image:
            img_array = self.qimage_to_numpy(self.current_image)
            binary = (img_array > threshold) * 255
            self.current_image = self.numpy_to_qimage(binary.astype(np.uint8))
            self.display_image(self.current_image)

    def percent_black_selection(self, percent):
        if self.current_image:
            img_array = self.qimage_to_numpy(self.current_image)
            flat = img_array.flatten()
            sorted_pixels = np.sort(flat)
            threshold_idx = int((100 - percent) * len(sorted_pixels) / 100)
            threshold = sorted_pixels[threshold_idx]
            binary = (img_array > threshold) * 255
            self.current_image = self.numpy_to_qimage(binary.astype(np.uint8))
            self.display_image(self.current_image)

    def mean_iterative_selection(self):
        if self.current_image:
            img_array = self.qimage_to_numpy(self.current_image)
            threshold = 127
            old_threshold = 0
            
            while abs(threshold - old_threshold) > 1:
                old_threshold = threshold
                lower = img_array[img_array < threshold]
                upper = img_array[img_array >= threshold]
                
                mean_lower = np.mean(lower) if len(lower) > 0 else 0
                mean_upper = np.mean(upper) if len(upper) > 0 else 255
                
                threshold = (mean_lower + mean_upper) / 2

            binary = (img_array > threshold) * 255
            self.current_image = self.numpy_to_qimage(binary.astype(np.uint8))
            self.display_image(self.current_image)

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)

