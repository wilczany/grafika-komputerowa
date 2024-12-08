from PySide6.QtGui import QColor, QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QFileDialog
import numpy as np
import Layout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        Layout.do_main_layout(self)
        self.original_image = None
        self.current_image = None
