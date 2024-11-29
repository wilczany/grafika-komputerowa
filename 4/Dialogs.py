from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton

import Layout

class RGBInputDialog(QDialog):
    def __init__(self):
        
        Layout.do_dialog_layout(self)
        
        
        
    def get_rgb(self):
        return(
            self.red_spinner.value(),
            self.green_spinner.value(),
            self.blue_spinner.value()   
        )