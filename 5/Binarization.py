from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixelFormat
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
            self.current_image_array = None
            self.display_image(self.current_image)

    def display_image(self, image):
        if image:
            self.image_viewer.display_image(image)

    def qimage_to_numpy(self, qimage):
        width = qimage.width()
        height = qimage.height()

        # Konwersja na skalę szarości
        gray_image = np.zeros((height, width), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                color = qimage.pixelColor(x, y)
                gray_value = int(
                    0.299 * color.red() + 0.587 * color.green() + 0.114 * color.blue()
                )
                gray_image[y, x] = gray_value
        self.current_image_array = gray_image
        return gray_image

    def numpy_to_qimage(self, arr):
        """Konwersja numpy array na QImage"""
        height, width = arr.shape
        bytes_per_line = width

        qimage = QImage(
            arr.data, width, height, bytes_per_line, QImage.Format_Grayscale8
        )
        return qimage

    def manual_threshold(self, threshold):
        if self.current_image is None:
            return
        img_array = self.qimage_to_numpy(self.current_image)
        binary = (img_array >= threshold) * 255
        self.current_image = self.numpy_to_qimage(binary.astype(np.uint8))
        self.display_image(self.current_image)

    def percent_black_selection(self, percent):
        if self.current_image is None:
            return
        img_array = self.qimage_to_numpy(self.current_image)

        threshold = np.percentile(img_array, percent)

        binarized_image = (img_array > threshold).astype(np.uint8) * 255

        # Wyświetlenie obrazu
        self.current_image = self.numpy_to_qimage(binarized_image)

        self.display_image(self.current_image)

    def mean_iterative_selection(self):
        if self.current_image is None:
            return

        img_array = self.qimage_to_numpy(self.current_image)
        # "suitable threshold level"
        threshold = 127
        old_threshold = 0
        i = 0

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

    def entropy_selection(self):
        if self.current_image is None:
            return

        img_array = self.qimage_to_numpy(self.current_image)
        histogram = np.histogram(img_array, bins=256, range=(0, 256))[0]
        total_pixels = np.sum(histogram)

        max_entropy = float("-inf")
        optimal_threshold = 0

        for threshold in range(1, 255):
            # podział histogramu na dwie klasy
            left = histogram[:threshold]
            right = histogram[threshold:]

            # obliczanie prawdopodobieństw
            p1 = np.sum(left) / total_pixels
            p2 = np.sum(right) / total_pixels

            if p1 == 0 or p2 == 0:
                continue

            dist1 = left / np.sum(left) if np.sum(left) > 0 else np.zeros_like(left)
            dist2 = right / np.sum(right) if np.sum(right) > 0 else np.zeros_like(right)

            # obliczanie entropii dla kazdej klasy
            entropy1 = -np.sum(dist1[dist1 > 0] * np.log2(dist1[dist1 > 0]))
            entropy2 = -np.sum(dist2[dist2 > 0] * np.log2(dist2[dist2 > 0]))

            # Total entropy
            total_entropy = entropy1 + entropy2

            if total_entropy > max_entropy:
                max_entropy = total_entropy
                optimal_threshold = threshold

        # Apply threshold
        binary = (img_array >= optimal_threshold) * 255
        self.current_image = self.numpy_to_qimage(binary.astype(np.uint8))
        self.display_image(self.current_image)

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
