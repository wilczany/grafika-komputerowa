from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import QWidget, QFileDialog
from ImageView import ImageViewer
import Layout


class Histogram(QWidget):
    def __init__(self):
        super().__init__()
        Layout.do_histogram_layout(self)
        self.original_image = None
        self.current_image = None

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

    def calculate_histogram(self, image):
        histograms = {"r": [0] * 256, "g": [0] * 256, "b": [0] * 256}
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))
                histograms["r"][color.red()] += 1
                histograms["g"][color.green()] += 1
                histograms["b"][color.blue()] += 1
        return histograms

    def normalize_histogram(self):
        if not self.current_image:
            return

        result = QImage(self.current_image)
        min_r = min_g = min_b = 255
        max_r = max_g = max_b = 0

        for y in range(self.current_image.height()):
            for x in range(self.current_image.width()):
                color = QColor(self.current_image.pixel(x, y))
                r, g, b = color.red(), color.green(), color.blue()

                min_r = min(min_r, r)
                min_g = min(min_g, g)
                min_b = min(min_b, b)

                max_r = max(max_r, r)
                max_g = max(max_g, g)
                max_b = max(max_b, b)

        for y in range(result.height()):
            for x in range(result.width()):
                color = QColor(self.current_image.pixel(x, y))

                r = (
                    int((color.red() - min_r) * 255 / (max_r - min_r))
                    if max_r > min_r
                    else color.red()
                )
                g = (
                    int((color.green() - min_g) * 255 / (max_g - min_g))
                    if max_g > min_g
                    else color.green()
                )
                b = (
                    int((color.blue() - min_b) * 255 / (max_b - min_b))
                    if max_b > min_b
                    else color.blue()
                )

                result.setPixel(x, y, QColor(r, g, b).rgb())

        self.current_image = result
        self.display_image(self.current_image)

    # metoda CDF
    # https://en.wikipedia.org/wiki/Histogram_equalization#Implementation

    # def equalize_histogram(self):
    #     if not self.current_image:
    #         return

    #     histograms = self.calculate_histogram(self.current_image)
    #     total_pixels = self.current_image.width() * self.current_image.height()

    #
    #     cdf = {"r": [0] * 256, "g": [0] * 256, "b": [0] * 256}
    #     for channel in ["r", "g", "b"]:
    #         sum = 0
    #         for i in range(256):
    #             sum += histograms[channel][i]
    #             cdf[channel][i] = sum

    #
    #     result = QImage(self.current_image)
    #     for y in range(result.height()):
    #         for x in range(result.width()):
    #             color = QColor(self.current_image.pixel(x, y))
    #             r = int(cdf["r"][color.red()] * 255 / total_pixels)
    #             g = int(cdf["g"][color.green()] * 255 / total_pixels)
    #             b = int(cdf["b"][color.blue()] * 255 / total_pixels)
    #             result.setPixel(x, y, QColor(r, g, b).rgb())

    #     self.current_image = result
    #     self.display_image(self.current_image)

    def equalize_histogram(self):

        if not self.current_image:
            return

        histogram = self.calculate_histogram(self.current_image)
        total_pixels = self.current_image.width() * self.current_image.height()

        # LUT table
        lut = {"r": [0] * 256, "g": [0] * 256, "b": [0] * 256}
        min_r = 0
        min_g = 0
        min_b = 0
        for i in range(256):
            if histogram["r"][i] != 0:
                min_r = histogram["r"][i]
                break

        for i in range(256):
            if histogram["g"][i] != 0:
                min_g = histogram["g"][i]
                break

        for i in range(256):
            if histogram["b"][i] != 0:
                min_b = histogram["b"][i]
                break

        sum_r = 0
        sum_g = 0
        sum_b = 0
        for i in range(256):
            sum_r += histogram["r"][i]
            sum_g += histogram["g"][i]
            sum_b += histogram["b"][i]
            lut["r"][i] = int((sum_r - min_r) * 255 / (total_pixels - min_r))
            lut["g"][i] = int((sum_g - min_g) * 255 / (total_pixels - min_g))
            lut["b"][i] = int((sum_b - min_b) * 255 / (total_pixels - min_b))

        for y in range(self.current_image.height()):
            for x in range(self.current_image.width()):
                color = QColor(self.current_image.pixel(x, y))
                r = lut["r"][color.red()]
                g = lut["g"][color.green()]
                b = lut["b"][color.blue()]
                self.current_image.setPixel(x, y, QColor(r, g, b).rgb())

        self.display_image(self.current_image)

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
