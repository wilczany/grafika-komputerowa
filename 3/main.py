import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, 
                             QSlider, QTabWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QLinearGradient, QBrush

class ColorPreview(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor(0, 0, 0)
        self.setMinimumSize(100, 100)
        
    def setColor(self, color):
        self.color = color
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QBrush(self.color))

class ColorSlider(QWidget):
    def __init__(self, orientation=Qt.Horizontal):
        super().__init__()
        self.orientation = orientation
        self.setMinimumSize(20, 20)
        
    def setGradient(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient()
        
        if self.orientation == Qt.Horizontal:
            gradient.setStart(0, 0)
            gradient.setFinalStop(self.width(), 0)
        else:
            gradient.setStart(0, self.height())
            gradient.setFinalStop(0, 0)
            
        gradient.setColorAt(0, self.color1)
        gradient.setColorAt(1, self.color2)
        painter.fillRect(self.rect(), QBrush(gradient))

class RGBWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # RGB controls
        rgb_layout = QHBoxLayout()
        
        # Red channel
        red_layout = QVBoxLayout()
        self.red_label = QLabel("Red:")
        self.red_slider = QSlider(Qt.Horizontal)
        self.red_slider.setRange(0, 255)
        self.red_spin = QSpinBox()
        self.red_spin.setRange(0, 255)
        self.red_gradient = ColorSlider(Qt.Horizontal)
        self.red_gradient.setGradient(QColor(0, 0, 0), QColor(255, 0, 0))
        
        red_layout.addWidget(self.red_label)
        red_layout.addWidget(self.red_gradient)
        red_layout.addWidget(self.red_slider)
        red_layout.addWidget(self.red_spin)
        
        # Green channel
        green_layout = QVBoxLayout()
        self.green_label = QLabel("Green:")
        self.green_slider = QSlider(Qt.Horizontal)
        self.green_slider.setRange(0, 255)
        self.green_spin = QSpinBox()
        self.green_spin.setRange(0, 255)
        self.green_gradient = ColorSlider(Qt.Horizontal)
        self.green_gradient.setGradient(QColor(0, 0, 0), QColor(0, 255, 0))
        
        green_layout.addWidget(self.green_label)
        green_layout.addWidget(self.green_gradient)
        green_layout.addWidget(self.green_slider)
        green_layout.addWidget(self.green_spin)
        
        # Blue channel
        blue_layout = QVBoxLayout()
        self.blue_label = QLabel("Blue:")
        self.blue_slider = QSlider(Qt.Horizontal)
        self.blue_slider.setRange(0, 255)
        self.blue_spin = QSpinBox()
        self.blue_spin.setRange(0, 255)
        self.blue_gradient = ColorSlider(Qt.Horizontal)
        self.blue_gradient.setGradient(QColor(0, 0, 0), QColor(0, 0, 255))
        
        blue_layout.addWidget(self.blue_label)
        blue_layout.addWidget(self.blue_gradient)
        blue_layout.addWidget(self.blue_slider)
        blue_layout.addWidget(self.blue_spin)
        
        rgb_layout.addLayout(red_layout)
        rgb_layout.addLayout(green_layout)
        rgb_layout.addLayout(blue_layout)
        
        # Preview
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Preview:")
        self.color_preview = ColorPreview()
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.color_preview)
        
        # CMYK values display
        cmyk_layout = QHBoxLayout()
        self.cmyk_label = QLabel("CMYK values:")
        self.cmyk_values = QLabel()
        cmyk_layout.addWidget(self.cmyk_label)
        cmyk_layout.addWidget(self.cmyk_values)
        
        layout.addLayout(rgb_layout)
        layout.addLayout(preview_layout)
        layout.addLayout(cmyk_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.red_slider.valueChanged.connect(self.red_spin.setValue)
        self.red_spin.valueChanged.connect(self.red_slider.setValue)
        self.green_slider.valueChanged.connect(self.green_spin.setValue)
        self.green_spin.valueChanged.connect(self.green_slider.setValue)
        self.blue_slider.valueChanged.connect(self.blue_spin.setValue)
        self.blue_spin.valueChanged.connect(self.blue_slider.setValue)
        
        self.red_spin.valueChanged.connect(self.updateColor)
        self.green_spin.valueChanged.connect(self.updateColor)
        self.blue_spin.valueChanged.connect(self.updateColor)
        
    def updateColor(self):
        r = self.red_spin.value()
        g = self.green_spin.value()
        b = self.blue_spin.value()
        
        color = QColor(r, g, b)
        self.color_preview.setColor(color)
        
        # Convert to CMYK
        r_normalized = r / 255
        g_normalized = g / 255
        b_normalized = b / 255
        
        k = 1 - max(r_normalized, g_normalized, b_normalized)
        
        if k == 1:
            c = m = y = 0
        else:
            c = (1 - r_normalized - k) / (1 - k)
            m = (1 - g_normalized - k) / (1 - k)
            y = (1 - b_normalized - k) / (1 - k)
        
        self.cmyk_values.setText(f"C: {c:.2%} M: {m:.2%} Y: {y:.2%} K: {k:.2%}")

class CMYKWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()
        
    def setupUI(self):
        layout = QVBoxLayout()
        
        # CMYK controls
        cmyk_layout = QHBoxLayout()
        
        # Cyan channel
        cyan_layout = QVBoxLayout()
        self.cyan_label = QLabel("Cyan:")
        self.cyan_slider = QSlider(Qt.Horizontal)
        self.cyan_slider.setRange(0, 100)
        self.cyan_spin = QDoubleSpinBox()
        self.cyan_spin.setRange(0, 100)
        self.cyan_spin.setSuffix("%")
        self.cyan_gradient = ColorSlider(Qt.Horizontal)
        self.cyan_gradient.setGradient(QColor(255, 255, 255), QColor(0, 255, 255))
        
        cyan_layout.addWidget(self.cyan_label)
        cyan_layout.addWidget(self.cyan_gradient)
        cyan_layout.addWidget(self.cyan_slider)
        cyan_layout.addWidget(self.cyan_spin)
        
        # Magenta channel
        magenta_layout = QVBoxLayout()
        self.magenta_label = QLabel("Magenta:")
        self.magenta_slider = QSlider(Qt.Horizontal)
        self.magenta_slider.setRange(0, 100)
        self.magenta_spin = QDoubleSpinBox()
        self.magenta_spin.setRange(0, 100)
        self.magenta_spin.setSuffix("%")
        self.magenta_gradient = ColorSlider(Qt.Horizontal)
        self.magenta_gradient.setGradient(QColor(255, 255, 255), QColor(255, 0, 255))
        
        magenta_layout.addWidget(self.magenta_label)
        magenta_layout.addWidget(self.magenta_gradient)
        magenta_layout.addWidget(self.magenta_slider)
        magenta_layout.addWidget(self.magenta_spin)
        
        # Yellow channel
        yellow_layout = QVBoxLayout()
        self.yellow_label = QLabel("Yellow:")
        self.yellow_slider = QSlider(Qt.Horizontal)
        self.yellow_slider.setRange(0, 100)
        self.yellow_spin = QDoubleSpinBox()
        self.yellow_spin.setRange(0, 100)
        self.yellow_spin.setSuffix("%")
        self.yellow_gradient = ColorSlider(Qt.Horizontal)
        self.yellow_gradient.setGradient(QColor(255, 255, 255), QColor(255, 255, 0))
        
        yellow_layout.addWidget(self.yellow_label)
        yellow_layout.addWidget(self.yellow_gradient)
        yellow_layout.addWidget(self.yellow_slider)
        yellow_layout.addWidget(self.yellow_spin)
        
        # Key (Black) channel
        key_layout = QVBoxLayout()
        self.key_label = QLabel("Key (Black):")
        self.key_slider = QSlider(Qt.Horizontal)
        self.key_slider.setRange(0, 100)
        self.key_spin = QDoubleSpinBox()
        self.key_spin.setRange(0, 100)
        self.key_spin.setSuffix("%")
        self.key_gradient = ColorSlider(Qt.Horizontal)
        self.key_gradient.setGradient(QColor(255, 255, 255), QColor(0, 0, 0))
        
        key_layout.addWidget(self.key_label)
        key_layout.addWidget(self.key_gradient)
        key_layout.addWidget(self.key_slider)
        key_layout.addWidget(self.key_spin)
        
        cmyk_layout.addLayout(cyan_layout)
        cmyk_layout.addLayout(magenta_layout)
        cmyk_layout.addLayout(yellow_layout)
        cmyk_layout.addLayout(key_layout)
        
        # Preview
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Preview:")
        self.color_preview = ColorPreview()
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.color_preview)
        
        # RGB values display
        rgb_layout = QHBoxLayout()
        self.rgb_label = QLabel("RGB values:")
        self.rgb_values = QLabel()
        rgb_layout.addWidget(self.rgb_label)
        rgb_layout.addWidget(self.rgb_values)
        
        layout.addLayout(cmyk_layout)
        layout.addLayout(preview_layout)
        layout.addLayout(rgb_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.cyan_slider.valueChanged.connect(lambda x: self.cyan_spin.setValue(x))
        self.cyan_spin.valueChanged.connect(lambda x: self.cyan_slider.setValue(int(x)))
        self.magenta_slider.valueChanged.connect(lambda x: self.magenta_spin.setValue(x))
        self.magenta_spin.valueChanged.connect(lambda x: self.magenta_slider.setValue(int(x)))
        self.yellow_slider.valueChanged.connect(lambda x: self.yellow_spin.setValue(x))
        self.yellow_spin.valueChanged.connect(lambda x: self.yellow_slider.setValue(int(x)))
        self.key_slider.valueChanged.connect(lambda x: self.key_spin.setValue(x))
        self.key_spin.valueChanged.connect(lambda x: self.key_slider.setValue(int(x)))
        
        self.cyan_spin.valueChanged.connect(self.updateColor)
        self.magenta_spin.valueChanged.connect(self.updateColor)
        self.yellow_spin.valueChanged.connect(self.updateColor)
        self.key_spin.valueChanged.connect(self.updateColor)
        
    def updateColor(self):
        c = self.cyan_spin.value() / 100
        m = self.magenta_spin.value() / 100
        y = self.yellow_spin.value() / 100
        k = self.key_spin.value() / 100
        
        # Convert to RGB
        r = int(255 * (1 - c) * (1 - k))
        g = int(255 * (1 - m) * (1 - k))
        b = int(255 * (1 - y) * (1 - k))
        
        color = QColor(r, g, b)
        self.color_preview.setColor(color)
        self.rgb_values.setText(f"R: {r} G: {g} B: {b}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Space Converter")
        self.setMinimumSize(800, 600)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Create RGB and CMYK tabs
        rgb_widget = RGBWidget()
        cmyk_widget = CMYKWidget()
        
        tab_widget.addTab(rgb_widget, "RGB")
        tab_widget.addTab(cmyk_widget, "CMYK")
        
        self.setCentralWidget(tab_widget)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()