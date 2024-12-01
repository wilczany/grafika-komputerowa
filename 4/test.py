import sys
import numpy as np
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFileDialog)
from PySide6.QtGui import QImage, QPixmap, QImageReader
from PySide6.QtCore import Qt

class ImageFilterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.original_image = None
        self.filtered_image = None

    def initUI(self):
        self.setWindowTitle('Image Filter Application')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Image display area
        self.original_label = QLabel('Original Image')
        self.filtered_label = QLabel('Filtered Image')
        
        # Ensure images scale properly
        self.original_label.setAlignment(Qt.AlignCenter)
        self.filtered_label.setAlignment(Qt.AlignCenter)

        # Button layout
        button_layout = QHBoxLayout()
        
        # Filter buttons
        filter_buttons = [
            ('Load Image', self.load_image),
            ('Mean Filter', self.apply_mean_filter),
            ('Median Filter', self.apply_median_filter),
            ('Sobel Edge Detection', self.apply_sobel_filter),
            ('Sharpen Filter', self.apply_sharpen_filter),
            ('Gaussian Blur', self.apply_gaussian_blur)
        ]

        for name, method in filter_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(method)
            button_layout.addWidget(btn)

        # Add widgets to main layout
        main_layout.addWidget(self.original_label)
        main_layout.addWidget(self.filtered_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', 
                                                   r'', 
                                                   'Images (*.png *.xpm *.jpg *.bmp *.gif)')
        if file_name:
            # Read image
            reader = QImageReader(file_name)
            image = reader.read()
            
            # Convert to numpy array
            image = image.convertToFormat(QImage.Format_Grayscale8)
            width = image.width()
            height = image.height()
            
            # Create numpy array from image
            ptr = image.bits()
            # ptr.setsize(image.byteCount())
            self.original_image = np.frombuffer(ptr, np.uint8).reshape((height, width))
            
            # Display original image
            pixmap = QPixmap.fromImage(image)
            self.original_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

    def apply_mean_filter(self):
        if self.original_image is None:
            return
        
        # Mean (averaging) filter
        def mean_filter(image, kernel_size=3):
            h, w = image.shape
            pad = kernel_size // 2
            result = np.zeros_like(image)
            
            for i in range(pad, h-pad):
                for j in range(pad, w-pad):
                    neighborhood = image[i-pad:i+pad+1, j-pad:j+pad+1]
                    result[i, j] = np.mean(neighborhood)
            
            return result.astype(np.uint8)
        
        self.filtered_image = mean_filter(self.original_image)
        self._display_filtered_image(self.filtered_image)

    def apply_median_filter(self):
        if self.original_image is None:
            return
        
        # Median filter
        def median_filter(image, kernel_size=3):
            h, w = image.shape
            pad = kernel_size // 2
            result = np.zeros_like(image)
            
            for i in range(pad, h-pad):
                for j in range(pad, w-pad):
                    neighborhood = image[i-pad:i+pad+1, j-pad:j+pad+1]
                    result[i, j] = np.median(neighborhood)
            
            return result.astype(np.uint8)
        
        self.filtered_image = median_filter(self.original_image)
        self._display_filtered_image(self.filtered_image)

    def apply_sobel_filter(self):
        if self.original_image is None:
            return
        
        # Sobel edge detection
        def sobel_filter(image):
            # Sobel kernels
            sobel_x = np.array([[-1, 0, 1], 
                                [-2, 0, 2], 
                                [-1, 0, 1]])
            sobel_y = np.array([[-1, -2, -1], 
                                [0, 0, 0], 
                                [1, 2, 1]])
            
            h, w = image.shape
            result = np.zeros_like(image)
            
            for i in range(1, h-1):
                for j in range(1, w-1):
                    # Compute gradient in x and y directions
                    gx = np.sum(image[i-1:i+2, j-1:j+2] * sobel_x)
                    gy = np.sum(image[i-1:i+2, j-1:j+2] * sobel_y)
                    
                    # Compute gradient magnitude
                    result[i, j] = np.sqrt(gx**2 + gy**2)
            
            # Normalize to 0-255 range
            result = (result / result.max() * 255).astype(np.uint8)
            return result
        
        self.filtered_image = sobel_filter(self.original_image)
        self._display_filtered_image(self.filtered_image)

    def apply_sharpen_filter(self):
        if self.original_image is None:
            return
        
        # High-pass sharpening filter
        def sharpen_filter(image):
            # Sharpening kernel
            kernel = np.array([[-1, -1, -1], 
                               [-1,  9, -1], 
                               [-1, -1, -1]])
            
            h, w = image.shape
            result = np.zeros_like(image)
            
            for i in range(1, h-1):
                for j in range(1, w-1):
                    result[i, j] = np.sum(image[i-1:i+2, j-1:j+2] * kernel)
            
            # Clip values to 0-255 range
            result = np.clip(result, 0, 255).astype(np.uint8)
            return result
        
        self.filtered_image = sharpen_filter(self.original_image)
        self._display_filtered_image(self.filtered_image)

    def apply_gaussian_blur(self):
        if self.original_image is None:
            return
        
        # Gaussian blur filter
        def gaussian_filter(image, sigma=1.0):
            # Create Gaussian kernel
            kernel_size = int(6 * sigma + 1)
            kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
            
            # Generate 1D Gaussian kernel
            x = np.linspace(-(kernel_size-1)/2, (kernel_size-1)/2, kernel_size)
            kernel_1d = np.exp(-x**2 / (2 * sigma**2))
            kernel_1d /= kernel_1d.sum()
            
            # Create 2D kernel by outer product
            kernel_2d = np.outer(kernel_1d, kernel_1d)
            
            h, w = image.shape
            result = np.zeros_like(image)
            pad = kernel_size // 2
            
            for i in range(pad, h-pad):
                for j in range(pad, w-pad):
                    neighborhood = image[i-pad:i+pad+1, j-pad:j+pad+1]
                    result[i, j] = np.sum(neighborhood * kernel_2d)
            
            return result.astype(np.uint8)
        
        self.filtered_image = gaussian_filter(self.original_image)
        self._display_filtered_image(self.filtered_image)

    def _display_filtered_image(self, filtered_array):
        # Convert numpy array to QImage
        h, w = filtered_array.shape
        q_image = QImage(filtered_array.data, w, h, w, QImage.Format_Grayscale8)
        
        # Display filtered image
        pixmap = QPixmap.fromImage(q_image)
        self.filtered_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

def main():
    app = QApplication(sys.argv)
    widget = ImageFilterWidget()
    widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()