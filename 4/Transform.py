from PySide6.QtWidgets import (
    QWidget,
    QInputDialog,
    QFileDialog,
    QMessageBox)
from PySide6.QtGui import QImage
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
    
    def get_operation_value(self):
        value, ok 
        if not ok or not value:
            return
        return value
    def add_value(self):
        value = self.get_operation_value()
        if not value:
            return
        
        
    def subtract_value(self):
        value = self.get_operation_value()
        if not value:
            return
        
    def multiply_value(self):
        value = self.get_operation_value()
        if not value:
            return
        
    def divide_value(self):
        value = self.get_operation_value()
        if not value:
            return
        
    def change_brightness(self):
        value = self.get_operation_value()
        if not value:
            return
    
        
    